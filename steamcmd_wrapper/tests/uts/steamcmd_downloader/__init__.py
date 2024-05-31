from pathlib import Path

from steamcmd_wrapper.steam_downloader.downloader_requests import PDownloadRequests
from steamcmd_wrapper.steam_downloader.file_system import PFileSystem


class DownloadRequestsMock(PDownloadRequests):
    def __init__(self) -> None:
        self.b = b"random bytes"
        self.call_times = 0

    def get_content(self, _: str) -> bytes:
        self.call_times += 1
        return self.b


class FileSystemMock(PFileSystem):
    def __init__(self) -> None:
        self.is_directory_free_return_value = True
        self.files_in_directory: list[str] = []
        self.dir_path = "/testpath"

        self.extracted_bytes: list[tuple[bytes, str]] = []

    def is_directory(self, path: Path) -> bool:
        return str(path) == self.dir_path

    def extract_bytes(self, b: bytes, location: Path) -> None:
        self.extracted_bytes.append((b, str(location)))

    def is_directory_free(self, path: Path) -> bool:
        return str(path) == self.dir_path and self.is_directory_free_return_value

    def is_file_in_directory(self, file_name: str, directory: Path) -> bool:
        if directory == self.dir_path:
            return False
        return file_name in self.files_in_directory
