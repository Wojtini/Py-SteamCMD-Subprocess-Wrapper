import logging
from pathlib import Path

from steamcmd_wrapper.config import package_links
from steamcmd_wrapper.steam_downloader.downloader_requests import PDownloadRequests
from steamcmd_wrapper.steam_downloader.file_system import PFileSystem
from steamcmd_wrapper.steam_downloader.protocol_steamcmd_downloader import (
    DirectoryNotEmptyError,
    PathIsNotADirectoryError,
    PSteamCMDDownloader,
)


class LinuxSteamCMDDownloader(PSteamCMDDownloader):
    def __init__(
        self,
        installation_dir_path: str,
        requests: PDownloadRequests,
        file_system: PFileSystem,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.requests = requests
        self.file_system = file_system
        self.installation_path = Path(installation_dir_path)
        self.platform_name = "Linux"
        self.executable_name = "steamcmd" + package_links[self.platform_name].executable_extension
        self.download_url = package_links[self.platform_name].url

        self._check_installation_path()

    def _check_installation_path(self) -> None:
        if self.file_system.is_directory_free(self.installation_path):
            return
        if not self.file_system.is_directory(self.installation_path):
            raise PathIsNotADirectoryError(self.installation_path)
        if self.file_system.is_file_in_directory(self.executable_name, self.installation_path):
            return
        raise DirectoryNotEmptyError(self.installation_path)

    def download(self) -> None:
        if self.file_system.is_file_in_directory(self.executable_name, self.installation_path):
            self.logger.info(f"SteamCMD already downloaded at {self.installation_path}. Skipping..")
            return
        self.logger.info(f"Downloading SteamCMD for {self.platform_name}")
        content = self.requests.get_content(self.download_url)

        self.file_system.extract_bytes(content, self.installation_path)
        self.logger.info("Downloaded SteamCMD")
