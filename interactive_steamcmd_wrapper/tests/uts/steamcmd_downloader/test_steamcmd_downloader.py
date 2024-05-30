from pathlib import Path

import pytest

from interactive_steamcmd_wrapper.steam_downloader.downloader_requests import PDownloadRequests
from interactive_steamcmd_wrapper.steam_downloader.file_system import PFileSystem
from interactive_steamcmd_wrapper.steam_downloader.linux_steamcmd_downloader import (
    LinuxSteamCMDDownloader,
)
from interactive_steamcmd_wrapper.steam_downloader.protocol_steamcmd_downloader import (
    DirectoryNotEmptyError,
    PathIsNotADirectoryError,
)


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


class TestLinuxSteamCMDDownloader:
    @pytest.fixture(autouse=True)
    def _setup(self) -> None:
        self.test_path = "/testpath"
        self.download_request_mock = DownloadRequestsMock()
        self.file_system_mock = FileSystemMock()

    def _get_downloader(self) -> LinuxSteamCMDDownloader:
        return LinuxSteamCMDDownloader(
            self.test_path,
            self.download_request_mock,
            self.file_system_mock,
        )

    def test_fresh_install(self) -> None:
        downloader = self._get_downloader()
        downloader.download()

        assert len(self.file_system_mock.extracted_bytes) == 1
        assert (
            self.download_request_mock.b,
            self.test_path,
        ) in self.file_system_mock.extracted_bytes

    def test_install_in_the_same_location(self) -> None:
        self.file_system_mock.is_directory_free_return_value = False
        self.file_system_mock.files_in_directory = ["steamcmd.sh"]

        downloader = self._get_downloader()
        downloader.download()

        assert len(self.file_system_mock.extracted_bytes) == 0

    def test_install_in_non_empty_directory(self) -> None:
        self.file_system_mock.is_directory_free_return_value = False
        self.file_system_mock.files_in_directory = ["random_file"]

        with pytest.raises(DirectoryNotEmptyError):
            self._get_downloader()

        assert len(self.file_system_mock.extracted_bytes) == 0
        assert self.download_request_mock.call_times == 0

    def test_install_in_non_directory(self) -> None:
        self.file_system_mock.is_directory_free_return_value = False
        self.test_path = "not_a_directory"
        self.file_system_mock.files_in_directory = ["random_file"]

        with pytest.raises(PathIsNotADirectoryError):
            self._get_downloader()

        assert len(self.file_system_mock.extracted_bytes) == 0
        assert self.download_request_mock.call_times == 0
