import logging
from pathlib import Path

from interactive_steamcmd_wrapper.steam_client.steamcmd_client import SteamCMDClient
from interactive_steamcmd_wrapper.steam_downloader.downloader_requests import DownloadRequests
from interactive_steamcmd_wrapper.steam_downloader.file_system import FileSystem
from interactive_steamcmd_wrapper.steam_downloader.linux_steamcmd_downloader import (
    LinuxSteamCMDDownloader,
)
from interactive_steamcmd_wrapper.steam_subprocess.linux_steam_subprocess import (
    LinuxSteamCMDSubprocess,
)


class UnsupportedPlatformError(Exception):
    def __init__(self, system_name: str) -> None:
        super().__init__(f"{system_name} is unsupported platform")


def get_steamcmd_client(path_location: str) -> SteamCMDClient:
    logging.basicConfig(level=logging.DEBUG)

    filesystem = FileSystem()
    LinuxSteamCMDDownloader(
        path_location,
        DownloadRequests(),
        filesystem,
    ).download()
    subprocess = LinuxSteamCMDSubprocess(Path(str(path_location) + "/steamcmd.sh"))
    return SteamCMDClient(
        subprocess,
        filesystem,
    )


__all__ = ["get_steamcmd_client", ""]
