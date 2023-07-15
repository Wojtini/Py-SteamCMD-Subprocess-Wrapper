
import os
from abc import abstractmethod
from io import BytesIO
from pathlib import Path
from tarfile import open as tarfile_open
from typing import Protocol


class PFileSystem(Protocol):
    @abstractmethod
    def extract_bytes(self, b: bytes, location: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_directory_free(self, directory: Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_file_in_directory(self, file_name: str, directory: Path) -> bool:
        raise NotImplementedError


class FileSystem(PFileSystem):
    def extract_bytes(self, b: bytes, location: Path) -> None:
        bytes_io = BytesIO(b)
        with tarfile_open(fileobj=bytes_io, mode="r") as tar:
            for member in tar.getmembers():
                tar.extract(member, path=location)

    def is_directory(self, path: Path) -> bool:
        return path.is_dir()

    def is_directory_free(self, path: Path) -> bool:
        if not path.exists():
            return True
        if not self.is_directory(path):
            return False
        return not bool(os.listdir(path))

    def is_file_in_directory(self, file_name: str, path: Path) -> bool:
        if not path.exists():
            return False
        return file_name in os.listdir(path)
