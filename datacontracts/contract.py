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

            # 1. Column existence
            if name not in df.columns:
                errors.append(f"Missing column: {name}")
                continue

            series = df[name]

            # 2. Type check (ALL invalid)
            invalid = series[~series.map(lambda x: isinstance(x, col.dtype))]
            for idx, value in invalid.items():
                errors.append(
                    f"Column '{name}' has wrong type "
                    f"(row {idx}, value={value})"
                )

            # 3. Min check (ALL invalid)
            if col.min is not None:
                invalid = series[series < col.min]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' below min {col.min} "
                        f"(row {idx}, value={value})"
                    )

            # 4. Max check (ALL invalid)
            if col.max is not None:
                invalid = series[series > col.max]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' above max {col.max} "
                        f"(row {idx}, value={value})"
                    )

            # 5. Allowed values check (ALL invalid)
            if col.allowed is not None:
                invalid = series[~series.isin(col.allowed)]
                for idx, value in invalid.items():
                    errors.append(
                        f"Column '{name}' has invalid value "
                        f"(row {idx}, value={value})"
                    )

        if errors:
            raise ContractError(errors)
