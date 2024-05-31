import logging
from pathlib import Path
from subprocess import PIPE, Popen

from steamcmd_wrapper.steam_subprocess.protocol_subprocess import (
    PSubprocessProtocol,
    SteamCMDSubprocessError,
)


class LinuxSteamCMDSubprocess(PSubprocessProtocol):
    def __init__(self, executable_path: Path) -> None:
        self._executable_path = executable_path
        self._executable_file = str(self.executable_path).split("/")[-1]
        self.logger = logging.getLogger(self.__class__.__name__)
        self._process: None | Popen = None

    @property
    def executable_path(self) -> Path:
        return self._executable_path

    @property
    def executable_file(self) -> str:
        return self._executable_file

    def start(self) -> None:
        self.logger.debug("Starting SteamCMD subprocess")
        self._process = Popen(self.executable_path, stdin=PIPE, stdout=PIPE)  # noqa: S603
        self._process.stderr = self._process.stdout
        self.logger.debug(f"Started SteamCMD subprocess PID: {self._process.pid}")

    def stop(self) -> None:
        self.logger.debug("Stopping SteamCMD subprocess")
        self.input("quit")
        while self._process and self._process.poll() is None:
            continue

    def input(self, payload: str) -> None:
        if self._process is None:
            raise SteamCMDSubprocessError("SteamCMD subprocess has not been started yet")
        if not self._process.stdin:
            raise SteamCMDSubprocessError("No stdin")
        self._process.stdin.write(bytes(payload + "\n", encoding="UTF-8"))
        self._process.stdin.flush()

    def read_output(self) -> str:
        if self._process is None:
            raise SteamCMDSubprocessError("SteamCMD subprocess has not been started yet")
        if not self._process.stdout:
            raise SteamCMDSubprocessError("No stdout")
        output = str(self._process.stdout.readline().strip().decode("UTF-8"))
        if output:
            self.logger.debug(output)
        return output

    def __del__(self) -> None:
        if self._process is not None:
            self._process.kill()
