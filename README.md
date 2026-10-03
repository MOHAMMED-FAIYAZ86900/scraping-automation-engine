# 🚀 Scraping & Automation Engine

A production-oriented Python web scraping and browser automation demonstration built with **Playwright**, **asyncio**, concurrent workers, isolated browser sessions, retry/backoff handling, proxy-management architecture, anti-bot challenge detection, structured data extraction, and JSON aggregation.

This project was developed as a technical demonstration for a **Scraping & Automation Engineer** role.

---

## 📌 Project Overview

The goal of this project is to demonstrate how a reliable scraping system can be designed rather than building a single sequential scraper.

The engine is designed around several core engineering principles:

* Asynchronous execution
* Controlled concurrency
* Isolated browser sessions
* Browser automation with Playwright
* Proxy-management abstraction
* Retry and exponential backoff
* Anti-bot challenge detection
* Structured data extraction
* Result aggregation
* Duplicate removal
* Execution metrics
* Structured JSON output
* Modular architecture

The demonstration target is:

```text
https://quotes.toscrape.com/js/
```

The application launches multiple concurrent scraping workers and extracts structured quote/author data.

---

# 🎯 Key Features

## 1. Async Scraping

The engine uses Python's `asyncio` framework to execute multiple scraping jobs concurrently.

Instead of processing URLs sequentially:

```text
URL 1 → finish → URL 2 → finish → URL 3
```

the system executes:

```text
             ┌── Worker 1
URL Queue ───┼── Worker 2
             └── Worker 3
```

This allows independent scraping jobs to run concurrently.

---

## 2. Configurable Concurrency

The scraper uses an asyncio semaphore to control the maximum number of active workers.

Current demonstration configuration:

```python
CONCURRENCY = 3
```

This prevents uncontrolled task creation and provides a foundation for scaling the worker pool.

The concurrency limit can be changed without redesigning the scraper.

Example:

```python
CONCURRENCY = 5
```

---

# 🌐 Browser Automation

The project uses **Playwright** for browser-based scraping.

Playwright provides:

* Chromium automation
* Browser contexts
* Page navigation
* HTTP response inspection
* DOM extraction
* Session isolation

The browser is launched through:

```python
create_browser()
```

Each worker creates its own browser context.

---

# 🔐 Session Management

Every scraping worker receives a unique session identifier.

Example:

```text
session-001
session-002
session-003
```

The architecture separates browser contexts between workers.

This provides isolation between independent scraping tasks.

Conceptually:

```text
Worker 1
   |
   └── Session 001
          |
          └── Browser Context

Worker 2
   |
   └── Session 002
          |
          └── Browser Context

Worker 3
   |
   └── Session 003
          |
          └── Browser Context
```

This design can be extended in a production environment to support persistent cookies, authentication sessions, session pools, and other stateful workflows.

---

# 🔄 Proxy Management

The project includes a dedicated `ProxyManager`.

The proxy manager supports:

* Proxy pools
* Round-robin proxy selection
* Environment-variable configuration
* Direct connection fallback

Example configuration:

```text
PROXY_URLS=http://proxy1:8080,http://proxy2:8080
```

The manager rotates through configured proxies.

Example:

```text
Worker 1 → Proxy A
Worker 2 → Proxy B
Worker 3 → Proxy A
Worker 4 → Proxy B
```

### Important

The current demonstration is intentionally run without external proxy servers.

Therefore the current execution log shows:

```text
proxy=direct
```

The proxy-management abstraction is implemented, but this demo does not claim to have performed real external proxy rotation.

---

# 🛡️ Anti-Bot Challenge Detection

The project includes a dedicated challenge-detection module.

The detector looks for common challenge-page indicators such as:

```text
cloudflare
checking your browser
verify you are human
just a moment
security check
```

The purpose is to prevent the scraper from treating an anti-bot challenge page as valid application data.

The flow is:

```text
Page Load
    |
    v
Challenge Detection
    |
    +------------------+
    |                  |
 Normal             Challenge
    |                  |
    v                  v
Parser             Retry/Failure
    |                  |
    v                  v
JSON             Controlled Error
```

### Security approach

The system detects and handles challenge pages.

It does **not** attempt to bypass or defeat security controls.

This makes challenge handling an explicit reliability condition rather than silently returning incorrect data.

---

# ♻️ Retry & Exponential Backoff

The project includes a reusable retry mechanism.

