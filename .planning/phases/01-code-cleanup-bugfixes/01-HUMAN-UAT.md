---
status: complete
phase: 01-code-cleanup-bugfixes
source: [01-VERIFICATION.md]
started: 2026-05-25
updated: 2026-05-25
---

## Current Test

[testing complete]

## Tests

### 1. CR-01: export_all loop catch width — exporter.py:151
expected: Decide whether `except ExportError` is acceptable (plan's D-01 decision) or should be broadened to catch `duckdb.Error`/other exceptions and wrap them in ExportError (reviewer's recommendation).
result: issue
reported: "B (broaden)"
severity: major

### 2. CR-02: _batch_insert catch width — exporter.py:318
expected: Same decision — narrow `except ExportError` vs broader `except (ExportError, duckdb.Error)` as reviewer recommends.
result: issue
reported: "Option B, broaden"
severity: major

### 3. CR-03: _export_merchant catch width — exporter.py:268
expected: Same decision — narrow `except ExportError` vs broader catch that wraps with merchant context.
result: issue
reported: "B"
severity: major

### 4. CR-04: _insert_records_to_table coverage — exporter.py:343-383
expected: Confirm path where `conn.execute()` and `conn.unregister()` outside the Polars try/except are covered by upstream catches, or add a `duckdb.Error` guard.
result: pass

### 5. WR-02: connection.py:118 bare except Exception in transaction rollback
expected: Acknowledge as pre-existing or decide to fix. This `except Exception` in rollback interacts with now-narrower exporter catches.
result: issue
reported: "B — narrow it"
severity: major

## Summary

total: 5
passed: 1
issues: 4
pending: 0
skipped: 0
blocked: 0

## Gaps

- truth: "export_all loop at exporter.py:151 should catch duckdb.Error and wrap in ExportError with resource_name context"
  status: failed
  reason: "User decided: B (broaden) — current narrow `except ExportError` is insufficient"
  severity: major
  test: 1
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

- truth: "_batch_insert at exporter.py:318 should catch duckdb.Error (from transaction begin/commit) and wrap in ExportError with resource_name context"
  status: failed
  reason: "User decided: B (broaden) — duckdb.Error from transaction bookends bypasses current narrow catch"
  severity: major
  test: 2
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

- truth: "_export_merchant at exporter.py:268 should catch duckdb.Error and httpx/API errors and wrap with ExportError('merchant') context"
  status: failed
  reason: "User decided: B (broaden) — httpx and duckdb errors bypass current narrow ExportError catch"
  severity: major
  test: 3
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

- truth: "connection.py:118 bare `except Exception` in transaction() rollback should be narrowed to specific types (e.g. duckdb.Error, ExportError)"
  status: failed
  reason: "User decided: B (narrow) — bare except Exception is inconsistent with project-wide exception tightening"
  severity: major
  test: 5
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""
