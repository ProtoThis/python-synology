"""Library exceptions."""
from .const import API_AUTH
from .const import ERROR_AUTH
from .const import ERROR_COMMON
from .const import ERROR_DOWNLOAD_SEARCH
from .const import ERROR_DOWNLOAD_TASK
from .const import ERROR_FILE
from .const import ERROR_SURVEILLANCE
from .const import ERROR_VIRTUALIZATION


class SynologyDSMException(Exception):
    """Generic Synology DSM exception."""

    def __init__(self, api, code, details=None):
        reason = ERROR_COMMON.get(code)
        if api and not reason:
            if api == API_AUTH:
                reason = ERROR_AUTH.get(code)
            elif "SYNO.DownloadStation" in api:
                if "BTSearch" in api:
                    reason = ERROR_DOWNLOAD_SEARCH.get(code)
                elif "Task" in api:
                    reason = ERROR_DOWNLOAD_TASK.get(code)
            elif "SYNO.FileStation" in api:
                reason = ERROR_FILE.get(code)
            elif "SYNO.SurveillanceStation" in api:
                reason = ERROR_SURVEILLANCE.get(code)
            elif "SYNO.Virtualization" in api:
                reason = ERROR_VIRTUALIZATION.get(code)
        if not reason:
            reason = "Unknown"

        error_message = {"api": api, "code": code, "reason": reason, "details": details}
        super().__init__(error_message)


# Request
class SynologyDSMRequestException(SynologyDSMException):
    """Request exception."""

    def __init__(self, exception):
        ex_class = exception.__class__.__name__
        ex_reason = exception.args[0]
        if hasattr(exception.args[0], "reason"):
            ex_reason = exception.args[0].reason
        super().__init__(None, -1, f"{ex_class} = {ex_reason}")


# API
class SynologyDSMAPINotExistsException(SynologyDSMException):
    """API not exists exception."""

    def __init__(self, api):
        super().__init__(api, -2, f"API {api} does not exists")


class SynologyDSMAPIErrorException(SynologyDSMException):
    """API returns an error exception."""

    def __init__(self, api, code, details):
        super().__init__(api, code, details)


# Login
class SynologyDSMLoginFailedException(SynologyDSMException):
    """Failed to login exception."""

    def __init__(self, code, details=None):
        super().__init__(API_AUTH, code, details)


class SynologyDSMLoginInvalidException(SynologyDSMLoginFailedException):
    """Invalid password & not admin account exception."""

    def __init__(self, username):
        message = f"Invalid password or not admin account: {username}"
        super().__init__(400, message)


class SynologyDSMLoginDisabledAccountException(SynologyDSMLoginFailedException):
    """Guest & disabled account exception."""

    def __init__(self, username):
        message = f"Guest or disabled account: {username}"
        super().__init__(401, message)


class SynologyDSMLoginPermissionDeniedException(SynologyDSMLoginFailedException):
    """No access to login exception."""

    def __init__(self, username):
        message = f"Permission denied for account: {username}"
        super().__init__(402, message)


class SynologyDSMLogin2SARequiredException(SynologyDSMLoginFailedException):
    """2SA required to login exception."""

    def __init__(self, username):
        message = f"Two-step authentication required for account: {username}"
        super().__init__(403, message)


class SynologyDSMLogin2SAFailedException(SynologyDSMLoginFailedException):
    """2SA code failed exception."""

    def __init__(self):
        message = "Two-step authentication failed, retry with a new pass code"
        super().__init__(404, message)
