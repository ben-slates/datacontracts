import pandas as pd
import pytest

from datacontracts import Contract, Column
from datacontracts.errors import ContractError

class Users(Contract):
    user_id = Column(int, min=1)
    age = Column(int, min=0, max=120)


def test_valid_users_pass():
    df = pd.DataFrame({
        "user_id": [1, 2, 3],
        "age": [20, 30, 40]
    })

    # Should NOT raise an error
    Users.validate(df)

def test_invalid_users_fail():
    df = pd.DataFrame({
        "user_id": [1, 2],
        "age": [25, 999]  # invalid age
    })

    with pytest.raises(ContractError):
        Users.validate(df)
