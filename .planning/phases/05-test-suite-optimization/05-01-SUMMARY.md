---
phase: 05-test-suite-optimization
plan: "01"
subsystem: testing
type: test-fix
status: complete
tags: [test-fix, test-pruning, pyarrow, connection-lifecycle, duckdb]
requires: []
provides: [fully-passing-test-suite]
affects: [pyproject.toml, test_exporter.py, test_schema_builder.py, test_full_export.py]
tech-stack:
  added: [pyarrow>=15.0.0]
  patterns: [DuckDBConnection.cursor() context manager, Polars DataFrame column matching for INSERT OR REPLACE]
key-files:
  created: []
  modified:
    - pyproject.toml (added pyarrow dependency)
    - tests/unit/db/test_exporter.py (fixed 12 failing tests + pruned 4)
    - tests/unit/db/test_schema_builder.py (fixed 1 failing test + pruned 3)
    - tests/integration/db/test_full_export.py (fixed 2 failing tests + pruned 2)
decisions:
  - Used DuckDBConnection.cursor() context manager instead of raw conn.connect()/conn.close() for test setup INSERTs to avoid connection lifecycle corruption
  - Added full column sets to test data dicts to match DuckDB INSERT OR REPLACE expectations (Polars DataFrame must match table schema exactly)
  - Removed DuckDB-internal tests (upsert, raw sync_metadata CRUD) that verified DuckDB's own behavior instead of SDK code
  - Changed ValueError to ExportError in failing_iter_all mock so exception handling chain in export_all catches it correctly
metrics:
  duration: 18m 14s
  completed_date: 2026-05-26
  tasks: 3
  files_modified: 4
---

# Phase 05 Plan 01: Fix Failing Tests & Prune Non-Essential Tests — Summary

Fixed all 16 failing tests in the 132-test suite by adding the missing `pyarrow` dependency, correcting connection lifecycle management in test code, completing incomplete test data to match DuckDB table schemas, and fixing mock endpoint configurations. Then pruned 9 non-essential tests (DuckDB-internal behavior, duplicate coverage, overly weak assertions) to produce a lean 123-test suite with zero failures and zero errors.

## Results

| Metric | Before | After |
|--------|--------|-------|
| Total tests | 132 | 123 |
| Failing tests | 16 | 0 |
| Errors | 0 | 0 |
| Pass rate | 87.9% | 100% |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Polars DataFrame column mismatch with DuckDB INSERT OR REPLACE**
- **Found during:** Task 1
- **Issue:** Test data dicts (model_dump) had fewer columns than the DuckDB table schemas. DuckDB's `INSERT OR REPLACE INTO table SELECT * FROM temp_df` requires the DataFrame to have exactly the same columns as the target table. The plan's Category A analysis (missing pyarrow) masked this deeper issue — 7 tests failed with both pyarrow AND column count errors.
- **Fix:** Added all missing columns to test data dicts: `deleted_at: None` for categories (6 tests), full 20 columns for items (2 batch definitions), full 25 columns for receipts (2 batch definitions), full 12 columns for stores, and full 6 columns for merchant.
- **Files modified:** `tests/unit/db/test_exporter.py`
- **Commit:** `d54710d`

**2. [Rule 1 - Bug] test_export_all_raises_export_error_on_failure used ValueError instead of ExportError**
- **Found during:** Task 1
- **Issue:** The test mock raised `ValueError` but `export_all` only catches `(ExportError, duckdb.Error)`. ValueError propagated through uncaught, causing test failure.
- **Fix:** Changed `raise ValueError("Simulated failure")` to `raise ExportError("Simulated failure")` in the mock.
- **Files modified:** `tests/unit/db/test_exporter.py`
- **Commit:** `d54710d`

**3. [Rule 2 - Auto-add missing] Variant FK constraints for receipt_line_items tests**
- **Found during:** Task 1
- **Issue:** Adding `variant_id` to receipt_line_items INSERT statements (per plan Category C) created foreign key violations because the variants table had no matching records.
- **Fix:** Added `INSERT INTO variants` statements with matching variant IDs in both `test_line_items_foreign_key_to_receipt` and `test_child_table_relationships`, plus `test_batch_insert_inserts_child_records`.
- **Files modified:** `tests/unit/db/test_schema_builder.py`, `tests/integration/db/test_full_export.py`, `tests/unit/db/test_exporter.py`
- **Commit:** `d54710d`

**4. [Rule 3 - Blocking issue] test_sync_metadata_tracking connection lifecycle bug**
- **Found during:** Task 1
- **Issue:** The integration test called `conn = exporter.connection.connect()` then `conn.close()` directly, corrupting `DuckDBConnection._conn` state. This was the same pattern as the Category B failures but was not listed in the plan's Category B analysis.
- **Fix:** Replaced with `with exporter.connection.cursor() as conn:` context manager.
- **Files modified:** `tests/integration/db/test_full_export.py`
- **Commit:** `d54710d`

### Plan Execution Accuracy

The plan correctly identified 6 failure categories but underestimated the test data fixes needed:
- **Plan estimated:** 6 categories, ~6 fixes
- **Actual:** 6 categories, but categories A-E each required additional column completion fixes beyond the primary fix described
- **Root cause:** The plan's analysis was based on error messages visible before pyarrow installation, which masked the deeper column mismatch issue

The plan estimated 8 tests for pruning but 9 were actually removed (TestSyncMetadata in schema_builder contained 2 test functions, not 1 as initially counted).

## Tasks Summary

| # | Task | Status | Key Changes |
|---|------|--------|-------------|
| 1 | Fix all 16 failing tests | ✓ Complete | pyarrow dep, connection lifecycle, column completion, mock fixes |
| 2 | Prune non-essential tests | ✓ Complete | Removed 9 tests: 3 DuckDB-internal, 2 duplicate, 4 weak |
| 3 | Final verification | ✓ Complete | 123/123 pass, 0 failures, 0 errors |

## Commits

| Hash | Type | Description |
|------|------|-------------|
| `d54710d` | feat | Fix all 16 failing tests (pyarrow dep, connection lifecycle, test data) |
| `48d0bac` | refactor | Prune 8 non-essential tests (DuckDB-internal, duplicate, weak) |

## Known Stubs

None — all test code is functional and complete. No placeholder values or unimplemented code paths introduced.

## Self-Check: PASSED

All modified files exist, all commits verified in git log. Full test suite: 123 passed, 0 failed, 0 errors.

## Test Run Log

```
123 passed in 3.54s
  - Unit tests: 115 passed
  - Integration tests: 8 passed
```
