import logging
import os
from subprocess import Popen, PIPE
from typing import Optional

from interactive_steamcmd_wrapper.config import (
    ON_READY_MSG,
    ON_LOGIN_MSG,
    ON_APP_UPDATE_SUCCESS_MSG,
    ON_MOD_UPDATE_SUCCESS_MSG,
    GENERIC_ERRORS, IGNORED_ERRORS,
)
from interactive_steamcmd_wrapper.exceptions import ISteamCMDProcessError, ISteamCMDDownloadTimeout, CustomError


class ISteamCMDProcess:
    def __init__(self, steamcmd_location: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.run_file = steamcmd_location

    def __enter__(self):
        self.process = Popen(self.run_file, stdin=PIPE, stdout=PIPE, shell=True)
        self.process.stderr = self.process.stdout
        self._wait_for_steam_cmd_output(ON_READY_MSG)
        return self

    def login(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):
        if not user:
            user = "anonymous"
        payload = f"login {user} {password if password else ''} {token if token else ''}"
        self._input(payload, hide_logs=True)
        self._wait_for_steam_cmd_output(ON_LOGIN_MSG)

    def _set_install_dir(self, install_dir: str) -> None:
        if os.path.join(install_dir, "SteamCMD.exe") in self.run_file:
            raise ISteamCMDProcessError(
                "Can't install in same directory as steamcmd. SteamCMD won't throw an error but will ignore new location"
            )
        self._input(f"force_install_dir {install_dir}")

    def update_app(self, app_id: int, app_dir: str, validate: bool = True) -> None:
        self._set_install_dir(app_dir)
        self._input(f"app_update {app_id} {'validate' if validate else ''}")
        self._wait_for_steam_cmd_output(ON_APP_UPDATE_SUCCESS_MSG)

    def update_workshop_mod(self, app_id: int, mod_id: int, mods_dir: str, validate: bool = True) -> None:
        self._set_install_dir(mods_dir)
        self._input(f"workshop_download_item {app_id} {mod_id} {'validate' if validate else ''}")
        try:
            self._wait_for_steam_cmd_output(ON_MOD_UPDATE_SUCCESS_MSG)
            return
        except ISteamCMDDownloadTimeout:
            pass
        self.logger.info("Retrying download after timeout...")
        self.update_workshop_mod(app_id, mod_id, mods_dir, validate)

    def _wait_for_steam_cmd_output(self, success_msg: str) -> None:
        while True:
            output = self._read_output()
            if success_msg in output:
                return
            self._check_output_for_errors(output)

    @staticmethod
    def _check_output_for_errors(output: str) -> None:
        for generic_error in GENERIC_ERRORS:
            if generic_error.error_msg.lower() in output.lower():
                if any(output.lower() in ignored_error.lower() for ignored_error in IGNORED_ERRORS):
                    return
                raise ISteamCMDProcessError("Steam CMD errored", output)

    def _input(self, payload: str, hide_logs: bool = False) -> None:
        if not hide_logs:
            self.logger.info("Payload: '%s'", payload)
        self.process.stdin.write(bytes(payload + "\n", encoding="UTF-8"))
        self.process.stdin.flush()

    def _read_output(self) -> str:
        output = self.process.stdout.readline().strip().decode("UTF-8")
        self.logger.info(output)
        return output

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.stdin.write(b"quit\n")
