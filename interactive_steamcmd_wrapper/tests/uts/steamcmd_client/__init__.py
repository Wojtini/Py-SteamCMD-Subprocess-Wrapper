from pathlib import Path

from interactive_steamcmd_wrapper.steam_downloader.file_system import PFileSystem
from interactive_steamcmd_wrapper.steam_subprocess.protocol_subprocess import PSubprocessProtocol


class FileSystemMock(PFileSystem):
    def is_file_in_directory(self, _: str, path: Path) -> bool:
        return str(path) == "/steamcmd_dir"

    def extract_bytes(self, b: bytes, location: Path) -> None:
        raise NotImplementedError

    def is_directory(self, path: Path) -> bool:
        raise NotImplementedError

    def is_directory_free(self, directory: Path) -> bool:
        raise NotImplementedError


class SubprocessMock(PSubprocessProtocol):
    def __init__(self) -> None:
        self.started = False
        self.inputs: list[str] = []
        self.outputs: list[str] = []

    @property
    def executable_path(self) -> Path:
        return Path("/steamcmd_dir")

    @property
    def executable_file(self) -> str:
        return "steamcmd.sh"

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        ...

    def input(self, payload: str) -> None:
        self.inputs.append(payload)

    def read_output(self) -> str:
        return self.outputs.pop(0)
