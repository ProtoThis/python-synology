"""Synology DSM tests."""
import pytest

from . import SynologyDSMMock
from . import USER_MAX_TRY
from . import VALID_HOST
from . import VALID_HTTPS
from . import VALID_PASSWORD
from . import VALID_PORT
from . import VALID_USER
from . import VALID_USER_2SA
from . import VALID_VERIFY_SSL
from synology_dsm.api.core.security import SynoCoreSecurity
from synology_dsm.api.core.share import SynoCoreShare
from synology_dsm.api.core.system import SynoCoreSystem
from synology_dsm.api.core.upgrade import SynoCoreUpgrade
from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.download_station import SynoDownloadStation
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.storage.storage import SynoStorage
from synology_dsm.api.surveillance_station import SynoSurveillanceStation
from synology_dsm.const import API_AUTH
from synology_dsm.const import API_INFO
from synology_dsm.exceptions import SynologyDSMAPIErrorException
from synology_dsm.exceptions import SynologyDSMAPINotExistsException
from synology_dsm.exceptions import SynologyDSMLogin2SAFailedException
from synology_dsm.exceptions import SynologyDSMLogin2SARequiredException
from synology_dsm.exceptions import SynologyDSMLoginFailedException
from synology_dsm.exceptions import SynologyDSMLoginInvalidException
from synology_dsm.exceptions import SynologyDSMRequestException


