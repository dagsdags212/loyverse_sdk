# Phase 2: Test Fixes & Verification - Context

**Gathered:** 2026-05-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix all test import errors (8 unit model test files incorrectly import from `loyverse_api` instead of `loyverse_sdk`), correct the `surchage` typo to `surcharge` in receipt model test, and verify all tests pass with zero failures and zero errors.

</domain>

<decisions>
## Implementation Decisions

### Test Import Fixes
- **D-01:** All 8 unit model test files need `from loyverse_api` → `from loyverse_sdk` in their import statements
- **D-02:** Files affected: `test_category_model.py`, `test_customer_model.py`, `test_employee_model.py`, `test_discount_model.py`, `test_item_model.py`, `test_payment_type_model.py`, `test_receipt_model.py`, `test_pos_device_model.py`

### Receipt Test Typo Fix
- **D-03:** `test_receipt_model.py:140` — change `r.surchage` (typo) to `r.surcharge` (correct field name from receipt model)

### Verification Strategy
- **D-04:** Run `pytest` across all tests and confirm zero failures, zero errors
- **D-05:** Integration tests import from `loyverse_sdk` correctly and don't need changes

### the agent's Discretion
- Exact replacement pattern for imports — straightforward find-and-replace
- Test execution command and any failure analysis during verification

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Source code — test files needing fixes
- `tests/unit/models/test_category_model.py` — line 6: `from loyverse_api.models`
- `tests/unit/models/test_customer_model.py` — line 6: `from loyverse_api.models`
- `tests/unit/models/test_employee_model.py` — line 7: `from loyverse_api.models`
- `tests/unit/models/test_discount_model.py` — lines 7-8: `from loyverse_api.models...`
- `tests/unit/models/test_item_model.py` — line 6: `from loyverse_api.models`
- `tests/unit/models/test_payment_type_model.py` — line 6: `from loyverse_api.models`
- `tests/unit/models/test_receipt_model.py` — line 6: `from loyverse_api.models`, line 140: `surchage`
- `tests/unit/models/test_pos_device_model.py` — line 5: `from loyverse_api.models`

### Source code — receipt model field
- `src/loyverse_sdk/models/receipt.py` — line 84: `surcharge: NonNegativeFloat = 0.0`

### Requirements traceability
- `.planning/REQUIREMENTS.md` — TST-01, TST-02, VER-01

</canonical_refs>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-test-fixes-verification*
*Context gathered: 2026-05-26*
