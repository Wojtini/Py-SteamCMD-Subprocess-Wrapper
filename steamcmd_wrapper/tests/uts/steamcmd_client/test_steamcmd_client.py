import pytest

from steamcmd_wrapper import SteamCMDClient
from steamcmd_wrapper.config import (
    IGNORED_ERRORS,
    ON_APP_UPDATE_SUCCESS_MSG,
    ON_LOGIN_MSG,
    ON_MOD_UPDATE_SUCCESS_MSG,
    ON_READY_MSG,
    TIMEOUT_ERROR_MSG,
    SteamCMDProcessError,
)
from steamcmd_wrapper.steam_client.steamcmd_client import SteamCMDClientInstallDirError
from steamcmd_wrapper.tests.uts.steamcmd_client import FileSystemMock, SubprocessMock


class TestSteamCMDClient:
    @pytest.fixture(autouse=True)
    def _setup(self) -> None:
        self.file_system_mock = FileSystemMock()
        self.subprocess_mock = SubprocessMock()
        self.subprocess_mock.outputs = [ON_READY_MSG]
        self.steamcmd_client = SteamCMDClient(
            self.subprocess_mock,
            self.file_system_mock,
        )

    def test_subprocess_started(self) -> None:
        assert self.subprocess_mock.started

    def test_generic_error_on_startup(self) -> None:
        self.subprocess_mock.outputs = ["generic error"]
        with pytest.raises(SteamCMDProcessError):
            self.steamcmd_client = SteamCMDClient(
                self.subprocess_mock,
                self.file_system_mock,
            )

    def test_ignored_error_on_startup(self) -> None:
        self.subprocess_mock.outputs = [IGNORED_ERRORS[0], ON_READY_MSG]
        self.steamcmd_client = SteamCMDClient(
            self.subprocess_mock,
            self.file_system_mock,
        )

        assert self.subprocess_mock.started

    def test_login(self) -> None:
        self.subprocess_mock.outputs = [ON_LOGIN_MSG]
        self.steamcmd_client.login("login", "password", "oauth2")

        assert self.subprocess_mock.inputs == ["login login password oauth2"]

    def test_login_anonymous(self) -> None:
        self.subprocess_mock.outputs = [ON_LOGIN_MSG]
        self.steamcmd_client.login_as_anonymous()

        assert self.subprocess_mock.inputs == ["login anonymous anonymous"]

    def test_update_app(self) -> None:
        self.subprocess_mock.outputs = [ON_APP_UPDATE_SUCCESS_MSG] * 2
        self.steamcmd_client.update_app("123456", validate=False)
        self.steamcmd_client.update_app("111111", validate=True)

        assert self.subprocess_mock.inputs[0] == "app_update 123456"
        assert self.subprocess_mock.inputs[1] == "app_update 111111 validate"

    def test_update_workshop_mod(self) -> None:
        self.subprocess_mock.outputs = [ON_MOD_UPDATE_SUCCESS_MSG] * 2
        self.steamcmd_client.update_workshop_mod("app_id_1", "mod_id_1", validate=False)
        self.steamcmd_client.update_workshop_mod("app_id_2", "mod_id_2", validate=True)

        assert self.subprocess_mock.inputs[0] == "workshop_download_item app_id_1 mod_id_1"
        assert self.subprocess_mock.inputs[1] == "workshop_download_item app_id_2 mod_id_2 validate"

    def test_update_workshop_mod_timeout_with_noise(self) -> None:
        noise = ["mock message"] * 20
        self.subprocess_mock.outputs = [TIMEOUT_ERROR_MSG, *noise, ON_MOD_UPDATE_SUCCESS_MSG]
        self.steamcmd_client.update_workshop_mod("app_id_1", "mod_id_1")

        assert self.subprocess_mock.inputs[0] == "workshop_download_item app_id_1 mod_id_1 validate"

    def test_set_install_dir(self) -> None:
        self.steamcmd_client.set_install_dir("/dir")

        assert self.subprocess_mock.inputs == ["force_install_dir /dir"]

    def test_set_install_dir_in_the_same_dir_as_executable(self) -> None:
        with pytest.raises(SteamCMDClientInstallDirError):
            self.steamcmd_client.set_install_dir("/steamcmd_dir")
