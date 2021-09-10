"""Synology DSM tests."""
import pytest

from . import SynologyDSMMock
from . import VALID_HOST
from . import VALID_HTTPS
from . import VALID_OTP
from . import VALID_PASSWORD
from . import VALID_PORT
from . import VALID_USER_2SA
from . import VALID_VERIFY_SSL
from .const import DEVICE_TOKEN
from .const import SESSION_ID
from .const import SYNO_TOKEN
from synology_dsm.const import API_AUTH
from synology_dsm.exceptions import SynologyDSMLogin2SARequiredException


class TestSynologyDSM7:
    """SynologyDSM 7 test cases."""

    def test_login(self, dsm_7):
        """Test login."""
        assert dsm_7.login()
        assert dsm_7.apis.get(API_AUTH)
        assert dsm_7._session_id == SESSION_ID
        assert dsm_7._syno_token == SYNO_TOKEN

    def test_login_2sa(self):
        """Test login with 2SA."""
        dsm_7 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_7.dsm_version = 7
        with pytest.raises(SynologyDSMLogin2SARequiredException) as error:
            dsm_7.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 403
        assert error_value["reason"] == "One time password not specified"
        assert (
            error_value["details"]
            == "Two-step authentication required for account: valid_user_2sa"
        )

        assert dsm_7.login(VALID_OTP)

        assert dsm_7._session_id == SESSION_ID
        assert dsm_7._syno_token == SYNO_TOKEN
        assert dsm_7._device_token == DEVICE_TOKEN
        assert dsm_7.device_token == DEVICE_TOKEN

    def test_login_2sa_new_session(self):
        """Test login with 2SA and a new session with granted device."""
        dsm_7 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
            device_token=DEVICE_TOKEN,
        )
        dsm_7.dsm_version = 7
        assert dsm_7.login()

        assert dsm_7._session_id == SESSION_ID
        assert dsm_7._syno_token == SYNO_TOKEN
        assert dsm_7._device_token == DEVICE_TOKEN
        assert dsm_7.device_token == DEVICE_TOKEN
