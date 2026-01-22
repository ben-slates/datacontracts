import pandas as pd
from .column import Column
from .errors import ContractError


class Contract:
    @classmethod
    def columns(cls):
        """
        Find all Column definitions inside the contract class.
        Example:
            class Users(Contract):
                age = Column(int)
        """
        return {
            name: value
            for name, value in cls.__dict__.items()
            if isinstance(value, Column)
        }

    @classmethod
    def validate(cls, df: pd.DataFrame):
        """
        Validate a pandas DataFrame against the contract.
        """
        errors = []

        for name, col in cls.columns().items():
            # 1. Column must exist
            if name not in df.columns:
                errors.append(f"Missing column: {name}")
                continue

            series = df[name]

            # 2. Type check
            if not series.map(lambda x: isinstance(x, col.dtype)).all():
                errors.append(f"Column '{name}' has wrong type")

            # 3. Min check
            if col.min is not None:
                if (series < col.min).any():
                    errors.append(f"Column '{name}' below min {col.min}")

            # 4. Max check
            if col.max is not None:
                if (series > col.max).any():
                    errors.append(f"Column '{name}' above max {col.max}")

            # 5. Allowed values check
            if col.allowed is not None:
                if not series.isin(col.allowed).all():
                    errors.append(f"Column '{name}' has invalid values")

        if errors:
            raise ContractError(errors)
