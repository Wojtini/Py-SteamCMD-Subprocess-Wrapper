from abc import abstractmethod
from typing import Protocol


class PSteamCMDClient(Protocol):
    @abstractmethod
    def login(
        self,
        username: str,
        password: str,
        token: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def login_as_anonymous(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_install_dir(self, install_dir: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_app(self, app_id: str, validate: bool = True) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_workshop_mod(self, app_id: str, mod_id: str, validate: bool = True) -> None:
        raise NotImplementedError
