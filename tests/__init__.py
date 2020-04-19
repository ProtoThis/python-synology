# -*- coding: utf-8 -*-
"""Library tests."""
from simplejson.errors import JSONDecodeError
from requests.exceptions import ConnectionError as ConnError, RequestException, SSLError

from synology_dsm import SynologyDSM
from synology_dsm.exceptions import SynologyDSMRequestException
from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.storage.storage import SynoStorage

from .const import (
    ERROR_INSUFFICIENT_USER_PRIVILEGE,
    ERROR_AUTH_INVALID_CREDENTIALS,
    ERROR_AUTH_OTP_AUTHENTICATE_FAILED,
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

VALID_HOST = "nas.mywebsite.me"
VALID_PORT = "443"
VALID_SSL = True
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
        if "no_internet" in request_url:
            raise SynologyDSMRequestException(
                ConnError(
                    "<urllib3.connection.VerifiedHTTPSConnection object at 0x106c1f250>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known"
                )
            )

        if VALID_HOST not in request_url:
            raise SynologyDSMRequestException(
                ConnError(
                    "<urllib3.connection.HTTPConnection object at 0x10d6f8090>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known"
                )
            )

        if VALID_PORT not in request_url and "https" not in request_url:
            raise SynologyDSMRequestException(
                JSONDecodeError("Expecting value", "<html>document</html>", 0, None)
            )

        if VALID_PORT not in request_url:
            raise SynologyDSMRequestException(
                SSLError(
                    "[SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1076)"
                )
            )

        if "https" not in request_url:
            raise SynologyDSMRequestException(RequestException("Bad request"))

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
                    return ERROR_AUTH_OTP_AUTHENTICATE_FAILED

            if VALID_USER in request_url and VALID_PASSWORD in request_url:
                return DSM_6_AUTH_LOGIN

            return ERROR_AUTH_INVALID_CREDENTIALS

        if self.API_URI in request_url:
            if not self._session_id or not self._syno_token:
                return ERROR_INSUFFICIENT_USER_PRIVILEGE

            if SynoDSMInformation.API_KEY in request_url:
                return DSM_6_DSM_INFORMATION

            if SynoCoreUtilization.API_KEY in request_url:
                return DSM_6_CORE_UTILIZATION

            if SynoStorage.API_KEY in request_url:
                return DSM_6_STORAGE_STORAGE

        return None
