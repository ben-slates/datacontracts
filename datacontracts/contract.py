import pandas as pd
from .column import Column
from .errors import ContractError


class Contract:
    @classmethod
    def columns(cls):
        return {
            name: value
            for name, value in cls.__dict__.items()
            if isinstance(value, Column)
        }

    @classmethod
    def validate(cls, df: pd.DataFrame):
        errors = []

        for name, col in cls.columns().items():

            # Column existence
            if name not in df.columns:
                errors.append(f"Missing column: {name}")
                continue

            series = df[name]

            # Handle nulls
            is_null = series.isna()
            if not col.nullable and is_null.any():
                for idx, value in series[is_null].items():
                    errors.append(
                        f"Column '{name}' must not be null "
                        f"(row {idx}, value={value})"
                    )

            # Work only on non-null values
            clean = series[~is_null]

            # Type check
            invalid = clean[~clean.map(lambda x: isinstance(x, col.dtype))]
            for idx, value in invalid.items():
                errors.append(
                    f"Column '{name}' has wrong type "
                    f"(row {idx}, value={value})"
                )

            # Min check
            if col.min is not None:
                invalid = clean[clean < col.min]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be >= {col.min} "
                        f"(row {idx}, value={value})"
                    )

            # Max check
            if col.max is not None:
                invalid = clean[clean > col.max]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be <= {col.max} "
                        f"(row {idx}, value={value})"
                    )

            # Less than check
            if col.lt is not None:
                invalid = clean[clean >= col.lt]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be < {col.lt} "
                        f"(row {idx}, value={value})"
                    )

            # Greater than check
            if col.gt is not None:
                invalid = clean[clean <= col.gt]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be > {col.gt} "
                        f"(row {idx}, value={value})"
                    )

            # Between check
            if col.between is not None:
                low, high = col.between
                invalid = clean[(clean < low) | (clean > high)]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be between {low} and {high} "
                        f"(row {idx}, value={value})"
                    )

            # Allowed values
            if col.allowed is not None:
                invalid = clean[~clean.isin(col.allowed)]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' has invalid value "
                        f"(row {idx}, value={value})"
                    )

        if errors:
            raise ContractError(errors)
