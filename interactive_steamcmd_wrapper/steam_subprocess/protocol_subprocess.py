from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class SteamCMDSubprocessError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(f"Subprocess unknown error reason: {reason}")


class PSubprocessProtocol(Protocol):
    @abstractmethod
    @property
    def executable_path(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    @property
    def executable_file(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def input(self, payload: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def read_output(self) -> str:
        raise NotImplementedError

    def __del__(self) -> None:
        self.stop()
