# Scraping & Automation Engineer Demo

A portfolio-style Python + Playwright demonstration of reliable browser automation, bounded async concurrency, isolated browser sessions, proxy abstraction, challenge detection, retries/backoff, and structured JSON output.

## Safety / authorization
This project is intended for websites and environments where you have permission to automate. It **does not bypass Cloudflare or other access controls**. If an access challenge is detected, the scraper records the event, backs off, retries according to policy, and fails gracefully.

## Features
- Python async Playwright
- Bounded concurrency with `asyncio.Semaphore`
- Independent Playwright BrowserContexts for session isolation
- Optional authorized proxy rotation abstraction
- Exponential backoff with jitter
- Challenge/access-control detection
- Structured JSON output
- Logging and error handling
- Configuration through `.env`

Playwright supports async Python APIs, independent browser contexts, and proxy configuration per browser context. See the official docs: https://playwright.dev/python/docs/library and https://playwright.dev/python/docs/api/class-browsercontext

## Windows setup
Open PowerShell in this directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

## Run

```powershell
copy .env.example .env
python main.py
```

A browser window will open because `HEADLESS=false`. The program launches six concurrent tasks with a maximum of three active workers, extracts quotes, and writes `output/results.json`.

## Proxy configuration
Only use proxies you are authorized to use. Put comma-separated proxy URLs in `.env`:

```text
PROXY_URLS=http://user:password@proxy1.example:3128,http://user:password@proxy2.example:3128
```

Do not commit `.env` or credentials.

## Demo talking points
1. Playwright provides the browser automation layer.
2. Browser contexts isolate cookies and session state.
3. A semaphore bounds concurrency to protect both the target and local resources.
4. ProxyManager provides a clean abstraction for authorized proxy infrastructure.
5. Challenge detection prevents the system from attempting to circumvent access controls.
6. Retries use exponential backoff and jitter.
7. Results are normalized into JSON for downstream pipelines.

## Suggested production architecture
Scheduler/API -> Queue (Redis/RabbitMQ) -> Worker pool -> Playwright -> Parser -> PostgreSQL/S3 -> Metrics/Logs

For production, add rate limits per domain, deduplication, checkpointing, distributed locks where necessary, structured logs, metrics, alerting, and persistent job state.
