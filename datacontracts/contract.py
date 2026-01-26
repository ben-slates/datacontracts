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
    def validate(cls, df: pd.DataFrame, autocorrect=False):
        errors = []
        df = df.copy()

        for name, col in cls.columns().items():

            if name not in df.columns:
                errors.append(f"Missing column: {name}")
                continue

            series = df[name]
            is_null = series.isna()

            # Null handling
            if not col.nullable and is_null.any():
                for idx in series[is_null].index:
                    errors.append(
                        f"Column '{name}' must not be null (row {idx})"
                    )

            clean = series[~is_null]

            # Type check (never autocorrect)
            invalid = clean[~clean.map(lambda x: isinstance(x, col.dtype))]
            for idx, value in invalid.items():
                errors.append(
                    f"Column '{name}' has wrong type (row {idx}, value={value})"
                )

            # Auto-correct helpers
            def clip_value(v, low=None, high=None):
                if low is not None:
                    v = max(v, low)
                if high is not None:
                    v = min(v, high)
                return v

            # lt
            if col.lt is not None:
                invalid = clean[clean >= col.lt]
                for idx, value in invalid.items():
                    if autocorrect and col.autocorrect == "clip":
                        df.at[idx, name] = col.lt - 1
                    else:
                        errors.append(
                            f"Column '{name}' must be < {col.lt} "
                            f"(row {idx}, value={value})"
                        )

            # gt
            if col.gt is not None:
                invalid = clean[clean <= col.gt]
                for idx, value in invalid.items():
                    if autocorrect and col.autocorrect == "clip":
                        df.at[idx, name] = col.gt + 1
                    else:
                        errors.append(
                            f"Column '{name}' must be > {col.gt} "
                            f"(row {idx}, value={value})"
                        )

            # between
            if col.between is not None:
                low, high = col.between
                invalid = clean[(clean < low) | (clean > high)]
                for idx, value in invalid.items():
                    if autocorrect and col.autocorrect == "clip":
                        df.at[idx, name] = clip_value(value, low, high)
                    else:
                        errors.append(
                            f"Column '{name}' must be between {low} and {high} "
                            f"(row {idx}, value={value})"
                        )

            # allowed
            if col.allowed is not None:
                invalid = clean[~clean.isin(col.allowed)]
                for idx, value in invalid.items():
                    if autocorrect and col.autocorrect == "null":
                        df.at[idx, name] = None
                    else:
                        errors.append(
                            f"Column '{name}' has invalid value "
                            f"(row {idx}, value={value})"
                        )

        if errors and not autocorrect:
            raise ContractError(errors)

        return df
