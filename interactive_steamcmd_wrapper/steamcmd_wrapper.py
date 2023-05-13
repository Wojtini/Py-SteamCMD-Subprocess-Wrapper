import logging
import os
import platform
import subprocess
import urllib.request
from interactive_steamcmd_wrapper.exceptions import ISteamCMDProcessError, ISteamCMDAlreadyInstalled, \
    ISteamCMDInstallException
from interactive_steamcmd_wrapper.steamcmd_process import ISteamCMDProcess

package_links = {
    "Linux": {
        "url": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
        "extension": ".sh",
        "d_extension": ".tar.gz"
    }
}


class InteractiveSteamCMD:
    _installation_path = ""

    def __init__(self, installation_path):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._installation_path = installation_path
        self._prepare_install_directory()

    def _prepare_install_directory(self) -> None:
        path = self._installation_path
        if os.path.exists(path):
            self.logger.info("Path exists at <%s>", path)
            if not os.path.isdir(path):
                raise ISteamCMDProcessError("install_directory is not a directory")
            return None
        self.logger.info("Creating directory for installation at <%s>", path)
        os.makedirs(path)

    def run(self):
        return ISteamCMDProcess(self.exe)

    def install(self):
        self._prepare_installation()
        if os.path.isfile(self.exe):
            self.logger.info("SteamCMD already installed. Skipping")
            self._empty_launch()
            raise ISteamCMDAlreadyInstalled("SteamCMD already installed")
        self._download()
        self._extract_steamcmd()
        self._empty_launch()

    def _prepare_installation(self):
        if self.platform not in package_links:
            raise ISteamCMDProcessError(f"Non supported operating system. Expected Windows or Linux, got {self.platform}")
        self.steamcmd_url = package_links[self.platform]["url"]
        self.zip = "steamcmd" + package_links[self.platform]["d_extension"]

    @property
    def platform(self):
        return platform.system()

    @property
    def exe(self) -> str:
        return os.path.join(
            self._installation_path,
            "steamcmd" + package_links[self.platform]["extension"]
        )

    def _download(self):
        self.logger.info("Downloading SteamCMD")
        try:
            if self.steamcmd_url.lower().startswith("http"):
                req = urllib.request.Request(self.steamcmd_url)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                with open(self.zip, "wb") as f:
                    f.write(data)
                return data
        except Exception as e:
            raise ISteamCMDProcessError(f"An unknown exception occurred during downloading. {e}")

    def _extract_steamcmd(self):
        self.logger.info("Extracting SteamCMD")
        if self.platform == 'Linux':
            import tarfile
            with tarfile.open(self.zip, 'r:gz') as f:
                f.extractall(self._installation_path)
        else:
            raise ISteamCMDProcessError(f"The operating system {self.platform} is not supported.")

        os.remove(self.zip)

    def _empty_launch(self):
        self.logger.info("Launching steam to update")
        try:
            subprocess.check_call((self.exe, "+quit"))
        except subprocess.CalledProcessError as e:
            raise ISteamCMDInstallException(f"First run returned {e.returncode}")
