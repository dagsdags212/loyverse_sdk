# Roadmap: Loyverse Data Toolkit

## Milestones

- ✅ **v1.0 Initial Cleanup** — Phases 1-2 (shipped 2026-05-25)

## Phases

<details>
<summary>✅ v1.0 Initial Cleanup (Phases 1-2) — SHIPPED 2026-05-25</summary>

- [x] Phase 1: Code Cleanup & Bugfixes (4/4 plans) — completed 2026-05-25
- [x] Phase 2: Test Fixes & Verification (1/1 plan) — completed 2026-05-25

</details>

### Phase 3: Cover missing Loyverse API endpoints (inventory)

**Goal:** Audit all 16 Loyverse API endpoints, implement missing data models and endpoint classes, identify supported CRUD operations, and register new endpoints to the main client.
**Requirements**: COMPLETE-SDK
**Depends on:** Phase 2
**Plans**: 3 plans

Plans:
- [x] 03-01-PLAN.md — Audit all endpoints, implement missing inventory + shifts, register in client, update DuckDB schema
- [x] 03-02-PLAN.md — Fix Inventory model to match API (variant_id, store_id, in_stock, updated_at)
- [x] 03-03-PLAN.md — Fix Shift model to match API (store_id, pos_device_id, cash_payments, nested arrays)

### Phase 4: Services layer with CRUD business logic for Loyverse records

**Goal:** Add optional services layer on top of CRUD endpoints — BaseService ABC, ItemsService (with validation + optimistic locking), CustomersService (with email validation + retrieve_by_email), DiscountsService, CategoriesService, TaxesService.
**Requirements**: TBD
**Depends on:** Phase 3
**Plans:** 3 plans

Plans:
- [x] 04-01-PLAN.md — Services infrastructure: BaseService, services module, ItemsService with validation + optimistic locking
- [x] 04-02-PLAN.md — CustomersService with email validation and retrieve_by_email
- [x] 04-03-PLAN.md — DiscountsService, CategoriesService, TaxesService + unit tests

---

*For full milestone details, see `.planning/milestones/v1.0-ROADMAP.md`*