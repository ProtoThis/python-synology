"""Test constants."""
# API test data are localized in
# `tests/api_data/dsm_[dsm_major_version]`
# Data constant names should be like :
# "DSM_[dsm_version]_[API_KEY]"
# if data failed, add "_FAILED"

SESSION_ID = "session_id"
SYNO_TOKEN = "Syñ0_T0k€ñ"
DEVICE_TOKEN = "Dév!cè_T0k€ñ"
UNIQUE_KEY = "1x2X3x!_UK"

# Common API error code
ERROR_UNKNOWN = {"error": {"code": 100}, "success": False}
ERROR_INVALID_PARAMETERS = {"error": {"code": 101}, "success": False}
ERROR_API_NOT_EXISTS = {"error": {"code": 102}, "success": False}
ERROR_API_METHOD_NOT_EXISTS = {"error": {"code": 103}, "success": False}
ERROR_API_VERSION_NOT_SUPPORTED = {"error": {"code": 104}, "success": False}
ERROR_INSUFFICIENT_USER_PRIVILEGE = {"error": {"code": 105}, "success": False}
ERROR_CONNECTION_TIME_OUT = {"error": {"code": 106}, "success": False}
ERROR_MULTIPLE_LOGIN_DETECTED = {"error": {"code": 107}, "success": False}

# Auth API error code
ERROR_AUTH_INVALID_CREDENTIALS = {"error": {"code": 400}, "success": False}
ERROR_AUTH_GUEST_OR_DISABLED_ACCOUNT = {"error": {"code": 401}, "success": False}
ERROR_AUTH_PERMISSION_DENIED = {"error": {"code": 402}, "success": False}
ERROR_AUTH_OTP_NOT_SPECIFIED = {"error": {"code": 403}, "success": False}
ERROR_AUTH_OTP_AUTHENTICATE_FAILED = {"error": {"code": 404}, "success": False}
ERROR_AUTH_INCORRECT_APP_PORTAL = {"error": {"code": 405}, "success": False}
ERROR_AUTH_OTP_CODE_ENFORCED = {"error": {"code": 406}, "success": False}
ERROR_AUTH_MAX_TRIES = {"error": {"code": 407}, "success": False}
