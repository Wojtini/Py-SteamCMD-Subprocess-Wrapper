from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class DownloadPathError(Exception):
    ...


class DirectoryNotEmptyError(DownloadPathError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"{path} is not empty")


class PathIsNotADirectoryError(DownloadPathError):
    def __init__(self, path: Path) -> None:
        super().__init__(f"{path} is not a directory")


class PSteamCMDDownloader(Protocol):
    @abstractmethod
    def download(self) -> None:
        raise NotImplementedError
