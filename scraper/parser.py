async def parse_page(page):

    quotes = await page.locator(".quote").all()

    records = []

    for quote in quotes:

        text = await quote.locator(".text").inner_text()

        author = await quote.locator(".author").inner_text()

        records.append({
            "quote": text,
            "author": author,
        })

    return records