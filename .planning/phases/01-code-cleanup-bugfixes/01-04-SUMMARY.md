---
plan: 01-04
phase: 01-code-cleanup-bugfixes
status: complete
wave: 3
gaps_closed: [CR-01, CR-02, CR-03, WR-02]
commit: 4895482
---

# Plan 01-04: Gap-Closure Fixes for CR-01, CR-02, CR-03, WR-02

## What Was Built

Closed all four exception-handling gaps identified during the phase-01 human UAT review.
All changes are surgical one-to-three line edits to existing `except` clauses — no new
methods, no new classes, no architectural changes.

| Gap | File | Line | Change |
|-----|------|------|--------|
| CR-01 | `exporter.py` | 151 | Broadened `except ExportError` → `except (ExportError, duckdb.Error)` in `export_all` loop; wraps raw `duckdb.Error` into `ExportError` before re-raise |
| CR-02 | `exporter.py` | 322 | Broadened `except ExportError` → `except (ExportError, duckdb.Error)` in `_batch_insert`; wraps raw `duckdb.Error` into `ExportError` with `resource_name` before re-raise |
| CR-03 | `exporter.py` | 270 | Broadened `except ExportError` → `except Exception` in `_export_merchant`; non-`ExportError` exceptions wrapped into `ExportError("Failed to export merchant: ...", "merchant")` |
| WR-02 | `connection.py` | 120 | Narrowed bare `except Exception` → `except (duckdb.Error, ExportError)` in `transaction()` rollback handler; unrelated exceptions (e.g. `KeyError`, `ValueError`) now propagate directly without triggering rollback |

## Tasks Completed

| # | Task | Commit |
|---|------|--------|
| 1+2 | Broaden exporter catches (CR-01/CR-02/CR-03) + narrow connection rollback (WR-02) | 4895482 |

Both edits were committed in a single atomic commit because CR-01/02/03 and WR-02 are
tightly coupled — WR-02 narrows the rollback handler that the broadened exporter catches
now properly feed into.

## Key Files Modified

- `src/loyverse_sdk/db/exporter.py` — 3 `except` clauses updated (lines 151, 270, 322)
- `src/loyverse_sdk/db/connection.py` — 1 `except` clause narrowed (line 120) + `ExportError` import added

## Deviations

None. The plan was followed exactly. Executor agent spawned in Wave 3 worked on wrong
files (receipts.py/webhooks.py) and its worktree commits were lost; edits were applied
inline by the orchestrator to the correct target files.

## Test Results

- Pre-existing failures: 14 (pyarrow missing, loyverse_api module, unrelated to this plan)
- New failures introduced by this plan: **0**
- Gap-site checks: all 4 passed ✓

## Self-Check: PASSED

Gap-site verification:
1. `grep "except (ExportError, duckdb.Error)" exporter.py` → 2 matches (lines 151, 322) ✓
2. `grep "except Exception" exporter.py` → 1 match (line 270, CR-03 _export_merchant) ✓
3. `grep "except (duckdb.Error, ExportError)" connection.py` → 1 match (line 120) ✓
4. `grep "except Exception" connection.py` → 0 matches ✓
