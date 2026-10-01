import asyncio
import logging


logger = logging.getLogger(__name__)


async def retry_with_backoff(
    operation,
    max_retries=3,
    base_delay=1.0,
):

    last_exception = None

    total_attempts = max_retries + 1

    for attempt in range(1, total_attempts + 1):

        try:

            logger.info(
                "[RETRY] attempt=%d/%d",
                attempt,
                total_attempts,
            )

            result = await operation()

            logger.info(
                "[RETRY] attempt=%d successful",
                attempt,
            )

            return result

        except Exception as exc:

            last_exception = exc

            logger.warning(
                "[RETRY] attempt=%d failed: %s",
                attempt,
                exc,
            )

            if attempt == total_attempts:

                logger.error(
                    "[RETRY] maximum attempts reached"
                )

                raise last_exception

            delay = base_delay * (
                2 ** (attempt - 1)
            )

            logger.info(
                "[RETRY] backoff=%.1fs",
                delay,
            )

            await asyncio.sleep(delay)

    raise last_exception