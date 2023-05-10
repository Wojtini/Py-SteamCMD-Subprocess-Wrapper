from typing import List

from interactive_steamcmd_wrapper.exceptions import CustomError, ISteamCMDDownloadTimeout, ISteamCMDProcessError

ON_READY_MSG = "Loading Steam API...OK"
ON_APP_UPDATE_SUCCESS_MSG = "Success! App"
ON_MOD_UPDATE_SUCCESS_MSG = "Success. Downloaded item"
ON_LOGIN_MSG = "Waiting for user info...OK"


TIMEOUT_ERROR: CustomError = CustomError("ERROR! Timeout downloading item", ISteamCMDDownloadTimeout())
GENERIC_ERRORS: List[CustomError] = [
    CustomError("ERROR", ISteamCMDProcessError()),
    CustomError("FAILED", ISteamCMDProcessError()),
]
