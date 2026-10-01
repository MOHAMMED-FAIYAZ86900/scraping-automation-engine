from playwright.async_api import async_playwright


async def create_browser(proxy=None):

    playwright = await async_playwright().start()

    options = {
        "headless": True,
    }

    if proxy:
        options["proxy"] = {
            "server": proxy
        }

    browser = await playwright.chromium.launch(
        **options
    )

    browser._playwright = playwright

    return browser