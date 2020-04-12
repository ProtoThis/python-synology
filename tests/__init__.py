# -*- coding: utf-8 -*-
"""Library tests."""
from synology_dsm import SynologyDSM

from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.storage.storage import SynoStorage

from .const import DSM_INSUFFICIENT_USER_PRIVILEGE, DSM_AUTH_OTP_AUTHENTICATE_FAILED
from .const_dsm_6 import (
    DSM_6_LOGIN,
    DSM_6_LOGIN_2SA,
    DSM_6_LOGIN_2SA_OTP,
    DSM_6_INFORMATION,
    DSM_6_UTILIZATION,
    DSM_6_STORAGE,
)

VALID_DSM_HOST = "nas.mywebsite.me"
VALID_DSM_PORT = "443"
VALID_USER = "valid_user"
VALID_USER_2SA = "valid_user_2sa"
VALID_PASSWORD = "valid_password"
VALID_OTP = "123456"


class SynologyDSMMock(SynologyDSM):
    """Mocked SynologyDSM."""

    LOGIN_URI = "auth.cgi"
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
        dsm_version=6,
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
            dsm_version,
        )

    def _execute_get_url(self, request_url):
        if VALID_DSM_HOST not in request_url or VALID_DSM_PORT not in request_url:
            return None

        if self.LOGIN_URI in request_url:
            if (
                VALID_USER_2SA in request_url
                and VALID_PASSWORD in request_url
                and "otp_code" not in request_url
            ):
                return DSM_6_LOGIN_2SA
            if (
                VALID_USER_2SA in request_url
                and VALID_PASSWORD in request_url
                and "otp_code" in request_url
            ):
                if VALID_OTP in request_url:
                    return DSM_6_LOGIN_2SA_OTP
                return DSM_AUTH_OTP_AUTHENTICATE_FAILED
            if VALID_USER in request_url and VALID_PASSWORD in request_url:
                return DSM_6_LOGIN

        elif self.API_URI in request_url:
            if not self._session_id or not self._syno_token:
                return DSM_INSUFFICIENT_USER_PRIVILEGE

            if SynoDSMInformation.API_KEY in request_url:
                return DSM_6_INFORMATION
            if SynoCoreUtilization.API_KEY in request_url:
                return DSM_6_UTILIZATION
            if SynoStorage.API_KEY in request_url:
                return DSM_6_STORAGE

        return None
