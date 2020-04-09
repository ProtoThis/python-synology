# -*- coding: utf-8 -*-
"""Library tests."""
from synology_dsm import SynologyDSM

from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.storage.storage import SynoStorage

from .const_dsm_6 import (
    DSM_6_LOGIN,
    DSM_6_INFORMATION,
    DSM_6_UTILIZATION,
    DSM_6_STORAGE,
)

VALID_DSM_HOST = "nas.mywebsite.me"
VALID_DSM_PORT = "443"
VALID_USER = "valid_user"
VALID_PASSWORD = "valid_password"


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
            debugmode,
            dsm_version,
        )

    def _execute_get_url(self, request_url, append_sid=True):
        if VALID_DSM_HOST not in request_url or VALID_DSM_PORT not in request_url:
            return None

        if (
            self.LOGIN_URI in request_url
            and VALID_USER in request_url
            and VALID_PASSWORD in request_url
        ):
            return DSM_6_LOGIN

        if self.API_URI in request_url:
            if SynoDSMInformation.API_KEY in request_url:
                return DSM_6_INFORMATION
            if SynoCoreUtilization.API_KEY in request_url:
                return DSM_6_UTILIZATION
            if SynoStorage.API_KEY in request_url:
                return DSM_6_STORAGE

        return None
