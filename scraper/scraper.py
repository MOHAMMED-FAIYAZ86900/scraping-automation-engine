import asyncio
import logging
import time

from scraper.browser import create_browser
from scraper.challenge import detect_challenge
from scraper.parser import parse_page
from scraper.proxy_manager import ProxyManager
from scraper.retry import retry_with_backoff


logger = logging.getLogger(__name__)


class Scraper:

    def __init__(
        self,
        max_concurrency=3,
    ):

        self.max_concurrency = max_concurrency

        self.semaphore = asyncio.Semaphore(
            max_concurrency
        )

        self.proxy_manager = ProxyManager()

    async def scrape_one(
        self,
        url,
        worker_id,
    ):

        async with self.semaphore:

            proxy = self.proxy_manager.next_proxy()

            session_id = (
                f"session-{worker_id:03d}"
            )

            logger.info(
                "[WORKER-%d] session=%s proxy=%s",
                worker_id,
                session_id,
                proxy or "direct",
            )

            async def operation():

                start = time.perf_counter()

                browser = await create_browser(
                    proxy
                )

                try:

                    context = await browser.new_context()

                    logger.info(
                        "[WORKER-%d] browser context created",
                        worker_id,
                    )

                    page = await context.new_page()

                    logger.info(
                        "[WORKER-%d] GET %s",
                        worker_id,
                        url,
                    )

                    response = await page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )

                    status_code = (
                        response.status
                        if response
                        else None
                    )

                    logger.info(
                        "[WORKER-%d] HTTP status=%s",
                        worker_id,
                        status_code,
                    )

                    title = await page.title()

                    body = await page.locator(
                        "body"
                    ).inner_text()

                    if detect_challenge(
                        title=title,
                        content=body,
                    ):

                        logger.warning(
                            "[WORKER-%d] anti-bot challenge detected",
                            worker_id,
                        )

                        raise RuntimeError(
                            "Anti-bot challenge detected"
                        )

                    records = await parse_page(
                        page
                    )

                    elapsed = (
                        time.perf_counter()
                        - start
                    )

                    logger.info(
                        "[WORKER-%d] extracted=%d records runtime=%.2fs",
                        worker_id,
                        len(records),
                        elapsed,
                    )

                    return {
                        "url": url,
                        "status": "success",
                        "session": session_id,
                        "proxy": proxy or "direct",
                        "http_status": status_code,
                        "records": records,
                        "runtime_seconds": round(
                            elapsed,
                            2,
                        ),
                    }

                finally:

                    await browser.close()

                    if hasattr(
                        browser,
                        "_playwright",
                    ):

                        await browser._playwright.stop()

                    logger.info(
                        "[WORKER-%d] browser closed",
                        worker_id,
                    )

            try:

                result = await retry_with_backoff(
                    operation
                )

                logger.info(
                    "[WORKER-%d] STATUS=SUCCESS",
                    worker_id,
                )

                return result

            except Exception as exc:

                logger.error(
                    "[WORKER-%d] STATUS=FAILED error=%s",
                    worker_id,
                    exc,
                )

                return {
                    "url": url,
                    "status": "failed",
                    "session": session_id,
                    "proxy": proxy or "direct",
                    "records": [],
                    "error": str(exc),
                }

    async def run(
        self,
        urls,
    ):

        logger.info(
            "[ENGINE] starting %d concurrent jobs",
            len(urls),
        )

        tasks = [
            self.scrape_one(
                url=url,
                worker_id=worker_id,
            )
            for worker_id, url
            in enumerate(
                urls,
                start=1,
            )
        ]

        results = await asyncio.gather(
            *tasks
        )

        logger.info(
            "[ENGINE] all workers completed"
        )

        return results