# `datacontracts`: Minimal Data Contracts for Pandas

[![PyPI version](https://img.shields.io/pypi/v/datacontracts.svg)](https://pypi.org/project/datacontracts/)
[![License](https://img.shields.io/pypi/l/datacontracts.svg)](https://pypi.org/project/datacontracts/)


A small Python library for enforcing **data contracts** on `pandas` DataFrames.

`datacontracts` lets you define simple, explicit rules—covering data types, value ranges, and allowed categories—for your data. By validating these contracts early in your data pipeline, you ensure data quality and prevent bad data from silently corrupting downstream processes.

This library is intentionally **minimal and boring**. It focuses on one thing: **failing fast** when data quality is compromised.

---

## Why this exists

The flexibility of the `pandas` library, while powerful, can be a source of silent data quality issues:

*   **Wrong Types:** A column expected to be an integer is loaded as a string.
*   **Out-of-Range Values:** A sensor reading is negative when it should be positive.
*   **Unexpected Categories:** A column meant to contain only 'A', 'B', or 'C' suddenly contains 'Z'.

These problems are often discovered late—in production dashboards, failing scripts, or degraded machine learning models—after the bad data has already propagated.

`datacontracts` shifts the validation left, ensuring that any data entering your system meets the required specification *before* it is processed.

---

## Installation

The library is available on PyPI.

```bash
pip install datacontracts
```

---

## Usage

The core workflow involves two steps: defining a `DataContract` and then using it to `validate` a `pandas` DataFrame.

### 1. Define the Contract

A contract is defined by a list of `Field` objects, each specifying the expected properties of a column.

```python
from datacontracts import DataContract, Field
import pandas as pd

# Define the contract for a 'User Activity' dataset
user_activity_contract = DataContract(
    fields=[
        # Enforce type and non-null constraint
        Field("user_id", dtype="int64", required=True),
        
        # Enforce string type and allowed categorical values
        Field("event_type", dtype="object", allowed_values=["login", "logout", "purchase", "view"]),
        
        # Enforce a numerical range
        Field("duration_seconds", dtype="float64", min_value=0.0, max_value=3600.0),
        
        # Enforce a specific datetime format and ensure it's not in the future
        Field("timestamp", dtype="datetime64[ns]", max_value=pd.Timestamp.now()),
    ]
)
```

### 2. Validate the Data

Pass your DataFrame to the `.validate()` method. If the data conforms to the contract, the method returns `None` (or the DataFrame itself, for chaining). If the data violates any rule, it raises a descriptive `DataContractError`.

```python
# Example of valid data
valid_data = pd.DataFrame({
    "user_id": [101, 102],
    "event_type": ["login", "purchase"],
    "duration_seconds": [15.5, 120.0],
    "timestamp": [pd.Timestamp("2024-01-15"), pd.Timestamp("2024-01-16")]
})

try:
    user_activity_contract.validate(valid_data)
    print("Data is valid. Proceeding with analysis.")
except DataContractError as e:
    # This block will not be executed for valid_data
    print(f"Validation failed: {e}")

# Example of invalid data (wrong type and out-of-range value)
invalid_data = pd.DataFrame({
    "user_id": ["A101", 102], # Wrong type (string instead of int64)
    "event_type": ["login", "sale"], # Unexpected category ('sale')
    "duration_seconds": [-5.0, 120.0], # Out-of-range value (-5.0)
    "timestamp": [pd.Timestamp("2024-01-15"), pd.Timestamp("2024-01-16")]
})

try:
    user_activity_contract.validate(invalid_data)
except DataContractError as e:
    print("\n--- Validation Failed ---")
    print(e)
    # Output will clearly list all violations found
```

### Expected Output on Failure

When validation fails, `datacontracts` aggregates all violations into a single, easy-to-read error message:

```
--- Validation Failed ---
DataContractError: The following contract violations were found:

1. Column 'user_id': Expected dtype 'int64', found 'object'. (Violation Type: DtypeMismatch)
2. Column 'event_type': Found 1 unexpected value(s) not in allowed set {'login', 'logout', 'purchase', 'view'}. Unexpected values: ['sale']. (Violation Type: AllowedValues)
3. Column 'duration_seconds': Found 1 value(s) below the minimum allowed value of 0.0. Minimum violation: -5.0. (Violation Type: RangeViolation)
```

---

## Contract Specification Details

The `Field` class supports the following parameters for defining robust contracts:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | **Required.** The name of the DataFrame column. |
| `dtype` | `str` | **Required.** The expected `pandas` dtype (e.g., `'int64'`, `'float64'`, `'object'`, `'datetime64[ns]'`). |
| `required` | `bool` | If `True`, the column must be present in the DataFrame. (Default: `False`) |
| `min_value` | `Number` / `Timestamp` | The minimum inclusive value allowed for numerical or datetime fields. |
| `max_value` | `Number` / `Timestamp` | The maximum inclusive value allowed for numerical or datetime fields. |
| `allowed_values` | `list` / `set` | A collection of all permissible values for categorical fields. |
| `regex` | `str` | A regular expression pattern that all string values in the column must match. |
| `unique` | `bool` | If `True`, all values in the column must be unique (no duplicates). (Default: `False`) |

---

## Development and Contributing

We welcome contributions! As the project aims to be minimal and boring, contributions should focus on:

1.  **Robustness:** Improving error handling and performance.
2.  **Clarity:** Enhancing the error messages and documentation.
3.  **Minimal Features:** Adding only essential validation types that are widely applicable and do not introduce significant complexity.

To contribute, please fork the repository, create a feature branch, and submit a pull request.

## License

`datacontracts` is released under the **MIT License**. See the `LICENSE` file for details.
