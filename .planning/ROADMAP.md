# Loyverse Data Toolkit — Roadmap

**Project:** Async Python SDK for Loyverse POS API with DuckDB warehousing
**Started:** 2026-05-25
**Current Milestone:** v1.1 Expansion

---

## Phase Summary

| Phase | Name | Status | Plans | Tasks | Summary |
|-------|------|--------|-------|-------|---------|
| 01 | Code Cleanup & Bugfixes | ✅ COMPLETE | 4 | — | Dead code removed, bugs fixed, bare exceptions replaced |
| 02 | Test Fixes & Verification | ✅ COMPLETE | 1 | 3 | 8 test files fixed, all 25 model tests pass |
| 03 | Cover Missing Loyverse API Endpoints (Inventory) | ✅ COMPLETE | 2 | 6 | Inventory model/DDL/endpoint fixed, exporter integrated, 139 tests |
| 04 | Services Layer with CRUD Business Logic | 🔄 IN PROGRESS | 0+ | — | Business logic layer for Loyverse records |
| 05 | Test Suite Optimization | ✅ COMPLETE | 1 | 3 | 123 tests pass, pyarrow added, non-essential tests pruned |
| 06 | Export to Flat Files (CSV + Parquet) | ⚪ PLANNED | 2 | 0 | Exporters package: CSV + Parquet via Polars, client integration |

---

## Phase 01: Code Cleanup & Bugfixes ✅

**Status:** COMPLETE — Shipped 2026-05-25
**Artifacts:** CONTEXT.md, DISCUSSION-LOG.md, PATTERNS.md, 4 PLANS + SUMMARIES, REVIEW.md, HUMAN-UAT.md, VERIFICATION.md

Delivered:
- Removed 3 orphaned files (`shift.py`, `schemas.py`, `logging.py`) and 2 dead functions from `utils.py`
- Fixed Tax model duplicate `name` field (preserved `max_length=40`)
- Fixed `MerchantEndpoint.retrieve()` from broken `GET /merchant/{id}` to singleton `GET /merchant`
- Replaced 13 bare `except Exception:` blocks with specific types (`ExportError`, `duckdb.Error`, `json.JSONDecodeError`, `pl.exceptions.PolarsError`)

---

## Phase 02: Test Fixes & Verification ✅

**Status:** COMPLETE — Shipped 2026-05-26
**Artifacts:** CONTEXT.md, DISCUSSION-LOG.md, 1 PLAN + SUMMARY, VERIFICATION.md

Delivered:
- Fixed `from loyverse_api.models` → `from loyverse_sdk.models` in all 8 test files
- Fixed `surchage` → `surcharge` typo in receipt model test
- Fixed missing required fields in receipt test payloads (`id`, `item_id`, `variant_id`, `sku`, `cost`, `receipt_date`, `receipt_type`)
- All 25 model tests pass (0 failures, 0 errors)

---

## Phase 03: Cover Missing Loyverse API Endpoints (Inventory) ✅

**Status:** COMPLETE — Shipped 2026-05-26
**Artifacts:** 03-01-PLAN.md, 03-01-SUMMARY.md, 03-02-PLAN.md, 03-02-SUMMARY.md
**Plans:** 2/2 plans complete

**Plans:**
- [x] 03-01-PLAN.md — Fix Inventory model, DDL, and endpoint (Pagination base, schema alignment, filter params)
- [x] 03-02-PLAN.md — Integrate Inventory into Exporter + Add Tests (RESOURCE_ORDER, model tests, endpoint tests)

Delivered:
- InventoryListResponse inherits Pagination (cursor-based pagination works)
- DDL aligned with SQLModel InventoryDB class (variant_id/store_id composite key)
- list() supports store_id/variant_ids filter params; removed broken retrieve()
- Inventory added to RESOURCE_ORDER and converters for DuckDB export
- 139 tests pass (9 new: 1 Pagination + 2 filter forwarding + 6 structural)
- Post-merge FK constraint fixes in junction/child batch_insert tests

---

## Phase 04: Services Layer with CRUD Business Logic 🔄

**Status:** IN PROGRESS
**Artifacts:** 04-03-SUMMARY.md, 04-REVIEW.md, 04-VERIFICATION.md

Scope: Build a services layer that provides CRUD business logic abstractions on top of the raw Loyverse API endpoint wrappers.

---

## Phase 05: Test Suite Optimization ✅

**Status:** COMPLETE — Shipped 2026-05-26
**Artifacts:** CONTEXT.md, 05-01-PLAN.md, 05-01-SUMMARY.md

**Plans:** 1/1 plans complete
- [x] 05-01-PLAN.md — Fix 16 failing tests, prune 9 non-essential tests, verify all pass

Delivered:
- Added `pyarrow>=15.0.0` dependency to fix Polars→Arrow conversion errors
- Fixed connection lifecycle bugs in 4 tests (raw `conn.close()` → `cursor()` context manager)
- Completed test data columns to match DuckDB table schemas
- Fixed merchant mock and exception handling in export mocks
- Pruned 9 non-essential tests (3 DuckDB-internal, 2 duplicate, 4 overly weak)
- Result: 123/123 tests pass (0 failures, 0 errors)

---

## Phase 06: Export to Flat Files (CSV + Parquet) ⚪

**Status:** PLANNED
**Requirements:** EXP-01, EXP-02, EXP-03

Scope: Build flat-file export capabilities that allow users to save Loyverse API data directly to CSV and Parquet files. Leverages Polars (already a dependency) for efficient serialization. Integrates with the existing endpoint classes for filtered data retrieval before export.

**Plans:** 2 plans

Plans:
- [ ] 06-01-PLAN.md — Core Export Module with Unit Tests (FlatFileExporter class, CSV/Parquet export via Polars)
- [ ] 06-02-PLAN.md — Client Integration & Example (LoyverseClient convenience methods, example script)

---

## Requirements Traceability

See `.planning/REQUIREMENTS.md` for detailed requirement-to-phase mapping.

---

*Last updated: 2026-05-26*
*Next action: `/gsd-execute-phase 04` to continue the services layer*
