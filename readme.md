# `datacontracts`: Minimal Data Contracts for Pandas

[![PyPI version](https://img.shields.io/pypi/v/datacontracts.svg)](https://pypi.org/project/datacontracts/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A small Python library for enforcing data contracts on **pandas DataFrames**.

`datacontracts` lets you define simple rules for your data (types, ranges, allowed values)
and **fail fast** when data violates those rules — with clear, row-level error messages.

This library is intentionally minimal and explicit.

---

## Why this exists

Pandas allows invalid data to flow silently:

*   wrong types
*   out-of-range values
*   unexpected categories

These issues are usually discovered late — in dashboards, models, or production.

`datacontracts` stops bad data **early**.

---

## Installation

```bash
pip install datacontracts
```

---

## Usage

The core workflow uses Python classes to define the contract, making it explicit and readable.

### Quick Example

#### 1. Define a Contract
Define your contract by inheriting from `Contract` and using `Column` objects to specify constraints.

```python
from datacontracts import Contract, Column

class Users(Contract):
    # Column(expected_type, min=..., max=..., allowed=[...], unique=...)
    user_id = Column(int, min=1)
    age = Column(int, min=0, max=120)
    country = Column(str, allowed=["US", "UK", "CA"])
```

#### 2. Validate a DataFrame
Pass your DataFrame to the static `validate()` method.

```python
import pandas as pd

df = pd.DataFrame({
    "user_id": [1, 2, 3],
    "age": [25, 999, 150],
    "country": ["US", "UK", "CA"]
})

Users.validate(df)
```

#### Output (v0.1.2 - Row-Level Errors)
When validation fails, `datacontracts` reports *all* invalid rows with clear, actionable details:

```
ContractError:
Column 'age' above max 120 (row 1, value=999)
Column 'age' above max 120 (row 2, value=150)
```

Each error specifies:
*   The column name
*   The row number (DataFrame index)
*   The offending value

If all checks pass, the method returns silently.

### Common Use Cases

`datacontracts` is ideal for validating data at critical hand-off points:

*   **Database Exports:** Ensuring data pulled from a database conforms to expectations.
*   **User-Uploaded CSVs:** Providing immediate, clear feedback on data quality.
*   **ETL Pipelines:** Stopping bad data before it enters the warehouse.
*   **Pre-ML Validation:** Guaranteeing model inputs meet feature requirements.

---

## Contract Specification Details

The `Column` object supports the following constraints:

| Constraint | Type | Description |
| :--- | :--- | :--- |
| **Type** | `type` (e.g., `int`, `str`, `float`) | The required Python type for the column's values. |
| `min` | `Number` | The minimum inclusive value allowed. |
| `max` | `Number` | The maximum inclusive value allowed. |
| `allowed` | `list` or `set` | A collection of all permissible categorical values. |
| `unique` | `bool` | If `True`, all values in the column must be unique (no duplicates). |
| **Existence** | (Implicit) | The column must exist in the DataFrame. |

---

## Scope and Philosophy

### What this library does NOT do

`datacontracts` is intentionally minimal and focused. It does not handle:

*   SQL or database-level validation
*   Spark or distributed data processing
*   Automatic data fixing or imputation
*   Statistical drift detection or complex profiling
*   Schema inference (contracts must be explicit)

**Correctness comes before convenience.**

### Philosophy

*   **Explicit is better than implicit:** Contracts should be defined clearly in code.
*   **Fail early, fail loudly:** Stop bad data immediately with descriptive errors.
*   **Small surface area:** The library should be easy to learn and maintain.
*   **Readable source code:** The entire codebase is designed to be understandable in one sitting.

---

## Development

Run tests:

```bash
python -m pytest
```

## License

MIT
