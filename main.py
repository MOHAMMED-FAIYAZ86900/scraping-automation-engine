import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from scraper.scraper import Scraper


NAME = "Mohammed Faiyaz"
TARGET_URL = "https://quotes.toscrape.com/js/"
CONCURRENCY = 3


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)


def banner():
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║     SCRAPING & AUTOMATION ENGINEER DEMO     ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ Name        : {NAME:<29}║")
    print(
        f"║ Date        : "
        f"{datetime.now().strftime('%B %d, %Y'):<29}║"
    )
    print("║ Stack       : Python + Playwright           ║")
    print("║ Async       : asyncio + concurrency          ║")
    print("║ Reliability : retry + backoff                ║")
    print("║ Sessions    : isolated browser contexts      ║")
    print("╚══════════════════════════════════════════════╝")
    print()


async def main():

    banner()

    urls = [TARGET_URL] * CONCURRENCY

    print(f"[QUEUE] {len(urls)} jobs created")
    print(f"[CONFIG] concurrency={CONCURRENCY}")
    print()

    start_time = time.perf_counter()

    scraper = Scraper(
        max_concurrency=CONCURRENCY
    )

    results = await scraper.run(urls)

    elapsed = time.perf_counter() - start_time

    unique_records = {}

    for result in results:
        for record in result.get("records", []):

            key = (
                record.get("quote"),
                record.get("author"),
            )

            unique_records[key] = record

    unique_records = list(unique_records.values())

    successful = sum(
        1
        for result in results
        if result.get("status") == "success"
    )

    failed = len(results) - successful

    total_extracted = sum(
        len(result.get("records", []))
        for result in results
    )

    output = {
        "metadata": {
            "name": NAME,
            "timestamp": datetime.now().isoformat(),
            "target": TARGET_URL,
            "concurrency": CONCURRENCY,
        },
        "statistics": {
            "jobs": len(results),
            "successful": successful,
            "failed": failed,
            "raw_records": total_extracted,
            "unique_records": len(unique_records),
            "elapsed_seconds": round(elapsed, 2),
        },
        "jobs": results,
        "records": unique_records,
    }

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║              SCRAPING COMPLETE               ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ Jobs              : {len(results):<21}║")
    print(f"║ Successful        : {successful:<21}║")
    print(f"║ Failed            : {failed:<21}║")
    print(f"║ Raw records       : {total_extracted:<21}║")
    print(f"║ Unique records    : {len(unique_records):<21}║")
    print(f"║ Runtime           : {elapsed:.2f}s{' ':<16}║")
    print(f"║ JSON              : {str(output_file):<21}║")
    print("╚══════════════════════════════════════════════╝")
    print()


if __name__ == "__main__":
    asyncio.run(main())