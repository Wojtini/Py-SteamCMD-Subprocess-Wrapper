from typing import List

from interactive_steamcmd_wrapper.exceptions import CustomError, ISteamCMDDownloadTimeout, ISteamCMDProcessError

ON_READY_MSG = "OK"
ON_APP_UPDATE_SUCCESS_MSG = "Success! App"
ON_MOD_UPDATE_SUCCESS_MSG = "Success. Downloaded item"
ON_LOGIN_MSG = "Waiting for user info...OK"


GENERIC_ERRORS: List[CustomError] = [
    CustomError("ERROR", ISteamCMDProcessError()),
    CustomError("FAILED", ISteamCMDProcessError()),
    CustomError("ERROR! Timeout downloading item", ISteamCMDDownloadTimeout()),
]

IGNORED_ERRORS: List[str] = [
    "Loading Steam API...dlmopen steamservice.so failed: steamservice.so: cannot open shared object file: No such file or directory",
]
