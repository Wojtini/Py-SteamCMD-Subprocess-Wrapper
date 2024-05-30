import logging
from pathlib import Path

from interactive_steamcmd_wrapper.config import (
    GENERIC_ERRORS,
    IGNORED_ERRORS,
    ON_APP_UPDATE_SUCCESS_MSG,
    ON_LOGIN_MSG,
    ON_MOD_UPDATE_SUCCESS_MSG,
    ON_READY_MSG,
    SteamCMDDownloadTimeoutError,
)
from interactive_steamcmd_wrapper.steam_client.protocol_steamcmd_client import PSteamCMDClient
from interactive_steamcmd_wrapper.steam_downloader.file_system import PFileSystem
from interactive_steamcmd_wrapper.steam_subprocess.protocol_subprocess import PSubprocessProtocol


class SteamCMDClientInstallDirError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Can't install in same directory as steamcmd. SteamCMD will ignore new location",
        )


class SteamCMDClient(PSteamCMDClient):
    def __init__(self, subprocess: PSubprocessProtocol, file_system: PFileSystem) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_logged_user: str | None = None
        self.subprocess = subprocess
        self.file_system = file_system
        self.subprocess.start()
        self._wait_for_steam_cmd_output(ON_READY_MSG)

    def login(
        self,
        username: str,
        password: str,
        token: str | None = None,
    ) -> None:
        self.logger.info("Logging in as username:")
        self.current_logged_user = username
        payload = f"login {username} {password} {token if token else ''}"
        self.subprocess.input(payload)
        self._wait_for_steam_cmd_output(ON_LOGIN_MSG)

    def login_as_anonymous(self) -> None:
        self.login("anonymous", "anonymous")

    def set_install_dir(self, install_dir: str) -> None:
        if self.file_system.is_file_in_directory(
            self.subprocess.executable_file,
            Path(install_dir),
        ):
            raise SteamCMDClientInstallDirError
        self.subprocess.input(f"force_install_dir {install_dir}")

    def update_app(self, app_id: str, validate: bool = True) -> None:
        self.subprocess.input(f"app_update {app_id} {'validate' if validate else ''}")
        self._wait_for_steam_cmd_output(ON_APP_UPDATE_SUCCESS_MSG)

    def update_workshop_mod(self, app_id: str, mod_id: str, validate: bool = True) -> None:
        self.subprocess.input(
            f"workshop_download_item {app_id} {mod_id} {'validate' if validate else ''}",
        )
        try:
            self._wait_for_steam_cmd_output(ON_MOD_UPDATE_SUCCESS_MSG)
        except SteamCMDDownloadTimeoutError:
            self.logger.info("Retrying download after timeout...")
            self.update_workshop_mod(app_id, mod_id, validate)
        else:
            return

    def _wait_for_steam_cmd_output(self, success_msg: str) -> None:
        while True:
            output = self.subprocess.read_output()
            if success_msg in output:
                return
            self._check_output_for_errors(output)

    def _check_output_for_errors(self, output: str) -> None:
        for generic_error in GENERIC_ERRORS:
            if generic_error.error_msg.lower() in output.lower():
                if any(output.lower() in ignored_error.lower() for ignored_error in IGNORED_ERRORS):
                    return
                raise generic_error.exception(output)
