# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-05-26

### Added
- **16 API endpoints**: categories, customers, discounts, devices, employees, inventory, items, merchant, modifiers, receipts, shifts, stores, suppliers, taxes, variants, webhooks
- Async/await interface using httpx for non-blocking API calls
- Pydantic models for type-safe request/response validation
- Cursor-based pagination with `iter_all()` async generator
- Full CRUD operations for all supported endpoints
- DuckDB export pipeline with 15 main tables, 8 junction tables, and 2 child tables
- Streaming export with batch inserts, progress tracking, and UPSERT support
- Timezone-aware datetime conversion (UTC to local via pytz)
- UUID serialization for consistent ID handling across models
- Custom exception hierarchy for error handling

### Fixed
- Inventory endpoint filter parameters (store_id, variant_ids)
- Items and Modifiers endpoints now correctly inherit update mixin
- MerchantEndpoint.retrieve for singleton resource handling
- Tax model duplicate name field removed
- Receipt model surcharge typo corrected
- FK constraint violations in batch insert tests

### Changed
- Default page limit of 250 for API pagination
- Replaced bare `except Exception` blocks with specific exception types

### Removed
- Dead code: convert_response, use_model utils, db/schemas.py, core/logging.py
- Orphaned models and duplicate test files

## [0.0.0] - 2025-02-14

### Added
- Initial project setup with LoyverseClient class
- Auth class for API token handling
- Config class with environment variable support
- Custom exceptions for API and SDK errors