The retry manager supports:

* Configurable attempts
* Exception handling
* Exponential backoff
* Logging
* Final failure propagation

Current default:

```text
Maximum attempts: 4
```

The delay follows an exponential pattern:

```text
Attempt 1
   |
  1 second
   |
Attempt 2
   |
  2 seconds
   |
Attempt 3
   |
  4 seconds
   |
Attempt 4
```

The implementation prevents a temporary network or browser failure from immediately terminating the entire scraping workflow.

Example log:

```text
[RETRY] attempt=1/4
[RETRY] attempt=1 successful
```

If an operation fails:

```text
[RETRY] attempt=1 failed
[RETRY] backoff=1.0s
[RETRY] attempt=2/4
```

---

# 📊 Structured Data Extraction

The parser extracts structured records from the target page.

Each record contains:

```json
{
  "quote": "Example quote",
  "author": "Example Author"
}
```

The parser is separated from browser management so that scraping logic and data extraction logic remain independently maintainable.

---

# 🧹 Deduplication

Multiple workers can potentially return the same records.

The aggregation layer therefore removes duplicate records.

The current demonstration intentionally executes the same target three times.

Each worker extracts:

```text
10 records
```

Therefore:

```text
3 workers × 10 records = 30 raw records
```

After deduplication:

```text
30 raw records
        ↓
10 unique records
```

This demonstrates an important data-engineering concern when combining results from concurrent workers.

---

# 📦 JSON Output

The final result is stored at:

```text
output/results.json
```

The output contains:

```text
metadata
statistics
jobs
records
```

Example structure:

```json
{
  "metadata": {
    "name": "Mohammed Faiyaz",
    "timestamp": "...",
    "target": "https://quotes.toscrape.com/js/",
    "concurrency": 3
  },
  "statistics": {
    "jobs": 3,
    "successful": 3,
    "failed": 0,
    "raw_records": 30,
    "unique_records": 10,
    "elapsed_seconds": 10.77
  },
  "jobs": [],
  "records": []
}
```

The actual file contains the complete extracted records and job-level information.

---

# 📈 Execution Metrics

The application records several useful metrics:

* Number of jobs
* Successful jobs
* Failed jobs
* Raw records
* Unique records
* Runtime
* HTTP status
* Session ID
* Proxy information
* Worker ID

Example final output:

```text
╔══════════════════════════════════════════════╗
║              SCRAPING COMPLETE               ║
╠══════════════════════════════════════════════╣
║ Jobs              : 3                       ║
║ Successful        : 3                       ║
║ Failed            : 0                       ║
║ Raw records       : 30                      ║
║ Unique records    : 10                      ║
║ Runtime           : 10.77s                  ║
║ JSON              : output\results.json     ║
╚══════════════════════════════════════════════╝
```

---

# 🧱 Project Architecture

```text
scraping-engineer-demo/
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── scraper/
│   │
│   ├── __init__.py
│   │
│   ├── browser.py
│   │
│   ├── challenge.py
│   │
│   ├── parser.py
│   │
│   ├── proxy_manager.py
│   │
│   ├── retry.py
│   │
│   └── scraper.py
│
└── output/
    │
    └── results.json
```

---

# 📁 Module Responsibilities

## `main.py`

Application entry point.

Responsible for:

* Configuration
* Banner
* Job creation
* Starting the scraper
* Aggregating results
* Deduplicating records
* Generating statistics
* Writing JSON output

---

## `scraper/scraper.py`

Core scraping engine.

Responsible for:

* Worker creation
* Concurrency control
* Session management
* Proxy selection
* Playwright execution
* Navigation
* Challenge detection
* Parsing
* Retry integration
* Worker results

---

## `scraper/browser.py`

Browser lifecycle management.

Responsible for:

* Starting Playwright
* Launching Chromium
* Optional proxy configuration
* Returning browser instances

---

## `scraper/parser.py`

Data extraction layer.

Responsible for:

* Finding quote elements
* Extracting quote text
* Extracting author names
* Returning structured Python dictionaries

---

## `scraper/proxy_manager.py`

Proxy abstraction.

Responsible for:

* Loading proxies
* Maintaining proxy pool
* Round-robin selection
* Direct-connection fallback

---

## `scraper/retry.py`

Reliability layer.

Responsible for:

* Retry attempts
* Exception handling
* Exponential backoff
* Retry logging

---

## `scraper/challenge.py`