class TestSynologyDSM:
    """Common SynologyDSM 5 and 6 test cases."""

    def test_init(self, dsm):
        """Test init."""
        assert dsm.username
        assert dsm._base_url
        assert dsm._timeout == 10
        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

    @pytest.mark.parametrize("version", [5, 6])
    def test_login_basic_failed(self, version):
        """Test basic failed login."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            USER_MAX_TRY,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version

        with pytest.raises(SynologyDSMLoginFailedException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 407
        assert error_value["reason"] == "Max Tries (if auto blocking is set to true)"
        assert error_value["details"] == USER_MAX_TRY

    @pytest.mark.parametrize("version", [5, 6])
    def test_login_2sa_failed(self, version):
        """Test failed login with 2SA."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version

        with pytest.raises(SynologyDSMLogin2SARequiredException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 403
        assert error_value["reason"] == "One time password not specified"
        assert (
            error_value["details"]
            == "Two-step authentication required for account: valid_user_2sa"
        )

        with pytest.raises(SynologyDSMLogin2SAFailedException) as error:
            dsm.login(888888)
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 404
        assert error_value["reason"] == "One time password authenticate failed"
        assert (
            error_value["details"]
            == "Two-step authentication failed, retry with a new pass code"
        )

        assert dsm._session_id is None
        assert dsm._syno_token is None
        assert dsm._device_token is None

    @pytest.mark.parametrize("version", [5, 6])
    def test_connection_failed(self, version):
        """Test failed connection."""
        # No internet
        dsm = SynologyDSMMock(
            "no_internet",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMRequestException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            "ConnectionError = <urllib3.connection.VerifiedHTTPSConnection "
            in error_value["details"]
        )

        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

        # Wrong host
        dsm = SynologyDSMMock(
            "host",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMRequestException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            "ConnectionError = <urllib3.connection.HTTPConnection "
            in error_value["details"]
        )

        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

        # Wrong port
        dsm = SynologyDSMMock(
            VALID_HOST, 0, VALID_USER, VALID_PASSWORD, VALID_HTTPS, VALID_VERIFY_SSL
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMRequestException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert error_value["details"] == (
            "SSLError = [SSL: WRONG_VERSION_NUMBER] "
            "wrong version number (_ssl.c:1076)"
        )

        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

        # Wrong HTTPS
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            False,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMRequestException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert error_value["details"] == "RequestException = Bad request"

        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

        # Wrong SSL
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            False,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMRequestException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            error_value["details"]
            == f"SSLError = hostname '192.168.0.35' doesn't match '{VALID_HOST}'"
        )

        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

    @pytest.mark.parametrize("version", [5, 6])
    def test_login_failed(self, version):
        """Test failed login."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            "user",
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMLoginInvalidException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 400
        assert error_value["reason"] == "Invalid credentials"
        assert error_value["details"] == "Invalid password or not admin account: user"

        assert dsm.apis.get(API_AUTH)
        assert not dsm._session_id

        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            "pass",
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm.dsm_version = version
        with pytest.raises(SynologyDSMLoginInvalidException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 400
        assert error_value["reason"] == "Invalid credentials"
        assert (
            error_value["details"]
            == "Invalid password or not admin account: valid_user"
        )

        assert dsm.apis.get(API_AUTH)
        assert not dsm._session_id

    @pytest.mark.parametrize("version", [5, 6])
    def test_request_timeout(self, version):
        """Test request timeout."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
            timeout=2,
        )
        dsm.dsm_version = version
        assert dsm._timeout == 2

    def test_request_get(self, dsm):
        """Test get request."""
        assert dsm.get(API_INFO, "query")
        assert dsm.get(API_AUTH, "login")
        assert dsm.get("SYNO.DownloadStation2.Task", "list")
        assert dsm.get(API_AUTH, "logout")

    def test_request_get_failed(self, dsm):
        """Test failed get request."""
        with pytest.raises(SynologyDSMAPINotExistsException) as error:
            dsm.get("SYNO.Virtualization.API.Task.Info", "list")
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.Virtualization.API.Task.Info"
        assert error_value["code"] == -2
        assert error_value["reason"] == "Unknown"
        assert (
            error_value["details"]
            == "API SYNO.Virtualization.API.Task.Info does not exists"
        )

    def test_request_post(self, dsm):
        """Test post request."""
        assert dsm.post(
            "SYNO.FileStation.Upload",
            "upload",
            params={"dest_folder_path": "/upload/test", "create_parents": True},
            files={"file": "open('file.txt','rb')"},
        )

        assert dsm.post(
            "SYNO.DownloadStation2.Task",
            "create",
            params={
                "uri": "ftps://192.0.0.1:21/test/test.zip",
                "username": "admin",
                "password": "1234",
            },
        )

    def test_request_post_failed(self, dsm):
        """Test failed post request."""
        with pytest.raises(SynologyDSMAPIErrorException) as error:
            dsm.post(
                "SYNO.FileStation.Upload",
                "upload",
                params={"dest_folder_path": "/upload/test", "create_parents": True},
                files={"file": "open('file_already_exists.txt','rb')"},
            )
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.FileStation.Upload"
        assert error_value["code"] == 1805
        assert error_value["reason"] == (
            "Can’t overwrite or skip the existed file, if no overwrite"
            " parameter is given"
        )
        assert not error_value["details"]

        with pytest.raises(SynologyDSMAPIErrorException) as error:
            dsm.post(
                "SYNO.DownloadStation2.Task",
                "create",
                params={
                    "uri": "ftps://192.0.0.1:21/test/test_not_exists.zip",
                    "username": "admin",
                    "password": "1234",
                },
            )
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.DownloadStation2.Task"
        assert error_value["code"] == 408
        assert error_value["reason"] == "File does not exist"
        assert not error_value["details"]

    def test_reset_str_attr(self, dsm):
        """Test reset with string attr."""
        assert not dsm._security
        assert dsm.security
        assert dsm._security
        assert dsm.reset("security")
        assert not dsm._security

        assert not dsm._share
        assert dsm.share
        assert dsm._share
        assert dsm.reset("share")
        assert not dsm._share

        assert not dsm._system
        assert dsm.system
        assert dsm._system
        assert dsm.reset("system")
        assert not dsm._system

        assert not dsm._upgrade
        assert dsm.upgrade
        assert dsm._upgrade
        assert dsm.reset("upgrade")
        assert not dsm._upgrade

        assert not dsm._utilisation
        assert dsm.utilisation
        assert dsm._utilisation
        assert dsm.reset("utilisation")
        assert not dsm._utilisation

        assert not dsm._download
        assert dsm.download_station
        assert dsm._download
        assert dsm.reset("download")
        assert not dsm._download

        assert not dsm._storage
        assert dsm.storage
        assert dsm._storage
        assert dsm.reset("storage")
        assert not dsm._storage

        assert not dsm._surveillance
        assert dsm.surveillance_station
        assert dsm._surveillance
        assert dsm.reset("surveillance")
        assert not dsm._surveillance

    def test_reset_str_key(self, dsm):
        """Test reset with string API key."""
        assert not dsm._security
        assert dsm.security
        assert dsm._security
        assert dsm.reset(SynoCoreSecurity.API_KEY)
        assert not dsm._security

        assert not dsm._share
        assert dsm.share
        assert dsm._share
        assert dsm.reset(SynoCoreShare.API_KEY)
        assert not dsm._share

        assert not dsm._system
        assert dsm.system
        assert dsm._system
        assert dsm.reset(SynoCoreSystem.API_KEY)
        assert not dsm._system

        assert not dsm._upgrade
        assert dsm.upgrade
        assert dsm._upgrade
        assert dsm.reset(SynoCoreUpgrade.API_KEY)
        assert not dsm._upgrade

        assert not dsm._utilisation
        assert dsm.utilisation
        assert dsm._utilisation
        assert dsm.reset(SynoCoreUtilization.API_KEY)
        assert not dsm._utilisation

        assert not dsm._download
        assert dsm.download_station
        assert dsm._download
        assert dsm.reset(SynoDownloadStation.API_KEY)
        assert not dsm._download

        assert not dsm._storage
        assert dsm.storage
        assert dsm._storage
        assert dsm.reset(SynoStorage.API_KEY)
        assert not dsm._storage

        assert not dsm._surveillance
        assert dsm.surveillance_station
        assert dsm._surveillance
        assert dsm.reset(SynoSurveillanceStation.API_KEY)
        assert not dsm._surveillance

    def test_reset_object(self, dsm):
        """Test reset with object."""
        assert not dsm._security
        assert dsm.security
        assert dsm._security
        assert dsm.reset(dsm.security)
        assert not dsm._security

        assert not dsm._share
        assert dsm.share
        assert dsm._share
        assert dsm.reset(dsm.share)
        assert not dsm._share

        assert not dsm._system
        assert dsm.system
        assert dsm._system
        assert dsm.reset(dsm.system)
        assert not dsm._system

        assert not dsm._upgrade
        assert dsm.upgrade
        assert dsm._upgrade
        assert dsm.reset(dsm.upgrade)
        assert not dsm._upgrade

        assert not dsm._utilisation
        assert dsm.utilisation
        assert dsm._utilisation
        assert dsm.reset(dsm.utilisation)
        assert not dsm._utilisation

        assert not dsm._download
        assert dsm.download_station
        assert dsm._download
        assert dsm.reset(dsm.download_station)
        assert not dsm._download

        assert not dsm._storage
        assert dsm.storage
        assert dsm._storage
        assert dsm.reset(dsm.storage)
        assert not dsm._storage

        assert not dsm._surveillance
        assert dsm.surveillance_station
        assert dsm._surveillance
        assert dsm.reset(dsm.surveillance_station)
        assert not dsm._surveillance

    def test_reset_str_attr_information(self, dsm):
        """Test reset with string information attr (should not be reset)."""
        assert not dsm._information
        assert dsm.information
        assert dsm._information
        assert not dsm.reset("information")
        assert dsm._information

    def test_reset_str_key_information(self, dsm):
        """Test reset with string information API key (should not be reset)."""
        assert not dsm._information
        assert dsm.information
        assert dsm._information
        assert not dsm.reset(SynoDSMInformation.API_KEY)
        assert dsm._information

    def test_reset_object_information(self, dsm):
        """Test reset with information object (should not be reset)."""
        assert not dsm._information
        assert dsm.information
        assert dsm._information
        assert not dsm.reset(dsm.information)
        assert dsm._information

    def test_utilisation(self, dsm):
        """Test utilisation."""
        assert dsm.utilisation
        dsm.utilisation.update()

    def test_utilisation_cpu(self, dsm):
        """Test utilisation CPU."""
        dsm.utilisation.update()
        assert dsm.utilisation.cpu
        assert dsm.utilisation.cpu_other_load
        assert dsm.utilisation.cpu_user_load
        assert dsm.utilisation.cpu_system_load
        assert dsm.utilisation.cpu_total_load
        assert dsm.utilisation.cpu_1min_load
        assert dsm.utilisation.cpu_5min_load
        assert dsm.utilisation.cpu_15min_load

    def test_utilisation_error(self, dsm):
        """Test utilisation error."""
        dsm.error = True
        with pytest.raises(SynologyDSMAPIErrorException) as error:
            dsm.utilisation.update()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.Core.System.Utilization"
        assert error_value["code"] == 1055
        assert error_value["reason"] == "Unknown"
        assert error_value["details"] == {
            "err_key": "",
            "err_line": 883,
            "err_msg": "Transmition failed.",
            "err_session": "",
        }

    def test_utilisation_memory(self, dsm):
        """Test utilisation memory."""
        dsm.utilisation.update()
        assert dsm.utilisation.memory
        assert dsm.utilisation.memory_real_usage
        assert dsm.utilisation.memory_size()
        assert dsm.utilisation.memory_size(True)
        assert dsm.utilisation.memory_available_swap()
        assert dsm.utilisation.memory_available_swap(True)
        assert dsm.utilisation.memory_cached()
        assert dsm.utilisation.memory_cached(True)
        assert dsm.utilisation.memory_available_real()
        assert dsm.utilisation.memory_available_real(True)
        assert dsm.utilisation.memory_total_real()
        assert dsm.utilisation.memory_total_real(True)
        assert dsm.utilisation.memory_total_swap()
        assert dsm.utilisation.memory_total_swap(True)

    def test_utilisation_network(self, dsm):
        """Test utilisation network."""
        dsm.utilisation.update()
        assert dsm.utilisation.network
        assert dsm.utilisation.network_up()
        assert dsm.utilisation.network_up(True)
        assert dsm.utilisation.network_down()
        assert dsm.utilisation.network_down(True)
