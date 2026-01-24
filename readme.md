# `datacontracts`: Minimal Data Contracts for Pandas

[![PyPI version](https://img.shields.io/pypi/v/datacontracts.svg)](https://pypi.org/project/datacontracts/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A small Python library for enforcing **business-friendly data contracts** on `pandas` DataFrames.

**v0.1.3** introduces expressive, human-readable rules (`lt`, `gt`, `between`) that allow you to define data quality expectations the way you think about them. `datacontracts` validates these contracts and **reports all invalid rows** with clear, actionable error messages.

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

## Usage (v0.1.3)

The core workflow uses Python classes to define the contract, making it explicit and readable.

### Quick Example

#### 1. Define a Contract
Define your contract by inheriting from `Contract` and using `Column` objects to specify constraints.

```python
from datacontracts import Contract, Column

class AuthorRules(Contract):
    # Expressive rules: must be less than 100
    author_followers = Column(int, lt=100)
    
    # Expressive range: must be between 1 and 9 (inclusive)
    author_books = Column(int, between=(1, 9))
    
    # Traditional rule: must be greater than 50
    user_rating = Column(float, gt=50)
```

#### 2. Validate a DataFrame
Pass your DataFrame to the static `validate()` method.

```python
import pandas as pd

df = pd.DataFrame({
    "author_followers": [99, 120, 50],
    "author_books": [5, 15, 0],
    "user_rating": [55.0, 49.9, 80.0]
})

AuthorRules.validate(df)
```

#### Output (Comprehensive Reporting)
v0.1.3 reports *every* violation across *all* columns with clear, human-readable messages:

```
ContractError:
Column 'author_followers' must be < 100 (row 1, value=120)
Column 'author_books' must be between 1 and 9 (row 2, value=15)
Column 'author_books' must be between 1 and 9 (row 2, value=0)
Column 'user_rating' must be > 50 (row 1, value=49.9)
```

This makes debugging and data cleaning much faster. If all checks pass, the method returns silently.

### Typical Real-World Use Cases

`datacontracts` is ideal for validating data at critical hand-off points:

*   **CSV/Excel Files:** Providing immediate, clear feedback on user-uploaded data quality.
*   **ETL Pipelines:** Stopping bad data before it enters the data warehouse.
*   **Pre-ML Validation:** Guaranteeing model inputs meet feature requirements.

---

## Contract Specification Details (v0.1.3)

The `Column` object supports the following constraints, allowing you to define rules the way you think about data:

| Constraint | Type | Description |
| :--- | :--- | :--- |
| **Type** | `type` (e.g., `int`, `str`, `float`) | The required Python type for the column's values. |
| `lt` | `Number` | **Less than** (e.g., `lt=100` means `< 100`). |
| `gt` | `Number` | **Greater than** (e.g., `gt=50` means `> 50`). |
| `between` | `Tuple[Number, Number]` | **Inclusive range** (e.g., `between=(1, 9)` means `1 <= value <= 9`). |
| `allowed` | `list` or `set` | A collection of all permissible categorical values. |
| `unique` | `bool` | If `True`, all values in the column must be unique (no duplicates). |
| `min` / `max` | `Number` | Traditional minimum/maximum (still supported, but `lt`/`gt` are recommended for clarity). |

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
