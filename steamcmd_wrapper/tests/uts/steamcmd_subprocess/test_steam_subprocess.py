import time
from pathlib import Path
from subprocess import Popen

import pytest

from steamcmd_wrapper import LinuxSteamCMDSubprocess
from steamcmd_wrapper.tests.uts.steamcmd_subprocess.echo import (
    STEAMCMD_SUBPROCESS_MOCK_EXECUTABLE,
)


class TestSteamSubprocess:
    @pytest.fixture(autouse=True)
    def _setup(self) -> None:
        self.path = Path(STEAMCMD_SUBPROCESS_MOCK_EXECUTABLE)
        self.subprocess = LinuxSteamCMDSubprocess(self.path)

    def test_properties(self) -> None:
        executable = "steamcmd.sh"
        path = Path(f"/steam_dir/{executable}")
        subprocess = LinuxSteamCMDSubprocess(path)
        assert subprocess.executable_path == path
        assert subprocess.executable_file == executable

    def test_subprocess_communication(self) -> None:
        self.subprocess.start()
        self.subprocess.input("test payload")
        assert self.subprocess.read_output() == "test payload"

    def test_subprocess_stopping(self) -> None:
        self.subprocess.start()
        self.subprocess.stop()

    def test_subprocess_stopping_after_del(self) -> None:
        self.subprocess.start()
        process = self.subprocess._process  # noqa: SLF001
        del self.subprocess
        assert process
        assert self.check_if_process_exited(process, 10)

    @staticmethod
    def check_if_process_exited(
        process: Popen,
        timeout: float,
        period: float=0.25,
    ) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            if process.poll() is not None:
                return True
            time.sleep(period)
        return False
