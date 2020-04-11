# -*- coding: utf-8 -*-
"""Library exceptions."""


class SynologyDSMException(Exception):
    """Generic Synology DSM exception."""
    pass


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
