from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from interactive_steamcmd_wrapper.steam_downloader.file_system import FileSystem


class TestFileSystem:
    @pytest.fixture(autouse=True)
    def _setup(self, fs: FakeFilesystem) -> None:
        self.fs = fs
        self.file_system = FileSystem()

    def test_is_directory(self) -> None:
        self.fs.create_file("/not_directory")
        self.fs.create_dir("/directory")

        assert not self.file_system.is_directory(Path("/not_directory"))
        assert self.file_system.is_directory(Path("/directory"))

    def test_is_file_in_directory_no_file(self) -> None:
        self.fs.create_dir("/directory")
        assert not self.file_system.is_file_in_directory("non_existing", Path("/directory"))

    def test_is_file_in_directory(self) -> None:
        self.fs.create_file("/directory/existing")
        assert self.file_system.is_file_in_directory("existing", Path("/directory"))

    def test_is_file_in_directory_no_directory(self) -> None:
        assert not self.file_system.is_file_in_directory("existing", Path("/directory"))

    def test_is_directory_free_full_dir(self) -> None:
        self.fs.create_file("/full_dir/random_file")
        assert not self.file_system.is_directory_free(Path("/full_dir/random_file"))

    def test_is_directory_free_empty_dir(self) -> None:
        self.fs.create_dir("/empty_dir")
        assert self.file_system.is_directory_free(Path("/empty_dir"))

    def test_is_directory_specified_file(self) -> None:
        self.fs.create_file("/empty_dir")
        assert not self.file_system.is_directory_free(Path("/empty_dir"))

    def test_is_directory_free_non_existing(self) -> None:
        assert self.file_system.is_directory_free(Path("/non_existing_dir"))
