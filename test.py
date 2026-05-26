import asyncio
from loyverse_sdk import LoyverseClient


async def main() -> None:
    client = LoyverseClient()

    record_counts = {}
    for epname, endpoint in client.endpoints.items():
        print(f"Fetching records from {epname} endpoint...")
        try:
            async for record in endpoint.iter_all():
                if epname in record_counts:
                    record_counts[epname] += 1
                else:
                    record_counts[epname] = 1
        except AttributeError:
            print(f"No iter_all() method for {epname} endpoint, skipping")
            continue

    print(record_counts)


if __name__ == "__main__":
    asyncio.run(main())
