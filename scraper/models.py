from dataclasses import dataclass

@dataclass
class ScrapeResult:
    url: str
    status: str
    title: str | None = None
    author: str | None = None
    error: str | None = None
    attempts: int = 1
