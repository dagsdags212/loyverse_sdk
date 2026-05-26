---
phase: 06-export-to-flat-files
plan: 02
subsystem: Flat-File Export Client Integration
tags: [export, client, convenience-methods, example]
requires:
  - 06-01 (FlatFileExporter + CSV/Parquet export functions)
provides:
  - export_to_csv() and export_to_parquet() convenience methods on LoyverseClient
  - Example script demonstrating query→filter→export workflow
affects:
  - src/loyverse_sdk/client.py (new methods)
  - tests/unit/exporters/ (integration tests)
  - examples/ (export_flat_files.py)
tech-stack:
  added: []
  patterns: [Lazy import, delegation, try/finally client lifecycle]
key-files:
  created:
    - tests/unit/exporters/test_client_integration.py
    - examples/export_flat_files.py
  modified:
    - src/loyverse_sdk/client.py
decisions: []
metrics:
  duration: "< 5 min"
  completed_date: "2026-05-27"
---

# Phase 6 Plan 2: Client Integration & Example — Summary

**One-liner:** Two synchronous convenience methods (`export_to_csv`, `export_to_parquet`) on `LoyverseClient` with lazy-import delegation and a working example script demonstrating 3 query→filter→export scenarios.

---

## Task Completion

| # | Task | Status | Commit | Files |
|---|------|--------|--------|-------|
| 1 | Add convenience methods to LoyverseClient | ✅ Complete | `26f56a7` | `src/loyverse_sdk/client.py`, `tests/unit/exporters/test_client_integration.py` |
| 2 | Create example script | ✅ Complete | `ce7ac66` | `examples/export_flat_files.py` |

### TDD Gate Compliance

| Gate | Commit | Status |
|------|--------|--------|
| RED | `4822407` | ✅ 4 failing tests (AttributeError — methods didn't exist) |
| GREEN | `26f56a7` | ✅ All 4 tests pass (delegation + end-to-end) |
| REFACTOR | N/A | Not needed — clean implementation on first pass |

---

## What Was Built

### 1. Client Convenience Methods (`src/loyverse_sdk/client.py`)

Two new synchronous methods in the `# FLAT-FILE EXPORT METHODS` section:

- **`def export_to_csv(self, data: Sequence[BaseModel], filepath: str | Path) -> None`** — Lazy-imports `export_csv` from `exporters` and delegates. Full docstring with Args, Returns, Raises, Example.

- **`def export_to_parquet(self, data: Sequence[BaseModel], filepath: str | Path) -> None`** — Lazy-imports `export_parquet` from `exporters` and delegates. Full docstring with Args, Returns, Raises, Example.

Both methods follow the existing `export_to_duckdb()` lazy-import pattern, are synchronous (Polars file I/O is sync), and require no `try/finally` (the exporters package is stateless).

### 2. Integration Tests (`tests/unit/exporters/test_client_integration.py`)

4 tests covering:
- **Delegation (mocked):** `export_to_csv()` calls `exporters.export_csv()` with correct args
- **Delegation (mocked):** `export_to_parquet()` calls `exporters.export_parquet()` with correct args
- **End-to-end CSV:** Real model list → file created with expected headers and content
- **End-to-end Parquet:** Real model list → file created and readable by `pl.read_parquet()`

### 3. Example Script (`examples/export_flat_files.py`)

Demonstrates 3 export scenarios:
1. **Customers by date range → CSV:** Query with `updated_since`, client-side filter for Jan-Feb 2026, export
2. **All items via pagination → Parquet:** `iter_all()` streaming, export full catalog to Parquet
3. **Latest receipts → CSV:** `list(limit=50)`, export page to CSV

Follows existing `examples/duckdb_export.py` conventions: shebang, module docstring, `async def main()`, `try/finally: await client.close()`, `asyncio.run(main())`, API token check, formatted console output.

---

## Deviations from Plan

None — plan executed exactly as written.

---

## Verification

| Check | Result |
|-------|--------|
| `grep "def export_to_csv" client.py` | ✅ Line 349 |
| `grep "def export_to_parquet" client.py` | ✅ Line 392 |
| `grep "from loyverse_sdk.exporters import" client.py` | ✅ 2 matches (lines 388, 426) |
| `ast.parse(export_flat_files.py)` | ✅ Valid Python |
| `grep "export_to_csv\|export_to_parquet" export_flat_files.py` | ✅ 3 matches |
| `grep "asyncio.run(main())" export_flat_files.py` | ✅ Line 111 |
| `pytest test_client_integration.py` | ✅ 4/4 passed |
| `pytest test_exporter.py` (existing) | ✅ 17/17 passed |

---

## Known Stubs

None. All methods are fully wired to the `exporters` package (built in plan 06-01). The example script uses real API calls.

---

## Threat Flags

None. All threats covered by plan's threat model (T-06-04 delegates to T-06-01 coverage, T-06-05 uses env-based auth as standard). No new trust boundaries introduced.

---

## Self-Check: PASSED

- [x] `tests/unit/exporters/test_client_integration.py` exists and has 4 passing tests
- [x] `examples/export_flat_files.py` exists and passes `ast.parse`
- [x] `src/loyverse_sdk/client.py` has `export_to_csv` and `export_to_parquet` methods
- [x] All acceptance criteria verified via grep/pytest
- [x] 3 commits on branch: `4822407` (RED), `26f56a7` (GREEN), `ce7ac66` (example script)
