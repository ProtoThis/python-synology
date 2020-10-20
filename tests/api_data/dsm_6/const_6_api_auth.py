"""DSM 6 SYNO.API.Auth data."""
from tests.const import (
    SESSION_ID,
    DEVICE_TOKEN,
    SYNO_TOKEN,
    ERROR_AUTH_OTP_NOT_SPECIFIED,
)


DSM_6_AUTH_LOGIN = {
    "data": {"is_portal_port": False, "sid": SESSION_ID, "synotoken": SYNO_TOKEN},
    "success": True,
}
DSM_6_AUTH_LOGIN_2SA = ERROR_AUTH_OTP_NOT_SPECIFIED
DSM_6_AUTH_LOGIN_2SA_OTP = {
    "data": {
        "did": DEVICE_TOKEN,
        "is_portal_port": False,
        "sid": SESSION_ID,
        "synotoken": SYNO_TOKEN,
    },
    "success": True,
}

DSM_6_AUTH_LOGOUT = {"success": True}
