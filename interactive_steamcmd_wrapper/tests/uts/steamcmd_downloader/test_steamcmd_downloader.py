import pytest

from interactive_steamcmd_wrapper.steam_downloader.linux_steamcmd_downloader import (
    LinuxSteamCMDDownloader,
)
from interactive_steamcmd_wrapper.steam_downloader.protocol_steamcmd_downloader import (
    DirectoryNotEmptyError,
    PathIsNotADirectoryError,
)
from interactive_steamcmd_wrapper.tests.uts.steamcmd_downloader import (
    DownloadRequestsMock,
    FileSystemMock,
)


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
