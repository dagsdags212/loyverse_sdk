<!-- GSD:project-start source:PROJECT.md -->
## Project

**Loyverse Data Toolkit**

An async Python SDK for the Loyverse POS API with local DuckDB data warehousing. Provides 14 typed endpoint wrappers (categories, customers, receipts, etc.), cursor-based pagination, and a streaming export pipeline into DuckDB for local analytics.

**Core Value:** Data can be reliably pulled from the Loyverse API into local storage for analysis, with correct typing and error handling throughout.

### Constraints

- **Python**: 3.12+ (already enforced via `.python-version`)
- **Dependencies**: Keep minimal; avoid adding new ones for cleanup work
- **Testing**: All existing tests must pass after fixes
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.12 — Entire SDK implementation. Enforced via `.python-version` and `requires-python = ">=3.12"` in `pyproject.toml`.
## Runtime
- CPython 3.12+
- `uv` (lockfile: `uv.lock` present)
- `pyproject.toml` uses `hatchling` as build backend (`pyproject.toml:48-49`)
## Frameworks
- **httpx** 0.28.1 — Async HTTP client for all API communication (`src/loyverse_sdk/client.py:47-49`)
- **Pydantic** 2.12.4 — Data validation via `BaseModel` for all request/response models (`src/loyverse_sdk/models/common.py:1-30`)
- **Pydantic-settings** 2.12.0 — Configuration management via `BaseSettings` with `.env` support (`src/loyverse_sdk/core/config.py:2-15`)
- **DuckDB** 1.4.3 — Embedded OLAP database for local data warehousing/export (`src/loyverse_sdk/db/connection.py:10-152`)
- **Polars** 1.36.1 — DataFrame library used for efficient batch inserts into DuckDB (`src/loyverse_sdk/db/exporter.py:354-358`)
- **SQLModel** 0.0.27 — ORM-style table definitions for DuckDB schema (`src/loyverse_sdk/db/schema_builder.py:9-382`)
- **pytest** 9.0.2 — Test runner (`pyproject.toml:21-22`)
- **pytest-asyncio** 1.3.0 — Async test support
- **pytest-mock** 3.15.1 — Mocking utilities
- **respx** 0.22.0 — HTTP mock for httpx (used to fake API responses)
- **hatchling** — Build backend (`pyproject.toml:48-49`)
- No TypeScript, JS bundlers, Docker, or CI config detected
## Key Dependencies
- `httpx>=0.28.1` — All API calls; core transport layer (`src/loyverse_sdk/client.py:3`)
- `pydantic>=2.12.4` — All models and validation (`src/loyverse_sdk/models/common.py:3`)
- `pydantic-settings>=2.12.0` — Config loading from env/`.env` (`src/loyverse_sdk/core/config.py:1-15`)
- `duckdb>=1.1.0` — Local analytics database for export feature (`src/loyverse_sdk/db/exporter.py:10`)
- `polars>=1.0.0` — DataFrame operations during DuckDB inserts (`src/loyverse_sdk/db/exporter.py:11`)
- `sqlmodel>=0.0.27` — Schema definitions (combines SQLAlchemy + Pydantic) (`src/loyverse_sdk/db/schema_builder.py:9`)
- `rich>=14.2.0` — Console output with colors/logging (`src/loyverse_sdk/core/console.py:1-7`)
- `pytz>=2025.2` — Timezone conversion for datetime fields (`src/loyverse_sdk/models/common.py:4`)
- `python-dotenv` (transitive via pydantic-settings or direct) — `.env` file loading (`src/loyverse_sdk/core/config.py:1`)
## Configuration
- Configuration via `pydantic-settings` `BaseSettings` (`src/loyverse_sdk/core/config.py:8-13`)
- `.env` file support via `load_dotenv()` in `src/loyverse_sdk/core/config.py:5`
- `LOYVERSE_API_TOKEN` — Required env var for API auth (`config.py:10`)
- Default `BASE_URL` = `https://api.loyverse.com/v1.0` (`config.py:9`)
- Default `PAGE_LIMIT` = 250 (`config.py:11`)
- Default `TIMEZONE` = `"Asia/Manila"` (`config.py:12`)
- `pyproject.toml` — Single config file for metadata, dependencies, build system, pytest
## Platform Requirements
- Python 3.12+
- `uv` package manager (or `pip` with `requirements.txt` equivalent)
- Access to the Loyverse API (an API token from a live merchant account)
- No specific deployment target; library is installed via `pip install git+...` or published to PyPI (not yet published)
- DuckDB output is a local `.duckdb` file on the filesystem
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Python source files: `snake_case.py` (e.g., `base.py`, `schema_builder.py`, `receipts.py`)
- Test files: `test_{module}.py` (e.g., `test_receipt_model.py`, `test_exporter.py`)
- Config file: `pyproject.toml`
- PascalCase (e.g., `LoyverseClient`, `DuckDBExporter`, `BadRequestError`, `ReceiptListResponse`)
- Endpoint classes use the pattern `{Resource}Endpoint` (e.g., `CategoriesEndpoint`, `CustomersEndpoint`)
- Mixins use the pattern `{Operation}Mixin` (e.g., `ListMixin`, `CreateMixin`, `PaginationMixin`)
- Database table classes use the pattern `{Resource}DB` (e.g., `CategoryDB`, `ReceiptDB`)
- `snake_case` (e.g., `standardize_datetime_str`, `pydantic_to_sql_dict`, `export_all`)
- Private methods prefixed with underscore (e.g., `_get`, `_post`, `_batch_insert`, `_split_items`)
- Async methods use `async def` with `await` throughout (`client.py:108`, `helpers.py:8`)
- Property accessors use `@property` decorator (e.g., `endpoints` property in `client.py:67`)
- `snake_case` (e.g., `api_token`, `base_url`, `db_path`, `record_dict`)
- Constants in `SCREAMING_SNAKE_CASE` (e.g., `RESOURCE_ORDER` in `exporter.py:41`, `BASE_URL` in `config.py:9`)
- Single uppercase letter for TypeVars (e.g., `T = TypeVar("T")` in `mixins.py:10`, `T = TypeVar("T", bound=BaseModel)` in `base.py:5`)
- `Self` for return type annotations from model validators (e.g., `discount.py:25: -> Self`)
## Code Style
- Use modern `str | None` syntax (PEP 604) everywhere, not `Optional[str]` — e.g., `client.py:40: api_token: str | None = None`
- Many functions still use the legacy `Optional[...]` from `typing` (e.g., `exporter.py:10`, `converters.py:11`) — inconsistent but not incorrect
- Return type annotations used on all public methods; some private methods omit them (e.g., `base.py:15: async def _get(self, path: str, **kwargs)` has no return annotation)
- Pydantic `Field(alias=...)` used for API field name mapping (e.g., `item.py:8: name: str = Field(alias="item_name")`)
- `type` union syntax (`str | None`)
- `Self` from `typing` for return types
- `StrEnum` for string enums (`discount.py:8`)
- `@unique` decorator on enums (`category.py:8`)
- `Generic[T]` for generic mixins (`mixins.py:105`)
- Async/await throughout
- `field_validator`, `model_validator`, `field_serializer` from Pydantic v2
## Import Organization
- One import per line for standard library (`from uuid import uuid4, UUID` is an exception)
- Groups separated by blank lines
- `from ... import (...)` with parentheses and trailing comma for multiple items (`client.py:6-15`)
## Error Handling
- Base: `LoyverseSDKError(Exception)` — in `exceptions.py:12`
- HTTP errors: `APIError(LoyverseSDKError)` → `BadRequestError`, `AuthenticationError`, `ForbiddenError`, `NotFoundError`, `RateLimitError`, `ServerError`
- SDK errors: `ConfigurationError`, `ValidationError`, `PaginationError`, `NetworkError`, `ResourceNotFoundError`, `ExportError`
- Network errors wrap original exception via `original_error` parameter
- Status code mapping via if/elif chain (`client.py:134-151`)
- Each exception class has a fixed `status_code` passed to `super().__init__()`
- Error messages built from payload inspection (dict keys "message", "detail", "error")
- Pydantic validation errors caught and re-raised as SDK `ValidationError` with Rich console log
- `try/finally` pattern for closing exporters after async operations (`client.py:233-245`, `exporter.py:538-541`)
- Used for parameter validation (`helpers.py:57-58: if n < 1: raise ConfigurationError`)
- Used for early returns on empty batches (`exporter.py:289-290: if not batch: return`)
## Logging
- Used sparingly in production code — only for validation errors (`mixins.py:34`)
- Debug logging via `if debug:` guards in helper functions (`helpers.py:90-91, 97-98`)
- Warning messages via `print()` for non-critical failures (`exporter.py:163, 427`)
- No use of Python's `logging` module — `core/logging.py` is a stub: `class Logger: ...`
- No structured logging, no log levels
- Print statements for user-facing progress (`examples/duckdb_export.py:24`)
- Rich formatting not used in examples
## Docstrings
- All public methods in `client.py` have full docstrings with Args/Returns/Raises/Example
- Helper functions in `helpers.py` have brief docstrings with Args/Returns/Raises
- Mixins in `mixins.py` have brief one-line docstrings, some have Raises
- Exception classes in `exceptions.py` have verbose module-level docstring and per-class docstrings with attributes
- **Notable gaps:** `BaseEndpoint` methods (`_get`, `_post`, etc.) in `base.py:15-29` have no docstrings. Many endpoint classes have no class-level docstrings.
- Models (`receipt.py`, `item.py`, etc.) have minimal or no docstrings on fields
- Pydantic validators rarely have docstrings
- Present in some modules (`exceptions.py`, `exporter.py`, `converters.py`, `db/__init__.py`, `schema_builder.py`)
- Absent in most endpoint modules, model modules, and `client.py`
## Function Design
- Most methods are focused and under 30 lines
- `DuckDBExporter` methods are larger (e.g., `export_resource` at 57 lines, `_batch_insert` at 40 lines)
- No functions exceed ~90 lines
- Named parameters with defaults for public API methods (e.g., `client.py:168-178`)
- `**kwargs` used to forward parameters to underlying methods (`mixins.py:24`)
- Keyword-only arguments: some helpers use `*,` separator (`helpers.py:10: *, debug: bool = False`)
- `Optional[type]` for parameters that can be None (inconsistent with `type | None` used in type hints elsewhere)
- Typed dicts (e.g., `dict[str, int]`), Pydantic models, or raw API response dicts
- Consistent return of `dict` from `client.request()` — callers either validate with Pydantic or return raw
- Endpoint methods all async, delegating to `BaseEndpoint._get/_post/_patch/_put/_delete`
- `iter_all()` is an `AsyncGenerator` with `async for` usage pattern
- `DuckDBExporter` initialization is synchronous, export methods are async
## Module Design
- `__all__` defined in top-level `__init__.py` (`__init__.py:4`) — only `LoyverseClient`
- `__all__` defined in `db/__init__.py` for all public db utilities
- `__init__.py` for endpoints re-exports all endpoint classes
- `__init__.py` for models re-exports model and list response classes
- `endpoints/__init__.py` — re-exports all endpoint classes from submodules
- `models/__init__.py` — re-exports all model and list response classes
## Testing Conventions
- `pytest-asyncio` for async test support
- `pytest-mock` for mocking
- `respx` for HTTP request mocking (listed but not used yet)
- `@pytest.mark.unit` — auto-applied via `conftest.py` path-based detection
- `@pytest.mark.integration` — auto-applied via `conftest.py` path-based detection
- `@pytest.mark.asyncio` — manually applied to async tests
- `tests/unit/models/test_receipt_model.py` → `src/loyverse_sdk/models/receipt.py`
- `tests/unit/db/test_converters.py` → `src/loyverse_sdk/db/converters.py`
- `tests/unit/db/test_exporter.py` → `src/loyverse_sdk/db/exporter.py`
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System Overview
```text
```
## Component Responsibilities
| Component | Responsibility | File |
|-----------|----------------|------|
| `LoyverseClient` | HTTP client lifecycle, request dispatch, endpoint access, DuckDB export API | `src/loyverse_sdk/client.py` |
| `Auth` | Bearer token management, header construction | `src/loyverse_sdk/auth.py` |
| `BaseEndpoint` | HTTP verb wrappers (_get, _post, _patch, _put, _delete) | `src/loyverse_sdk/endpoints/base.py` |
| `CrudMixin` | Composed CRUD (Create+Retrieve+Update+Delete) | `src/loyverse_sdk/endpoints/mixins.py` |
| `PaginationMixin` | Cursor-based pagination, `iter_all()` async generator | `src/loyverse_sdk/endpoints/mixins.py` |
| 14 Endpoint classes | Domain-specific endpoints with typed wrappers | `src/loyverse_sdk/endpoints/*.py` |
| `Base`, `Pagination` | Pydantic base models with timezone conversion, cursor handling | `src/loyverse_sdk/models/common.py` |
| 14 ListResponse models | Paginated API response models with `items` + `next_cursor` | `src/loyverse_sdk/models/*.py` |
| `Config` | Environment-driven settings (pydantic-settings + .env) | `src/loyverse_sdk/core/config.py` |
| Exception hierarchy | 12 exception classes for API errors, network failures, export errors | `src/loyverse_sdk/exceptions.py` |
| `DuckDBExporter` | Orchestrates streaming export of all resources to DuckDB | `src/loyverse_sdk/db/exporter.py` |
| Schema builder | Raw DDL creation for 25 tables (14 main, 8 junction, 2 child, 1 metadata) | `src/loyverse_sdk/db/schema_builder.py` |
| Converters | Pydantic→dict transform, nested data splitting for relational tables | `src/loyverse_sdk/db/converters.py` |
| `DuckDBConnection` | Connection management with transaction context manager | `src/loyverse_sdk/db/connection.py` |
## Pattern Overview
- **Façade pattern**: `LoyverseClient` (`client.py:35`) provides a single entry point that delegates to 14 endpoint objects
- **Mixin composition**: CRUD operations are composed from reusable mixins (`endpoints/mixins.py:200`), mixed into each endpoint class
- **Pydantic v2 for type safety**: All API payloads and responses are validated through Pydantic models with field validators and serializers
- **Async-first**: Uses `httpx.AsyncClient` for non-blocking I/O throughout
- **Late-binding DuckDB export**: The export subsystem (`client.py:230`) imports `DuckDBExporter` lazily — not loaded until `export_to_duckdb()` is called
## Layers
### 1. Client Layer
- **Purpose**: Single entry point for all API interaction
- **Location**: `src/loyverse_sdk/client.py`
- **Contains**: `LoyverseClient` class — HTTP client lifecycle, endpoint instantiation, request routing, error handling
- **Depends on**: `httpx`, `Auth`, `Config`, `exceptions.py`, 14 endpoint classes
- **Used by**: Consumer code, `helpers.py`, `DuckDBExporter`
### 2. Endpoint Layer
- **Purpose**: Business-domain API operations (list, retrieve, create, update, delete, paginate)
- **Location**: `src/loyverse_sdk/endpoints/`
- **Contains**: `BaseEndpoint` HTTP verb wrappers, CRUD mixins, 14 domain endpoint classes
- **Depends on**: `LoyverseClient` (via `self.client` for requests), Pydantic models
- **Used by**: `LoyverseClient`, `DuckDBExporter`
### 3. Model Layer
- **Purpose**: Type-safe request/response data structures
- **Location**: `src/loyverse_sdk/models/`
- **Contains**: 10 model files + `common.py` with base classes
- **Depends on**: `pydantic`, `pytz`
- **Used by**: All endpoint classes, `DuckDBExporter`
### 4. Core Layer
- **Purpose**: Shared infrastructure (config, logging, console)
- **Location**: `src/loyverse_sdk/core/`
- **Contains**: `Config` (pydantic-settings), `Console` (Rich singleton), `Logger` (placeholder)
- **Depends on**: `pydantic-settings`, `python-dotenv`, `rich`
- **Used by**: All layers
### 5. Export Layer (DuckDB)
- **Purpose**: Local data warehousing — stream API data into DuckDB with relational schema
- **Location**: `src/loyverse_sdk/db/`
- **Contains**: `DuckDBExporter`, `DuckDBConnection`, `schema_builder.py`, `converters.py`, `schemas.py`
- **Depends on**: `LoyverseClient`, `duckdb`, `polars`, `sqlmodel`
- **Used by**: Consumer code via `client.export_to_duckdb()`
## Data Flow
### Primary Request Path
### Pagination Flow
### DuckDB Export Flow
- No shared mutable state in the client layer (each `LoyverseClient` owns its own `httpx.AsyncClient`)
- `Config` (`core/config.py:8`) is a module-level singleton (`config = Config()`) — thread-safe for read-only use
- `console` (`core/console.py:4`) is a module-level Rich `Console` singleton — used for debug logging only
- `DuckDBConnection` manages its own connection state per instance; not thread-safe (single-threaded async usage)
## Key Abstractions
- Purpose: Compose reusable CRUD and pagination behavior across 14 domain endpoints
- Files: `src/loyverse_sdk/endpoints/mixins.py` (all 6 mixin classes, lines 13-203)
- Mixins: `ListMixin`, `RetrieveMixin`, `CreateMixin`, `UpdateMixin`, `DeleteMixin`, `PaginationMixin`, `CrudMixin`
- `CrudMixin` = `CreateMixin + RetrieveMixin + UpdateMixin + DeleteMixin` (`mixins.py:200`)
- Purpose: Consistent base with timezone conversion, UUID serialization, and pagination envelope
- Files: `src/loyverse_sdk/models/common.py`
- `Base` model: auto UUID generation, `created_at`/`updated_at`/`deleted_at`, UTC→local tz conversion, UUID→str serializer
- `Pagination` model: `next_cursor` from API's `cursor` field via alias
- Purpose: Map HTTP status codes to typed exceptions with structured payloads
- Files: `src/loyverse_sdk/exceptions.py`
- Root: `LoyverseSDKError` → `APIError` (with status_code, payload, endpoint) → `BadRequestError` (400), `AuthenticationError` (401), `ForbiddenError` (403), `NotFoundError` (404), `RateLimitError` (429), `ServerError` (5xx)
- SDK exceptions: `ConfigurationError`, `ValidationError`, `PaginationError`, `NetworkError`, `ResourceNotFoundError`, `ExportError`
- Purpose: Wraps paginated API responses in a consistent envelope
- Pattern: Each domain has a `ResourceListResponse(Pagination)` model with `items` field aliased to the API JSON key (e.g., `Field(alias="categories")`)
- Example: `CategoryListResponse(Pagination)` (`models/category.py:41`)
## Entry Points
- Location: `src/loyverse_sdk/client.py:35`
- Triggers: Imported from `loyverse_sdk.__init__`, instantiated by consumer
- Responsibilities: Client lifecycle, endpoint access, request dispatch, error mapping, DuckDB export convenience methods
- Location: `src/loyverse_sdk/db/exporter.py:19`
- Triggers: Lazily imported by `LoyverseClient.export_to_duckdb()` or used directly
- Responsibilities: Schema initialization, streaming export of all resources, batch insertion with transaction management, index creation, sync metadata tracking
- Location: `src/loyverse_sdk/db/exporter.py:506`
- Triggers: Imported directly by consumer scripts
- Responsibilities: Convenience function wrapping DuckDBExporter lifecycle
## Export Resource Dependency Order
## Architectural Constraints
- **Async-only**: All I/O is async/await via `httpx`; no synchronous API surface
- **Single-threaded event loop**: No threading or concurrency within the client; designed for `asyncio.run()` or similar
- **Config singleton**: `config = Config()` at module-level (`core/config.py:15`) — loaded once at import time; environment must be set before first import
- **No caching layer**: Every API call goes directly to the Loyverse API; no in-memory or disk caching
- **Lazy DuckDB imports**: `polars`, `duckdb`, `sqlmodel` are only imported when export methods are called, not at package load
## Anti-Patterns
### ValidationError shadowing built-in
### Logger placeholder
### Mixin path coupling
## Error Handling
- HTTP errors: Status code → typed exception via if/elif chain (`client.py:127-151`)
- Network errors: `httpx.TimeoutException` → `NetworkError`, `httpx.ConnectError` → `NetworkError` (`client.py:110-124`)
- Pydantic model validation errors: Caught in mixins, wrapped in SDK `ValidationError` with `validation_errors` and `model_name` (`mixins.py:33-38`)
- Export errors: `DuckDBExporter` wraps all exceptions as `ExportError` with `resource_name` context (`exporter.py:152-154`)
## Cross-Cutting Concerns
## Key File Referencs
| Concern | File | Line(s) |
|---------|------|---------|
| HTTP client creation | `src/loyverse_sdk/client.py` | 47-49 |
| Central request dispatch | `src/loyverse_sdk/client.py` | 86-157 |
| Endpoint instantiation | `src/loyverse_sdk/client.py` | 51-64 |
| Endpoint mixin composition | `src/loyverse_sdk/endpoints/mixins.py` | 200-202 |
| Pagination async generator | `src/loyverse_sdk/endpoints/mixins.py` | 133-197 |
| Base model with tz conversion | `src/loyverse_sdk/models/common.py` | 8-26 |
| DuckDB export orchestration | `src/loyverse_sdk/db/exporter.py` | 83-168 |
| DDL schema creation | `src/loyverse_sdk/db/schema_builder.py` | 385-779 |
| Nested data splitting | `src/loyverse_sdk/db/converters.py` | 70-126 |
| Exception hierarchy | `src/loyverse_sdk/exceptions.py` | 12-312 |
| Config (env-based) | `src/loyverse_sdk/core/config.py` | 8-15 |
| Helper functions | `src/loyverse_sdk/helpers.py` | 8-148 |
| Example export script | `examples/duckdb_export.py` | 1-315 |
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
