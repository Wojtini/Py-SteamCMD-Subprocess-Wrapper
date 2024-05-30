from dataclasses import dataclass


@dataclass
class PackageLink:
    url: str
    executable_extension: str


package_links: dict[str, PackageLink] = {
    "Linux": PackageLink(
        "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
        ".sh",
    ),
}

ON_READY_MSG = "OK"
ON_APP_UPDATE_SUCCESS_MSG = "Success! App"
ON_MOD_UPDATE_SUCCESS_MSG = "Success. Downloaded item"
ON_LOGIN_MSG = "Waiting for user info...OK"


class SteamCMDProcessError(Exception):
    def __init__(self, output: str) -> None:
        super().__init__(f"Steam CMD unknown error: {output}")


class SteamCMDDownloadTimeoutError(SteamCMDProcessError):
    def __init__(self, output: str) -> None:
        super().__init__(f"Timeout downloading item: {output}")


@dataclass
class CustomError:
    error_msg: str
    exception: type[SteamCMDProcessError]


GENERIC_ERRORS: list[CustomError] = [
    CustomError("ERROR! Timeout downloading item", SteamCMDDownloadTimeoutError),
    CustomError("ERROR", SteamCMDProcessError),
    CustomError("FAILED", SteamCMDProcessError),
]

IGNORED_ERRORS: list[str] = [
    # GUI library error Steam throws at the startup - not required:
    "Loading Steam API...dlmopen steamservice.so failed:"
    " steamservice.so: cannot open shared object file: No such file or directory",
    "ILocalize::AddFile()",
]
