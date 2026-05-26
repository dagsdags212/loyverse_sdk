#!/usr/bin/env python3
"""
Example: Export Loyverse data to CSV and Parquet flat files.

This script demonstrates how to query Loyverse API endpoints, filter data
client-side, and export results to CSV or Parquet files using the
convenience methods on LoyverseClient.

Prerequisites:
    - LOYVERSE_API_TOKEN environment variable set
    - Install dependencies: uv sync (or pip install loyverse-sdk)

Usage:
    python examples/export_flat_files.py
"""

import asyncio
import os

from loyverse_sdk import LoyverseClient


async def main():
    """Run all flat-file export scenarios."""
    print("=" * 60)
    print("  Flat-File Export Examples")
    print("=" * 60)

    # Check for API token
    if not os.getenv("LOYVERSE_API_TOKEN"):
        print("\nError: LOYVERSE_API_TOKEN environment variable not set")
        print("\nTo run these examples:")
        print(
            "  1. Get your API token from https://r.loyverse.com/dashboard/settings/api"
        )
        print("  2. Set environment variable: export LOYVERSE_API_TOKEN='your_token'")
        print("  3. Run: python examples/export_flat_files.py")
        return

    client = LoyverseClient()
    try:
        # ------------------------------------------------------------------
        # Scenario 1: Query customers by date range, filter, export to CSV
        # ------------------------------------------------------------------
        print("\n--- Scenario 1: Customers filtered by date → CSV ---\n")

        customers_resp = await client.customers.list(
            updated_since="2026-01-01T00:00:00Z"
        )
        # Filter client-side for customers created in January-February 2026
        jan_feb = [
            c
            for c in customers_resp.items
            if c.created_at
            and c.created_at.year == 2026
            and c.created_at.month in (1, 2)
        ]

        client.export_to_csv(jan_feb, "customers_jan_feb_2026.csv")
        print(f"Exported {len(jan_feb)} customers to CSV")

        # ------------------------------------------------------------------
        # Scenario 2: Export all items using iter_all(), save to Parquet
        # ------------------------------------------------------------------
        print("\n--- Scenario 2: All items via pagination → Parquet ---\n")

        items = []
        async for page in client.items.iter_all(limit=250):
            items.append(page)

        client.export_to_parquet(items, "items_full.parquet")
        print(f"Exported {len(items)} items to Parquet")

        # ------------------------------------------------------------------
        # Scenario 3: Export latest receipts page to CSV
        # ------------------------------------------------------------------
        print("\n--- Scenario 3: Latest receipts → CSV ---\n")

        receipts_resp = await client.receipts.list(limit=50)
        client.export_to_csv(receipts_resp.items, "receipts.csv")
        print(f"Exported {len(receipts_resp.items)} receipts to CSV")

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        print("\n" + "=" * 60)
        print("  All examples completed successfully!")
        print("=" * 60)
        print("\nOutput files:")
        print("  - customers_jan_feb_2026.csv")
        print("  - items_full.parquet")
        print("  - receipts.csv")
        print("\nNext steps:")
        print("  - Open CSV files in Excel, Numbers, or any text editor")
        print(
            "  - Load Parquet files with pandas (pd.read_parquet) or Polars (pl.read_parquet)"
        )
        print("  - Build data pipelines that combine API queries with file export")

    except Exception as e:
        print(f"\nError: {e}")
        print(f"\nType: {type(e).__name__}")
        import traceback

        traceback.print_exc()
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
