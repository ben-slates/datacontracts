# `datacontracts`: Minimal Data Contracts for Pandas

[![PyPI version](https://img.shields.io/pypi/v/datacontracts.svg)](https://pypi.org/project/datacontracts/)
[![Python versions](https://img.shields.io/pypi/pyversions/datacontracts.svg)](https://pypi.org/project/datacontracts/)
[![License](https://img.shields.io/pypi/l/datacontracts.svg)](https://pypi.org/project/datacontracts/)

A small Python library for enforcing **explicit data contracts** on **pandas DataFrames**.

`datacontracts` lets you define **business rules** for your data and:
-  fail fast when data is invalid
-  optionally auto-correct safe violations

Minimal, explicit, and predictable.

---

## Why this exists

The flexibility of the `pandas` library, while powerful, can be a source of silent data quality issues:

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

## Usage (v0.1.5)

The core workflow uses Python classes to define the contract, making it explicit and readable.

### Quick Example: Fail Fast (Default)

By default, `datacontracts` operates in its traditional **fail fast** mode, reporting all violations with clear, row-level error messages.

#### 1. Define a Contract
We use expressive, business-friendly rules like `lt`, `gt`, and `between`.

```python
from datacontracts import Contract, Column
import pandas as pd

class ProductContract(Contract):
    # Must be less than 100
    price = Column(int, lt=100)
    
    # Must be between 1 and 9 (inclusive)
    stock = Column(int, between=(1, 9))
```

#### 2. Validate (Fail Fast)
```python
df = pd.DataFrame({
    "price": [99, 120, 50], # 120 is invalid
    "stock": [5, 15, 0]     # 15 and 0 are invalid
})

# This will raise a ContractError, reporting all three violations
ProductContract.validate(df) 
```

### New in v0.1.5: Validate and Auto-Correct

For **safe, non-ambiguous violations** (like type coercion or clamping to a boundary), v0.1.5 introduces an optional auto-correction mode. This allows data to flow while ensuring it meets the contract's specification.

#### 3. Validate and Fix
Pass `fix=True` to the `validate` method. The method will return the corrected DataFrame and log any changes made.

```python
# Example data with a type violation (float instead of int) and a range violation
df_to_fix = pd.DataFrame({
    "price": [99.5, 120, 50], # 99.5 (type violation), 120 (range violation)
    "stock": [5, 15, 0]
})

# This returns a corrected DataFrame and logs the changes
corrected_df = ProductContract.validate(df_to_fix, fix=True)

# corrected_df will now have:
# price: [99, 100, 50] (99.5 coerced to 99, 120 clamped to 100)
# stock: [5, 9, 1] (15 clamped to 9, 0 clamped to 1)
```

**Note:** Auto-correction is only applied to violations where the fix is explicit and safe (e.g., clamping a value to a defined boundary, or coercing a float to an integer). Ambiguous violations (like missing values or unexpected categories) will still raise an error unless explicitly handled.

---

## Contract Specification Details

The `Column` object supports the following constraints:

| Constraint | Type | Description |
| :--- | :--- | :--- |
| **Type** | `type` (e.g., `int`, `str`, `float`) | The required Python type for the column's values. **Coercible types can be fixed with `fix=True`.** |
| `lt` | `Number` | **Less than** (e.g., `lt=100`). **Violations can be clamped with `fix=True`.** |
| `gt` | `Number` | **Greater than** (e.g., `gt=50`). **Violations can be clamped with `fix=True`.** |
| `between` | `Tuple[Number, Number]` | **Inclusive range** (e.g., `between=(1, 9)`). **Violations can be clamped with `fix=True`.** |
| `allowed` | `list` or `set` | A collection of all permissible categorical values. |
| `unique` | `bool` | If `True`, all values in the column must be unique (no duplicates). |

---

## Scope and Philosophy

### Correctness Before Convenience

The introduction of `fix=True` does not compromise the library's core philosophy.

*   **Explicit Control:** Auto-correction is opt-in. The default remains **fail fast**.
*   **Safe Violations Only:** Only violations with clear, deterministic fixes (clamping, type coercion) are corrected. Violations that require business logic (e.g., unexpected categories) still raise an error.
*   **Transparency:** All corrections are logged, ensuring a clear audit trail of data modifications.

### What this library does NOT do

*   SQL or database-level validation
*   Spark or distributed data processing
*   Statistical drift detection or complex profiling
*   Schema inference (contracts must be explicit)

---

## Development

Run tests:

```bash
python -m pytest
```

## License

MIT
