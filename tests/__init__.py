# -*- coding: utf-8 -*-
"""Library tests."""
from synology_dsm import SynologyDSM
from synology_dsm.exceptions import SynologyDSMRequestException
from simplejson.errors import JSONDecodeError

from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.storage.storage import SynoStorage

from .const import (
    DSM_INSUFFICIENT_USER_PRIVILEGE,
    DSM_AUTH_OTP_AUTHENTICATE_FAILED,
    DEVICE_TOKEN,
)
from .api_data.dsm_6 import (
    DSM_6_API_INFO,
    DSM_6_AUTH_LOGIN,
    DSM_6_AUTH_LOGIN_2SA,
    DSM_6_AUTH_LOGIN_2SA_OTP,
    DSM_6_DSM_INFORMATION,
    DSM_6_CORE_UTILIZATION,
    DSM_6_STORAGE_STORAGE,
)

VALID_DSM_HOST = "nas.mywebsite.me"
VALID_DSM_PORT = "443"
VALID_USER = "valid_user"
VALID_USER_2SA = "valid_user_2sa"
VALID_PASSWORD = "valid_password"
VALID_OTP = "123456"


class SynologyDSMMock(SynologyDSM):
    """Mocked SynologyDSM."""

    API_URI = "entry.cgi"

    def __init__(
        self,
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        device_token=None,
        debugmode=False,
    ):
        SynologyDSM.__init__(
            self,
            dsm_ip,
            dsm_port,
            username,
            password,
            use_https,
            device_token,
            debugmode,
        )

    def _execute_request(self, request_url):
        if VALID_DSM_HOST not in request_url or VALID_DSM_PORT not in request_url:
            raise SynologyDSMRequestException(JSONDecodeError("test", "doc", 0, 1))

        if self.API_INFO in request_url:
            return DSM_6_API_INFO

        if self.API_AUTH in request_url:
            if VALID_USER_2SA in request_url and VALID_PASSWORD in request_url:
                if "otp_code" not in request_url and "device_id" not in request_url:
                    return DSM_6_AUTH_LOGIN_2SA

                if "device_id" in request_url and DEVICE_TOKEN in request_url:
                    return DSM_6_AUTH_LOGIN

                if "otp_code" in request_url:
                    if VALID_OTP in request_url:
                        return DSM_6_AUTH_LOGIN_2SA_OTP
                    return DSM_AUTH_OTP_AUTHENTICATE_FAILED

            if VALID_USER in request_url and VALID_PASSWORD in request_url:
                return DSM_6_AUTH_LOGIN

        if self.API_URI in request_url:
            if not self._session_id or not self._syno_token:
                return DSM_INSUFFICIENT_USER_PRIVILEGE

            if SynoDSMInformation.API_KEY in request_url:
                return DSM_6_DSM_INFORMATION

            if SynoCoreUtilization.API_KEY in request_url:
                return DSM_6_CORE_UTILIZATION

            if SynoStorage.API_KEY in request_url:
                return DSM_6_STORAGE_STORAGE

        return None
