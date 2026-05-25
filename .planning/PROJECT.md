# Loyverse Data Toolkit

## What This Is

An async Python SDK for the Loyverse POS API with local DuckDB data warehousing. Provides 14 typed endpoint wrappers (categories, customers, receipts, etc.), cursor-based pagination, and a streaming export pipeline into DuckDB for local analytics.

## Core Value

Data can be reliably pulled from the Loyverse API into local storage for analysis, with correct typing and error handling throughout.

## Requirements

### Validated

- ✓ Async HTTP client with Bearer token auth — existing
- ✓ 14 domain endpoint classes (categories, customers, discounts, employees, items, etc.) — existing
- ✓ Pydantic v2 models with timezone conversion — existing
- ✓ Cursor-based pagination with async generator — existing
- ✓ DuckDB export pipeline with batch inserts — existing
- ✓ Type-safe exception hierarchy mapped to HTTP status codes — existing
- ✓ Config management via pydantic-settings/.env — existing
- ✓ Unit tests for 8 model files — existing

### Active

- [ ] **BUG-01**: Fix test import errors (all 8 files use `loyverse_api` instead of `loyverse_sdk`)
- [ ] **BUG-02**: Fix `surchage` typo → `surcharge` in receipt model test
- [ ] **BUG-03**: Fix duplicate `name` field in Tax model (second overwrites first's `max_length`)
- [ ] **BUG-04**: Fix `MerchantEndpoint.retrieve(id)` — id parameter is never used; constructs wrong URL for singleton resource
- [ ] **CLEAN-01**: Remove orphaned `models/shift.py` (no endpoint, no client integration, no tests)
- [ ] **CLEAN-02**: Remove dead `utils.py` functions (`convert_response`, `use_model`)
- [ ] **CLEAN-03**: Remove dead `db/schemas.py` (unused SQLModel schema, parallel to live raw-SQL schema)
- [ ] **CLEAN-04**: Remove dead `core/logging.py` stub (unused `class Logger`)
- [ ] **CLEAN-05**: Replace 11+ bare `except Exception:` blocks in `db/exporter.py` with specific exception handling
- [ ] **CLEAN-06**: Replace 2 bare `except Exception:` blocks in `client.py` with specific exception handling

### Out of Scope

- Adding new endpoint classes or features — cleanup/bugfix only
- Adding new test coverage for endpoints/client/auth — deferred
- Replacing `pytz` with `zoneinfo` — nice-to-have, not part of cleanup
- Removing `sqlmodel` or `polars` dependencies — risk reduction, not cleanup
- Adding retry/rate-limit logic — new feature, not bugfix
- Replacing `db/schema_builder.py` raw SQL with SQLModel — refactor, not cleanup

## Context

The codebase was built as a client library + export pipeline. The codebase map (.planning/codebase/) identified multiple concrete bugs, dead code in 4 modules, and 11+ bare except blocks. All existing tests have incorrect package imports, meaning they've likely never been run as-is. Fixing these issues and getting tests passing is the priority before any feature work.

## Constraints

- **Python**: 3.12+ (already enforced via `.python-version`)
- **Dependencies**: Keep minimal; avoid adding new ones for cleanup work
- **Testing**: All existing tests must pass after fixes

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Cleanup-first scope | Codebase map revealed concrete bugs and dead code that block reliable development | — Pending |

---

*Last updated: 2026-05-25 after initialization*
