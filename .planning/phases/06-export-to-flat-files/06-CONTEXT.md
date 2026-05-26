# Phase 06: Export to Flat Files (CSV + Parquet) — Context

**Gathered:** 2026-05-27
**Status:** Ready for planning
**Source:** Direct user requirements

<domain>
## Phase Boundary

This phase adds flat-file export capabilities to the Loyverse SDK. Users can retrieve data from any Loyverse API endpoint (e.g., customers, receipts, items) and save results to CSV or Parquet files locally.

**What this phase delivers:**
- A reusable export module that converts Loyverse API data to CSV files
- A reusable export module that converts Loyverse API data to Parquet files
- Integration with existing endpoint classes so users can filter/query data first, then export
- Example usage demonstrating query → export workflows

**What this phase does NOT deliver:**
- Compression formats beyond Parquet's built-in compression (no gzip/bzip2 wrappers)
- Streaming incremental exports — batch export only
- Format conversion between CSV and Parquet
</domain>

<decisions>
## Implementation Decisions

### D-01: Polars as the serialization engine
The SDK already depends on Polars 1.36.1 for DuckDB batch inserts. Use Polars `write_csv()` and `write_parquet()` methods for file export. This avoids adding new dependencies and leverages an existing, proven library.

### D-02: Export module location
Create `src/loyverse_sdk/exporters/` package (new top-level module alongside `db/`, `endpoints/`, `models/`). The export concern is distinct from the DuckDB warehousing concern — it operates on in-memory data, not database tables.

### D-03: Export API surface
The primary API should accept a list of Pydantic model instances (the typed response models already returned by endpoint methods) and serialize them. Both a class-based API (`FlatFileExporter`) and convenience module-level functions should be available.

### D-04: CSV format
Standard CSV with headers. Use Polars default settings: comma delimiter, double-quote quoting for fields containing special characters, UTF-8 encoding.

### D-05: Parquet format
Standard Parquet with snappy compression (Polars default). This provides a good balance of file size and read performance.

### D-06: Integration pattern
Users should be able to:
1. Query data using existing endpoint methods (list, iter_all, or filtered queries)
2. Pass the resulting Pydantic model list to the exporter
3. Get a file path back

Example workflow (per user request):
```python
# Query customers onboarded between January and February 2026
customers = await client.customers.list(updated_since="2026-01-01T00:00:00Z")
# Filter client-side for created_at range
jan_feb_customers = [c for c in customers.items 
                     if c.created_at and "2026-01" <= c.created_at.isoformat()[:7] <= "2026-02"]
# Save to CSV
from loyverse_sdk.exporters import export_to_csv
export_to_csv(jan_feb_customers, "customers_jan_feb_2026.csv")
```

### the agent's Discretion
- Exact class/method names in the exporters module
- Whether to provide async variants (file I/O is typically sync; Polars write methods are sync)
- Error handling strategy for file write failures
- Whether to add a convenience method on `LoyverseClient` (like `export_to_duckdb()` pattern) or keep exporters standalone
</decisions>

<canonical_refs>
## Canonical References

### Existing codebase patterns
- `src/loyverse_sdk/db/exporter.py` — DuckDBExporter class pattern: orchestration, error handling, batch processing
- `src/loyverse_sdk/db/converters.py` — Pydantic-to-dict transformation (pydantic_to_sql_dict reusable)
- `src/loyverse_sdk/endpoints/mixins.py` — PaginationMixin.iter_all() async generator for streaming all pages
- `src/loyverse_sdk/client.py` — LoyverseClient facade, endpoint access pattern, lazy import pattern
- `examples/duckdb_export.py` — Existing example script structure to model new examples after

### Existing dependencies available
- Polars 1.36.1 (already in pyproject.toml and uv.lock)
- pyarrow >=15.0.0 (already added in Phase 05)

### No external specs — requirements fully captured in decisions above
</canonical_refs>

<specifics>
## Specific Ideas

1. **CSV export** — Primary format requested. Should handle all 14 resource types without modification.
2. **Parquet export** — Secondary format. Better for large datasets, preserves types, columnar storage.
3. **Date-range filtering + export** — The motivating use case is: query customers in a date range, export to CSV. This means the exporter must work with the existing `list()` and `iter_all()` pattern, not introduce a new query mechanism.
4. **File naming** — Users provide the output path; no auto-naming convention needed.
</specifics>

<deferred>
## Deferred Ideas

- Incremental/streaming export (append to existing file) — could be a future enhancement
- Format conversion (CSV → Parquet and vice versa) — out of scope
- Remote upload (S3, GCS) — out of scope
- Excel (.xlsx) export — out of scope
- JSON/JSONL export — not requested, but could be a natural extension

</deferred>

---

*Phase: 06-export-to-flat-files*
*Context gathered: 2026-05-27 from direct user requirements*
