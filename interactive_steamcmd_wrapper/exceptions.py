from dataclasses import dataclass


class ISteamCMDProcessError(Exception):
    ...


class ISteamCMDAlreadyInstalled(ISteamCMDProcessError):
    ...


class ISteamCMDDownloadTimeout(ISteamCMDProcessError):
    ...


class ISteamCMDInstallException(ISteamCMDProcessError):
    ...


@dataclass
class CustomError:
    error_msg: str
    exception: ISteamCMDProcessError
