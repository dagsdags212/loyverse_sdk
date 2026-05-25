---
phase: 01-code-cleanup-bugfixes
plan: 02
subsystem: models, endpoints
tags: [pydantic, bugfix, tax-model, merchant-endpoint]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Dead code removal (utils.py, schemas.py, shift.py, logging.py)"
provides:
  - "Tax model with single name field preserving max_length=40 constraint"
  - "MerchantEndpoint with parameterless retrieve() calling GET /merchant directly"
affects: [future testing, loyverse-api-usage]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Singleton endpoint pattern: retrieve() without id, using _get(self.path) directly"

key-files:
  modified:
    - src/loyverse_sdk/models/tax.py
    - src/loyverse_sdk/endpoints/merchant.py

key-decisions:
  - "Preserved RetrieveMixin inheritance on MerchantEndpoint for interface consistency despite no longer calling super().retrieve()"
  - "Used direct _get(self.path) + model_validate pattern mirroring ListMixin.list() approach"

patterns-established:
  - "Singleton resource endpoints: override retrieve() to be parameterless and call _get(self.path) directly"

requirements-completed: [BUG-01, BUG-02]

# Metrics
duration: 2min
completed: 2026-05-25
---

# Phase 01 Plan 02: Tax Model and Merchant Endpoint Bugfixes Summary

**Removed duplicate `name` field from Tax model preserving `max_length=40` constraint; corrected `MerchantEndpoint.retrieve()` from a broken `GET /merchant/{id}` to proper singleton `GET /merchant`.**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-05-25T11:37:00Z
- **Completed:** 2026-05-25T11:38:58Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Tax model now has a single `name: str = Field(max_length=40)` — the duplicate `name: str` (which silently overwrote the constrained field) has been removed
- MerchantEndpoint.retrieve() is now parameterless, correctly calling `GET /merchant` (the singleton endpoint) instead of the broken `GET /merchant/{id}`

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix Tax model — remove duplicate name field** - `e78278d` (fix)
2. **Task 2: Fix MerchantEndpoint.retrieve — remove id parameter** - `ee5f5e3` (fix)

## Files Modified
- `src/loyverse_sdk/models/tax.py` — Removed duplicate `name: str` (line 10) that overwrote `name: str = Field(max_length=40)` (line 8), preserving the max-length constraint. Line count reduced from 16 to 15.
- `src/loyverse_sdk/endpoints/merchant.py` — Changed `retrieve(self, id: str)` to `retrieve(self)`, replacing `super().retrieve(id, model=Merchant)` with direct `self._get(self.path)` + `Merchant.model_validate(data)` to correctly target the singleton `/merchant` resource.

## Decisions Made
- **RetrieveMixin kept on MerchantEndpoint**: Although `super().retrieve()` is no longer called, `RetrieveMixin` inheritance was preserved for interface consistency — other code may check `isinstance(endpoint, RetrieveMixin)`. This is harmless and avoids cascading import changes.
- **Direct `_get` + `model_validate` pattern**: Follows the same pattern used by `ListMixin.list()` (which calls `self._get(self.path, params=...)` then `model.model_validate(data)`), providing consistency with existing codebase patterns.

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered
- **Test collection errors (12 errors) are pre-existing**: `uv run pytest --collect-only` shows 12 collection errors from test files using incorrect import paths (`loyverse_api` instead of `loyverse_sdk`). These are not caused by this plan's changes (which only touched `tax.py` and `merchant.py`) and are expected to be resolved in a downstream testing plan.
- **Note on requirement IDs**: The plan frontmatter references `BUG-01` and `BUG-02`, but the bugs actually fixed correspond to `BUG-03` (Tax duplicate field) and `BUG-04` (Merchant endpoint) in PROJECT.md. Frontmatter IDs used as-is for requirement tracking.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- Both model-layer and endpoint-layer bugs fixed — ready for Plan 01-03 (remaining cleanup items)
- No blockers or concerns

---
*Phase: 01-code-cleanup-bugfixes*
*Completed: 2026-05-25*
