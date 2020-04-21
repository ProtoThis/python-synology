# -*- coding: utf-8 -*-
"""Library exceptions."""
from .const import ERROR_AUTH, ERROR_COMMON, ERROR_DOWNLOAD_SEARCH, ERROR_DOWNLOAD_TASK, ERROR_FILE, ERROR_SURVEILLANCE, ERROR_VIRTUALIZATION

class SynologyDSMException(Exception):
    """Generic Synology DSM exception."""
    pass

# Request
class SynologyDSMRequestException(SynologyDSMException):
    """Request exception."""
    def __init__(self, exception):
        ex_class = exception.__class__.__name__
        ex_reason = exception.args[0]
        if hasattr(exception.args[0], "reason"):
            ex_reason = exception.args[0].reason
        message = "%s = %s" % (ex_class, ex_reason)
        super(SynologyDSMRequestException, self).__init__(message)

# API
class SynologyDSMAPINotExistsException(SynologyDSMException):
    """API not exists exception."""
    def __init__(self, api):
        message = "API %s does not exists" % api
        super(SynologyDSMAPINotExistsException, self).__init__(message)

class SynologyDSMAPIErrorException(SynologyDSMException):
    """API returns an error exception."""
    def __init__(self, api, code):
        reason = ERROR_COMMON.get(code)
        if api and not reason:
            if api == "SYNO.API.Auth":
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
        message = "\n Code: %s\n Reason: %s" % (str(code), reason)
        super(SynologyDSMAPIErrorException, self).__init__(message)

# Login
class SynologyDSMLoginFailedException(SynologyDSMException):
    """Failed to login exception."""
    pass


class SynologyDSMLoginInvalidException(SynologyDSMLoginFailedException):
    """Invalid password & not admin account exception."""
    def __init__(self, username):
        message = "Invalid password or not admin account: %s" % username
        super(SynologyDSMLoginInvalidException, self).__init__(message)


class SynologyDSMLoginDisabledAccountException(SynologyDSMLoginFailedException):
    """Guest & disabled account exception."""
    def __init__(self, username):
        message = "Guest or disabled account: %s" % username
        super(SynologyDSMLoginDisabledAccountException, self).__init__(message)


class SynologyDSMLoginPermissionDeniedException(SynologyDSMLoginFailedException):
    """No access to login exception."""
    def __init__(self, username):
        message = "Permission denied for account: %s" % username
        super(SynologyDSMLoginPermissionDeniedException, self).__init__(message)


class SynologyDSMLogin2SARequiredException(SynologyDSMLoginFailedException):
    """2SA required to login exception."""
    def __init__(self, username):
        message = "Two-step authentication required for account: %s" % username
        super(SynologyDSMLogin2SARequiredException, self).__init__(message)


class SynologyDSMLogin2SAFailedException(SynologyDSMLoginFailedException):
    """2SA code failed exception."""
    def __init__(self):
        message = "Two-step authentication failed, retry with a new pass code"
        super(SynologyDSMLogin2SAFailedException, self).__init__(message)
