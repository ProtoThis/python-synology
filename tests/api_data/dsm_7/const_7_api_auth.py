"""DSM 7 SYNO.API.Auth data."""
from tests.const import DEVICE_TOKEN
from tests.const import ERROR_AUTH_OTP_NOT_SPECIFIED
from tests.const import SESSION_ID
from tests.const import SYNO_TOKEN


DSM_7_AUTH_LOGIN = {
    "data": {"is_portal_port": False, "sid": SESSION_ID, "synotoken": SYNO_TOKEN},
    "success": True,
}
DSM_7_AUTH_LOGIN_2SA = ERROR_AUTH_OTP_NOT_SPECIFIED
DSM_7_AUTH_LOGIN_2SA_OTP = {
    "data": {
        "device_id": DEVICE_TOKEN,
        "is_portal_port": False,
        "sid": SESSION_ID,
        "synotoken": SYNO_TOKEN,
    },
    "success": True,
}

DSM_7_AUTH_LOGOUT = {"success": True}
