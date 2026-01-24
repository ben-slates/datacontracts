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

            if name not in df.columns:
                errors.append(f"Missing column: {name}")
                continue

            series = df[name]

            # Type check
            invalid = series[~series.map(lambda x: isinstance(x, col.dtype))]
            for idx, value in invalid.items():
                errors.append(
                    f"Column '{name}' has wrong type (row {idx}, value={value})"
                )

            # Min check
            if col.min is not None:
                invalid = series[series < col.min]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be >= {col.min} "
                        f"(row {idx}, value={value})"
                    )

            # Max check
            if col.max is not None:
                invalid = series[series > col.max]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be <= {col.max} "
                        f"(row {idx}, value={value})"
                    )

            # Less than check
            if col.lt is not None:
                invalid = series[series >= col.lt]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be < {col.lt} "
                        f"(row {idx}, value={value})"
                    )

            # Greater than check
            if col.gt is not None:
                invalid = series[series <= col.gt]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be > {col.gt} "
                        f"(row {idx}, value={value})"
                    )

            # Between check (ONLY allowed range)
            if col.between is not None:
                low, high = col.between
                invalid = series[(series < low) | (series > high)]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' must be between {low} and {high} "
                        f"(row {idx}, value={value})"
                    )

            # Allowed values
            if col.allowed is not None:
                invalid = series[~series.isin(col.allowed)]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' has invalid value "
                        f"(row {idx}, value={value})"
                    )

        if errors:
            raise ContractError(errors)
