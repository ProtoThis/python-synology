# -*- coding: utf-8 -*-
"""Test constants."""

# Name constants like this :
# "DSM_[dsm_version]_[API_KEY]"
# if data failed, add "_FAILED"

SESSION_ID = "session_id"
SYNO_TOKEN = "syno_token"
DEVICE_ID = "device_id"
SERIAL = "1x2X3x!_SN"
UNIQUE_KEY = "1x2X3x!_UK"

# Common API error code
DSM_UNKNOWN_ERROR = {"error": {"code": 100}, "success": False}
DSM_INVALID_PARAMETERS = {"error": {"code": 101}, "success": False}
DSM_API_NOT_EXISTS = {"error": {"code": 102}, "success": False}
DSM_API_METHOD_NOT_EXISTS = {"error": {"code": 103}, "success": False}
DSM_API_VERSION_NOT_SUPPORTED = {"error": {"code": 104}, "success": False}
DSM_INSUFFICIENT_USER_PRIVILEGE = {"error": {"code": 105}, "success": False}
DSM_CONNECTION_TIME_OUT = {"error": {"code": 106}, "success": False}
DSM_MULTIPLE_LOGIN_DETECTED = {"error": {"code": 107}, "success": False}

# Auth API error code
DSM_AUTH_INVALID_PASSWORD = {"error": {"code": 400}, "success": False}
DSM_AUTH_GUEST_OR_DISABLED_ACCOUNT = {"error": {"code": 401}, "success": False}
DSM_AUTH_PERMISSION_DENIED = {"error": {"code": 402}, "success": False}
DSM_AUTH_OTP_NOT_SPECIFIED = {"error": {"code": 403}, "success": False}
DSM_AUTH_OTP_AUTHENTICATE_FAILED = {"error": {"code": 404}, "success": False}
DSM_AUTH_INCORRECT_APP_PORTAL = {"error": {"code": 405}, "success": False}
DSM_AUTH_OTP_CODE_ENFORCED = {"error": {"code": 406}, "success": False}
DSM_AUTH_MAX_TRIES = {"error": {"code": 407}, "success": False}
