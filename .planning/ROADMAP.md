# Loyverse Data Toolkit — Roadmap

**Project:** Async Python SDK for Loyverse POS API with DuckDB warehousing
**Started:** 2026-05-25
**Current Milestone:** v1.0 Initial Cleanup → v1.1 Expansion

---

## Phase Summary

| Phase | Name | Status | Plans | Tasks | Summary |
|-------|------|--------|-------|-------|---------|
| 01 | Code Cleanup & Bugfixes | ✅ COMPLETE | 4 | — | Dead code removed, bugs fixed, bare exceptions replaced |
| 02 | Test Fixes & Verification | ✅ COMPLETE | 1 | 3 | 8 test files fixed, all 25 model tests pass |
| 03 | Cover Missing Loyverse API Endpoints (Inventory) | 📋 PLANNED | 0 | 0 | Add inventory endpoint coverage to SDK |
| 04 | Services Layer with CRUD Business Logic | 🔄 IN PROGRESS | 0+ | — | Business logic layer for Loyverse records |
| 05 | Test Suite Optimization | 📋 PLANNED | 1 | 3 | Fix 16 failing tests, prune non-essential tests, all pass cleanly |

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

## Phase 03: Cover Missing Loyverse API Endpoints (Inventory) 📋

**Status:** PLANNED — Not yet executed
**Artifacts:** None (placeholder)

Scope: Add SDK coverage for inventory-related Loyverse API endpoints not yet implemented.

---

## Phase 04: Services Layer with CRUD Business Logic 🔄

**Status:** IN PROGRESS
**Artifacts:** 04-03-SUMMARY.md, 04-REVIEW.md, 04-VERIFICATION.md

Scope: Build a services layer that provides CRUD business logic abstractions on top of the raw Loyverse API endpoint wrappers.

---

## Phase 05: Test Suite Optimization 📋

**Status:** PLANNED — Ready for execution
**Artifacts:** CONTEXT.md, 05-01-PLAN.md

**Plans:** 1 plan
- [ ] 05-01-PLAN.md — Fix 16 failing tests (pyarrow dependency, connection lifecycle, test data, mocks), prune 8 non-essential tests, verify all pass

Scope: Fix all 16 failing tests (missing pyarrow, connection lifecycle bugs, test data issues, mock problems), then prune non-essential tests (DuckDB-internal, duplicate coverage, overly weak assertions) from ~132 down to ~122 while keeping all SDK-logic coverage intact.

---

## Requirements Traceability

See `.planning/REQUIREMENTS.md` for detailed requirement-to-phase mapping.

---

*Last updated: 2026-05-26*
*Next action: `/gsd-execute-phase 05` to execute the test suite optimization plan*