Anti-bot challenge detection.

Responsible for:

* Detecting challenge-page indicators
* Preventing challenge pages from being parsed as valid data

---

# 🛠️ Technology Stack

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Core programming language |
| asyncio             | Asynchronous concurrency  |
| Playwright          | Browser automation        |
| Chromium            | Browser engine            |
| JSON                | Structured output         |
| Regular Expressions | Challenge detection       |
| Logging             | Runtime observability     |

---

# 💻 Requirements

Recommended environment:

```text
Python 3.11+
Windows / Linux / macOS
```

The project was developed and tested on Windows with a Python virtual environment.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd scraping-engineer-demo
```

---

## 2. Create virtual environment

Windows:

```powershell
python -m venv .venv
```

---

## 3. Activate virtual environment

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. Install Playwright Chromium

```powershell
python -m playwright install chromium
```

---

# ▶️ Running the Application

Run:

```powershell
python main.py
```

The application will:

```text
1. Create scraping jobs
2. Start concurrent workers
3. Create isolated browser sessions
4. Navigate to the target
5. Validate HTTP response
6. Detect challenge pages
7. Extract structured records
8. Retry transient failures
9. Aggregate results
10. Deduplicate records
11. Write JSON output
12. Display execution statistics
```

---

# 🧪 Demonstration Result

A successful demonstration produced:

```text
Jobs              : 3
Successful        : 3
Failed            : 0
Raw records       : 30
Unique records    : 10
Runtime           : 10.77s
```

The workers executed concurrently:

```text
Worker 1 → Session 001 → 10 records
Worker 2 → Session 002 → 10 records
Worker 3 → Session 003 → 10 records
```

The aggregation layer then reduced:

```text
30 raw records
        ↓
10 unique records
```

---

# 🔍 Example Runtime Logs

```text
[ENGINE] starting 3 concurrent jobs

[WORKER-1] session=session-001 proxy=direct
[WORKER-2] session=session-002 proxy=direct
[WORKER-3] session=session-003 proxy=direct

[RETRY] attempt=1/4

[WORKER-1] browser context created
[WORKER-2] browser context created
[WORKER-3] browser context created

[WORKER-1] GET https://quotes.toscrape.com/js/
[WORKER-2] GET https://quotes.toscrape.com/js/
[WORKER-3] GET https://quotes.toscrape.com/js/

[WORKER-1] HTTP status=200
[WORKER-2] HTTP status=200
[WORKER-3] HTTP status=200

[WORKER-1] extracted=10 records
[WORKER-2] extracted=10 records
[WORKER-3] extracted=10 records

[WORKER-1] STATUS=SUCCESS
[WORKER-2] STATUS=SUCCESS
[WORKER-3] STATUS=SUCCESS

[ENGINE] all workers completed
```

---

# 🧠 Engineering Design Decisions

## Why asyncio?

Web scraping is heavily I/O-bound.

Workers spend significant time waiting for:

* network responses
* browser navigation
* page rendering
* DOM availability

Async execution allows other workers to make progress during these waits.

---

## Why Playwright?

Playwright provides browser-level automation capabilities that are useful for modern JavaScript-heavy websites.

It provides:

* Chromium automation
* browser contexts
* page navigation
* DOM interaction
* response inspection
* session isolation

---

## Why separate modules?

The project follows separation of concerns.

For example:

```text
Browser lifecycle
       ≠
Parsing
       ≠
Retry logic
       ≠
Proxy management
       ≠
Challenge detection
```

This makes individual components easier to test, replace, and extend.

---

## Why a semaphore?

Creating unlimited concurrent browser sessions can consume significant:

* CPU
* memory
* network
* browser resources

The semaphore provides a controlled concurrency boundary.

---

## Why exponential backoff?

Immediate repeated requests after a transient failure can make reliability worse.

Exponential backoff creates increasing delays:

```text
1s → 2s → 4s → ...
```

This gives temporary failures time to recover while limiting aggressive retry behavior.

---

# 🔐 Responsible Scraping

This project is designed as an engineering demonstration.

When deploying a scraper against a real website, the implementation should consider:

* Terms of service
* robots.txt where applicable
* applicable laws and regulations
* authentication requirements
* rate limits
* server load
* privacy requirements
* data licensing
* access permissions

The anti-bot component in this project is a **challenge detector**, not a security-bypass mechanism.

---

# 🚀 Production Scaling

The current project is intentionally compact enough for a technical demonstration.

A production deployment could extend the architecture to:

```text
                    API / Scheduler
                          |
                          v
                    Task Queue
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
           Worker      Worker      Worker
              |           |           |
              +-----------+-----------+
                          |
                    Proxy Pool
                          |
                    Browser Pool
                          |
                    Data Pipeline
                          |
              +-----------+-----------+
              |                       |
              v                       v
          PostgreSQL              Object Storage
              |
              v
          Analytics
