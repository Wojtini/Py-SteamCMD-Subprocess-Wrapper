import logging
import os
from subprocess import Popen, PIPE
from typing import Optional
import platform

from interactive_steamcmd_wrapper.config import on_ready_msg, generic_error_msg, on_login_msg, \
    on_app_update_success_msg, on_mod_update_success_msg, on_timeout_msg
from interactive_steamcmd_wrapper.exceptions import ISteamCMDProcessError, ISteamCMDTimeout


class ISteamCMDProcess:
    def __init__(self, steamcmd_exe_location: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.exe = steamcmd_exe_location

    def __enter__(self):
        self.process = Popen(self.exe, stdin=PIPE, stdout=PIPE, shell=True)
        self.process.stderr = self.process.stdout
        self._wait_steam_to_load()
        return self

    @staticmethod
    def _get_proccess_command():
        system = platform.system()
        if system == "Linux":
            return "sh"
        raise ISteamCMDProcessError("Cannot start process on %s OS", system)

    def _wait_steam_to_load(self) -> None:
        while True:
            output = self._read_output()
            if on_ready_msg in output:
                return
            if generic_error_msg in output.lower():
                raise ISteamCMDProcessError("SteamCMD returned generic error code on startup")

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
        self._wait_steam_to_login()

    def _wait_steam_to_login(self) -> None:
        while True:
            output = self._read_output()
            if on_login_msg in output:
                return
            if generic_error_msg in output.lower():
                raise ISteamCMDProcessError("SteamCMD returned generic error code on startup")

    def _set_install_dir(self, install_dir: str) -> None:
        if os.path.join(install_dir, "SteamCMD.exe") in self.exe:
            raise ISteamCMDProcessError("Can't install in same directory as steamcmd. SteamCMD won't throw an error but will ignore new location")
        self._input(f"force_install_dir {install_dir}")

    def update_app(self, app_id: int, app_dir: str, validate: bool = True) -> None:
        self._set_install_dir(app_dir)
        self._input(f"app_update {app_id} {'validate' if validate else ''}")
        self._wait_for_update_app()

    def _wait_for_update_app(self):
        while True:
            output = self._read_output()
            if on_app_update_success_msg in output:
                return
            if generic_error_msg.lower() in output.lower():
                raise ISteamCMDProcessError("SteamCMD returned generic error code")

    def update_workshop_mod(self, app_id: int, mod_id: int, mods_dir: str, validate: bool = True) -> None:
        self._set_install_dir(mods_dir)
        self._input(f"workshop_download_item {app_id} {mod_id} {'validate' if validate else ''}")
        try:
            self._wait_for_update_workshop_mod()
            return
        except ISteamCMDTimeout:
            pass
        self.logger.info("Retrying download after timeout...")
        self.update_workshop_mod(app_id, mod_id, mods_dir, validate)

    def _wait_for_update_workshop_mod(self):
        while True:
            output = self._read_output()
            if on_mod_update_success_msg in output:
                return
            elif on_timeout_msg in output:
                raise ISteamCMDTimeout
            elif generic_error_msg in output.lower():
                raise ISteamCMDProcessError("SteamCMD returned generic error code")

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
