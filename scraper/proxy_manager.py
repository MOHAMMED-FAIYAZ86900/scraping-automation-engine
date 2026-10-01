import os
from itertools import cycle


class ProxyManager:

    def __init__(self, proxies=None):

        if proxies is None:

            proxy_string = os.getenv(
                "PROXY_URLS",
                ""
            ).strip()

            if proxy_string:

                proxies = [
                    item.strip()
                    for item in proxy_string.split(",")
                    if item.strip()
                ]

            else:
                proxies = []

        self.proxies = proxies

        self._cycle = (
            cycle(self.proxies)
            if self.proxies
            else None
        )

    def next_proxy(self):

        if self._cycle is None:
            return None

        return next(self._cycle)

    def count(self):

        return len(self.proxies)

    def has_proxies(self):

        return bool(self.proxies)