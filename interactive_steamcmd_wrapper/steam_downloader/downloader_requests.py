from abc import abstractmethod
from typing import Protocol

import requests


class PDownloadRequests(Protocol):
    @abstractmethod
    def get_content(self, url: str) -> bytes:
        raise NotImplementedError


class DownloadRequests(PDownloadRequests):
    def get_content(self, url: str) -> bytes:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.content