```

Potential production technologies include:

* Redis
* PostgreSQL
* Docker
* Kubernetes
* Prometheus
* Grafana
* centralized logging
* distributed task queues
* cloud browser infrastructure

These are architectural extension points rather than components required by the current demo.

---

# 📌 Future Improvements

Possible future improvements include:

### Infrastructure

* Docker containerization
* Redis task queue
* distributed workers
* cloud deployment
* Kubernetes orchestration

### Observability

* Prometheus metrics
* Grafana dashboards
* structured JSON logging
* centralized log aggregation

### Data

* PostgreSQL storage
* schema validation
* data quality checks
* incremental updates
* deduplication based on persistent identifiers

### Scraping

* configurable rate limiting
* per-domain concurrency limits
* configurable timeout policies
* persistent session management
* proxy health monitoring
* proxy failure tracking

### Testing

* unit tests
* parser tests
* retry tests
* challenge-detection tests
* integration tests
* browser automation tests

---

# 🧪 Example Testing Strategy

A production test suite could include:

```text
tests/
│
├── test_parser.py
├── test_retry.py
├── test_proxy_manager.py
├── test_challenge.py
└── test_scraper.py
```

Example test cases:

```text
✓ Parse valid quote
✓ Handle missing author
✓ Retry transient exception
✓ Stop after maximum retries
✓ Rotate configured proxies
✓ Detect challenge page
✓ Ignore normal page
✓ Deduplicate records
✓ Handle failed worker
```

---

# 🔒 Environment Variables

Proxy configuration can be provided through:

```text
PROXY_URLS
```

Example:

```powershell
$env:PROXY_URLS="http://proxy1:8080,http://proxy2:8080"
```

Do not commit credentials or private proxy URLs to GitHub.

Use:

```text
.env
```

or environment-level secrets for sensitive configuration.

---

# 📄 Git Ignore

Recommended `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.playwright/
output/*.json
```

This prevents:

* virtual environments
* Python cache files
* credentials
* generated output
* local Playwright artifacts

from being committed accidentally.

---

# 🎥 Technical Demonstration

The project can be demonstrated through a short screen recording.

Recommended demonstration sequence:

```text
1. Show project structure
2. Explain architecture
3. Run python main.py
4. Show concurrent workers
5. Show isolated session IDs
6. Show browser context creation
7. Show HTTP status
8. Show extracted records
9. Show retry framework
10. Show challenge detection
11. Open results.json
12. Explain deduplication
13. Show final statistics
14. Explain production scaling
```

---

# 👨‍💻 Author

**Mohammed Faiyaz**

AI/ML Engineer | Python | Generative AI | LLM Applications | Automation

---

# 📜 Disclaimer

This repository is a technical demonstration of scraping and browser-automation architecture.

The included target is used for demonstration purposes.

When adapting the system for real-world websites, users should respect applicable laws, website terms, access policies, rate limits, privacy requirements, and other relevant restrictions.

The project implements anti-bot **detection and controlled failure handling**, not circumvention of website security mechanisms.

---

# ⭐ Summary

This project demonstrates a modular asynchronous scraping architecture with:

```text
                ┌─────────────────────┐
                │     URL QUEUE       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ ASYNC CONCURRENCY   │
                └──────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Worker 1       Worker 2      Worker 3
             │             │             │
             ▼             ▼             ▼
         Session 1      Session 2     Session 3
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                    PLAYWRIGHT
                           │
                           ▼
                 CHALLENGE DETECTION
                      /         \
                     /           \
                    ▼             ▼
                PARSER        RETRY/BACKOFF
                    │
                    ▼
              STRUCTURED DATA
                    │
                    ▼
               DEDUPLICATION
                    │
                    ▼
                 JSON OUTPUT
```

The current successful demonstration executes **3 concurrent jobs**, produces **30 raw records**, reduces them to **10 unique records**, and writes the resulting structured dataset to `output/results.json`.
