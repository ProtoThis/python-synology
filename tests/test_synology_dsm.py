"""Synology DSM tests."""
import pytest

from . import SynologyDSMMock
from . import USER_MAX_TRY
from . import VALID_HOST
from . import VALID_HTTPS
from . import VALID_OTP
from . import VALID_PASSWORD
from . import VALID_PORT
from . import VALID_USER
from . import VALID_USER_2SA
from . import VALID_VERIFY_SSL
from .const import DEVICE_TOKEN
from .const import SESSION_ID
from .const import SYNO_TOKEN
from synology_dsm.api.core.security import SynoCoreSecurity
from synology_dsm.api.dsm.information import SynoDSMInformation
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
    """SynologyDSM test cases."""

    def test_init(self, dsm):
        """Test init."""
        assert dsm.username
        assert dsm._base_url
        assert dsm._timeout == 10
        assert not dsm.apis.get(API_AUTH)
        assert not dsm._session_id

    def test_connection_failed(self, dsm):
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

    def test_login(self, dsm):
        """Test login."""
        assert dsm.login()
        assert dsm.apis.get(API_AUTH)
        assert dsm._session_id == SESSION_ID
        assert dsm._syno_token == SYNO_TOKEN

    def test_login_failed(self):
        """Test failed login."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            "user",
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
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

    def test_login_2sa(self):
        """Test login with 2SA."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )

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

        assert dsm.login(VALID_OTP)

        assert dsm._session_id == SESSION_ID
        assert dsm._syno_token == SYNO_TOKEN
        assert dsm._device_token == DEVICE_TOKEN
        assert dsm.device_token == DEVICE_TOKEN

    def test_login_2sa_new_session(self):
        """Test login with 2SA and a new session with granted device."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
            device_token=DEVICE_TOKEN,
        )
        assert dsm.login()

        assert dsm._session_id == SESSION_ID
        assert dsm._syno_token == SYNO_TOKEN
        assert dsm._device_token == DEVICE_TOKEN
        assert dsm.device_token == DEVICE_TOKEN

    def test_login_2sa_failed(self):
        """Test failed login with 2SA."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )

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

    def test_login_basic_failed(self):
        """Test basic failed login."""
        dsm = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            USER_MAX_TRY,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )

        with pytest.raises(SynologyDSMLoginFailedException) as error:
            dsm.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 407
        assert error_value["reason"] == "Max Tries (if auto blocking is set to true)"
        assert error_value["details"] == USER_MAX_TRY

    def test_request_timeout(self):
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

    def test_reset_str_key(self, dsm):
        """Test reset with string API key."""
        assert not dsm._security
        assert dsm.security
        assert dsm._security
        assert dsm.reset(SynoCoreSecurity.API_KEY)
        assert not dsm._security

    def test_reset_object(self, dsm):
        """Test reset with object."""
        assert not dsm._security
        assert dsm.security
        assert dsm._security
        assert dsm.reset(dsm.security)
        assert not dsm._security

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

    def test_information(self, dsm):
        """Test information."""
        assert dsm.information
        dsm.information.update()
        assert dsm.information.model == "DS918+"
        assert dsm.information.ram == 4096
        assert dsm.information.serial == "1920PDN001501"
        assert dsm.information.temperature == 40
        assert not dsm.information.temperature_warn
        assert dsm.information.uptime == 155084
        assert dsm.information.version == "24922"
        assert dsm.information.version_string == "DSM 6.2.2-24922 Update 4"

    def test_network(self, dsm):
        """Test network."""
        assert dsm.network
        dsm.network.update()
        assert dsm.network.dns
        assert dsm.network.gateway
        assert dsm.network.hostname
        assert dsm.network.interfaces
        assert dsm.network.interface("eth0")
        assert dsm.network.interface("eth1")
        assert dsm.network.macs
        assert dsm.network.workgroup

    def test_security(self, dsm):
        """Test security, safe status."""
        assert dsm.security
        dsm.security.update()
        assert dsm.security.checks
        assert dsm.security.last_scan_time
        assert not dsm.security.start_time  # Finished scan
        assert dsm.security.success
        assert dsm.security.progress
        assert dsm.security.status == "safe"
        assert dsm.security.status_by_check
        assert dsm.security.status_by_check["malware"] == "safe"
        assert dsm.security.status_by_check["network"] == "safe"
        assert dsm.security.status_by_check["securitySetting"] == "safe"
        assert dsm.security.status_by_check["systemCheck"] == "safe"
        assert dsm.security.status_by_check["update"] == "safe"
        assert dsm.security.status_by_check["userInfo"] == "safe"

    def test_security_error(self, dsm):
        """Test security, outOfDate status."""
        dsm.error = True
        assert dsm.security
        dsm.security.update()
        assert dsm.security.checks
        assert dsm.security.last_scan_time
        assert not dsm.security.start_time  # Finished scan
        assert dsm.security.success
        assert dsm.security.progress
        assert dsm.security.status == "outOfDate"
        assert dsm.security.status_by_check
        assert dsm.security.status_by_check["malware"] == "safe"
        assert dsm.security.status_by_check["network"] == "safe"
        assert dsm.security.status_by_check["securitySetting"] == "safe"
        assert dsm.security.status_by_check["systemCheck"] == "safe"
        assert dsm.security.status_by_check["update"] == "outOfDate"
        assert dsm.security.status_by_check["userInfo"] == "safe"

    def test_shares(self, dsm):
        """Test shares."""
        assert dsm.share
        dsm.share.update()
        assert dsm.share.shares
        for share_uuid in dsm.share.shares_uuids:
            assert dsm.share.share_name(share_uuid)
            assert dsm.share.share_path(share_uuid)
            assert dsm.share.share_recycle_bin(share_uuid) is not None
            assert dsm.share.share_size(share_uuid) is not None
            assert dsm.share.share_size(share_uuid, human_readable=True)

        assert (
            dsm.share.share_name("2ee6c06a-8766-48b5-013d-63b18652a393") == "test_share"
        )
        assert (
            dsm.share.share_path("2ee6c06a-8766-48b5-013d-63b18652a393") == "/volume1"
        )
        assert (
            dsm.share.share_recycle_bin("2ee6c06a-8766-48b5-013d-63b18652a393") is True
        )
        assert (
            dsm.share.share_size("2ee6c06a-8766-48b5-013d-63b18652a393")
            == 3.790251876432216e19
        )
        assert (
            dsm.share.share_size("2ee6c06a-8766-48b5-013d-63b18652a393", True)
            == "32.9Eb"
        )

    def test_system(self, dsm):
        """Test system."""
        assert dsm.system
        dsm.system.update()
        assert dsm.system.cpu_clock_speed
        assert dsm.system.cpu_cores
        assert dsm.system.cpu_family
        assert dsm.system.cpu_series
        assert dsm.system.firmware_ver
        assert dsm.system.model
        assert dsm.system.ram_size
        assert dsm.system.serial
        assert dsm.system.sys_temp
        assert dsm.system.time
        assert dsm.system.time_zone
        assert dsm.system.time_zone_desc
        assert dsm.system.up_time
        for usb_dev in dsm.system.usb_dev:
            assert usb_dev.get("cls")
            assert usb_dev.get("pid")
            assert usb_dev.get("producer")
            assert usb_dev.get("product")
            assert usb_dev.get("rev")
            assert usb_dev.get("vid")

    def test_upgrade(self, dsm):
        """Test upgrade."""
        assert dsm.upgrade
        dsm.upgrade.update()
        assert dsm.upgrade.update_available
        assert dsm.upgrade.available_version == "DSM 6.2.3-25426 Update 2"
        assert dsm.upgrade.reboot_needed == "now"
        assert dsm.upgrade.service_restarts == "some"

    def test_utilisation(self, dsm):
        """Test utilisation."""
        assert dsm.utilisation
        dsm.utilisation.update()

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

    def test_storage(self, dsm):
        """Test storage roots."""
        assert dsm.storage
        dsm.storage.update()
        assert dsm.storage.disks
        assert dsm.storage.env
        assert dsm.storage.storage_pools
        assert dsm.storage.volumes

    def test_storage_raid_volumes(self, dsm):
        """Test RAID storage volumes."""
        dsm.storage.update()
        # Basics
        assert dsm.storage.volumes_ids
        for volume_id in dsm.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert dsm.storage.volume_status(volume_id)
            assert dsm.storage.volume_device_type(volume_id)
            assert dsm.storage.volume_size_total(volume_id)
            assert dsm.storage.volume_size_total(volume_id, True)
            assert dsm.storage.volume_size_used(volume_id)
            assert dsm.storage.volume_size_used(volume_id, True)
            assert dsm.storage.volume_percentage_used(volume_id)
            assert dsm.storage.volume_disk_temp_avg(volume_id)
            assert dsm.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm.storage.volume_status("volume_1") == "normal"
        assert dsm.storage.volume_device_type("volume_1") == "raid_5"
        assert dsm.storage.volume_size_total("volume_1") == 7672030584832
        assert dsm.storage.volume_size_total("volume_1", True) == "7.0Tb"
        assert dsm.storage.volume_size_used("volume_1") == 4377452806144
        assert dsm.storage.volume_size_used("volume_1", True) == "4.0Tb"
        assert dsm.storage.volume_percentage_used("volume_1") == 57.1
        assert dsm.storage.volume_disk_temp_avg("volume_1") == 24.0
        assert dsm.storage.volume_disk_temp_max("volume_1") == 24

        # Non existing volume
        assert not dsm.storage.volume_status("not_a_volume")
        assert not dsm.storage.volume_device_type("not_a_volume")
        assert not dsm.storage.volume_size_total("not_a_volume")
        assert not dsm.storage.volume_size_total("not_a_volume", True)
        assert not dsm.storage.volume_size_used("not_a_volume")
        assert not dsm.storage.volume_size_used("not_a_volume", True)
        assert not dsm.storage.volume_percentage_used("not_a_volume")
        assert not dsm.storage.volume_disk_temp_avg("not_a_volume")
        assert not dsm.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert dsm.storage.volume_status("test_volume") is None
        assert dsm.storage.volume_device_type("test_volume") is None
        assert dsm.storage.volume_size_total("test_volume") is None
        assert dsm.storage.volume_size_total("test_volume", True) is None
        assert dsm.storage.volume_size_used("test_volume") is None
        assert dsm.storage.volume_size_used("test_volume", True) is None
        assert dsm.storage.volume_percentage_used("test_volume") is None
        assert dsm.storage.volume_disk_temp_avg("test_volume") is None
        assert dsm.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr_volumes(self, dsm):
        """Test SHR storage volumes."""
        dsm.disks_redundancy = "SHR1"
        dsm.storage.update()

        # Basics
        assert dsm.storage.volumes_ids
        for volume_id in dsm.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert dsm.storage.volume_status(volume_id)
            assert dsm.storage.volume_device_type(volume_id)
            assert dsm.storage.volume_size_total(volume_id)
            assert dsm.storage.volume_size_total(volume_id, True)
            assert dsm.storage.volume_size_used(volume_id)
            assert dsm.storage.volume_size_used(volume_id, True)
            assert dsm.storage.volume_percentage_used(volume_id)
            assert dsm.storage.volume_disk_temp_avg(volume_id)
            assert dsm.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm.storage.volume_status("volume_1") == "normal"
        assert dsm.storage.volume_device_type("volume_1") == "shr_without_disk_protect"
        assert dsm.storage.volume_size_total("volume_1") == 2948623499264
        assert dsm.storage.volume_size_total("volume_1", True) == "2.7Tb"
        assert dsm.storage.volume_size_used("volume_1") == 2710796488704
        assert dsm.storage.volume_size_used("volume_1", True) == "2.5Tb"
        assert dsm.storage.volume_percentage_used("volume_1") == 91.9
        assert dsm.storage.volume_disk_temp_avg("volume_1") == 29.0
        assert dsm.storage.volume_disk_temp_max("volume_1") == 29

        assert dsm.storage.volume_status("volume_2") == "normal"
        assert dsm.storage.volume_device_type("volume_2") == "shr_without_disk_protect"
        assert dsm.storage.volume_size_total("volume_2") == 1964124495872
        assert dsm.storage.volume_size_total("volume_2", True) == "1.8Tb"
        assert dsm.storage.volume_size_used("volume_2") == 1684179374080
        assert dsm.storage.volume_size_used("volume_2", True) == "1.5Tb"
        assert dsm.storage.volume_percentage_used("volume_2") == 85.7
        assert dsm.storage.volume_disk_temp_avg("volume_2") == 30.0
        assert dsm.storage.volume_disk_temp_max("volume_2") == 30

        # Non existing volume
        assert not dsm.storage.volume_status("not_a_volume")
        assert not dsm.storage.volume_device_type("not_a_volume")
        assert not dsm.storage.volume_size_total("not_a_volume")
        assert not dsm.storage.volume_size_total("not_a_volume", True)
        assert not dsm.storage.volume_size_used("not_a_volume")
        assert not dsm.storage.volume_size_used("not_a_volume", True)
        assert not dsm.storage.volume_percentage_used("not_a_volume")
        assert not dsm.storage.volume_disk_temp_avg("not_a_volume")
        assert not dsm.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert dsm.storage.volume_status("test_volume") is None
        assert dsm.storage.volume_device_type("test_volume") is None
        assert dsm.storage.volume_size_total("test_volume") is None
        assert dsm.storage.volume_size_total("test_volume", True) is None
        assert dsm.storage.volume_size_used("test_volume") is None
        assert dsm.storage.volume_size_used("test_volume", True) is None
        assert dsm.storage.volume_percentage_used("test_volume") is None
        assert dsm.storage.volume_disk_temp_avg("test_volume") is None
        assert dsm.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr2_volumes(self, dsm):
        """Test SHR2 storage volumes."""
        dsm.disks_redundancy = "SHR2"
        dsm.storage.update()

        # Basics
        assert dsm.storage.volumes_ids
        for volume_id in dsm.storage.volumes_ids:
            assert dsm.storage.volume_status(volume_id)
            assert dsm.storage.volume_device_type(volume_id)
            assert dsm.storage.volume_size_total(volume_id)
            assert dsm.storage.volume_size_total(volume_id, True)
            assert dsm.storage.volume_size_used(volume_id)
            assert dsm.storage.volume_size_used(volume_id, True)
            assert dsm.storage.volume_percentage_used(volume_id)
            assert dsm.storage.volume_disk_temp_avg(volume_id)
            assert dsm.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm.storage.volume_status("volume_1") == "normal"
        assert dsm.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert dsm.storage.volume_size_total("volume_1") == 38378964738048
        assert dsm.storage.volume_size_total("volume_1", True) == "34.9Tb"
        assert dsm.storage.volume_size_used("volume_1") == 26724878606336
        assert dsm.storage.volume_size_used("volume_1", True) == "24.3Tb"
        assert dsm.storage.volume_percentage_used("volume_1") == 69.6
        assert dsm.storage.volume_disk_temp_avg("volume_1") == 37.0
        assert dsm.storage.volume_disk_temp_max("volume_1") == 41

    def test_storage_shr2_expansion_volumes(self, dsm):
        """Test SHR2 storage with expansion unit volumes."""
        dsm.disks_redundancy = "SHR2_EXPANSION"
        dsm.storage.update()

        # Basics
        assert dsm.storage.volumes_ids
        for volume_id in dsm.storage.volumes_ids:
            assert dsm.storage.volume_status(volume_id)
            assert dsm.storage.volume_device_type(volume_id)
            assert dsm.storage.volume_size_total(volume_id)
            assert dsm.storage.volume_size_total(volume_id, True)
            assert dsm.storage.volume_size_used(volume_id)
            assert dsm.storage.volume_size_used(volume_id, True)
            assert dsm.storage.volume_percentage_used(volume_id)
            assert dsm.storage.volume_disk_temp_avg(volume_id)
            assert dsm.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm.storage.volume_status("volume_1") == "normal"
        assert dsm.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert dsm.storage.volume_size_total("volume_1") == 31714659872768
        assert dsm.storage.volume_size_total("volume_1", True) == "28.8Tb"
        assert dsm.storage.volume_size_used("volume_1") == 25419707531264
        assert dsm.storage.volume_size_used("volume_1", True) == "23.1Tb"
        assert dsm.storage.volume_percentage_used("volume_1") == 80.2
        assert dsm.storage.volume_disk_temp_avg("volume_1") == 33.0
        assert dsm.storage.volume_disk_temp_max("volume_1") == 35

    def test_storage_disks(self, dsm):
        """Test storage disks."""
        dsm.storage.update()
        # Basics
        assert dsm.storage.disks_ids
        for disk_id in dsm.storage.disks_ids:
            if disk_id == "test_disk":
                continue
            assert "Drive" in dsm.storage.disk_name(disk_id)
            assert "/dev/" in dsm.storage.disk_device(disk_id)
            assert dsm.storage.disk_smart_status(disk_id) == "normal"
            assert dsm.storage.disk_status(disk_id) == "normal"
            assert not dsm.storage.disk_exceed_bad_sector_thr(disk_id)
            assert not dsm.storage.disk_below_remain_life_thr(disk_id)
            assert dsm.storage.disk_temp(disk_id)

        # Non existing disk
        assert not dsm.storage.disk_name("not_a_disk")
        assert not dsm.storage.disk_device("not_a_disk")
        assert not dsm.storage.disk_smart_status("not_a_disk")
        assert not dsm.storage.disk_status("not_a_disk")
        assert not dsm.storage.disk_exceed_bad_sector_thr("not_a_disk")
        assert not dsm.storage.disk_below_remain_life_thr("not_a_disk")
        assert not dsm.storage.disk_temp("not_a_disk")

        # Test disk
        assert dsm.storage.disk_name("test_disk") is None
        assert dsm.storage.disk_device("test_disk") is None
        assert dsm.storage.disk_smart_status("test_disk") is None
        assert dsm.storage.disk_status("test_disk") is None
        assert dsm.storage.disk_exceed_bad_sector_thr("test_disk") is None
        assert dsm.storage.disk_below_remain_life_thr("test_disk") is None
        assert dsm.storage.disk_temp("test_disk") is None

    def test_download_station(self, dsm):
        """Test DownloadStation."""
        assert dsm.download_station
        assert not dsm.download_station.get_all_tasks()

        assert dsm.download_station.get_info()["data"]["version"]
        assert dsm.download_station.get_config()["data"]["default_destination"]
        assert dsm.download_station.get_stat()["data"]["speed_download"]
        dsm.download_station.update()
        assert dsm.download_station.get_all_tasks()
        assert len(dsm.download_station.get_all_tasks()) == 8

        # BT DL
        assert dsm.download_station.get_task("dbid_86").status == "downloading"
        assert not dsm.download_station.get_task("dbid_86").status_extra
        assert dsm.download_station.get_task("dbid_86").type == "bt"
        assert dsm.download_station.get_task("dbid_86").additional.get("file")
        assert len(dsm.download_station.get_task("dbid_86").additional.get("file")) == 9

        # HTTPS error
        assert dsm.download_station.get_task("dbid_549").status == "error"
        assert (
            dsm.download_station.get_task("dbid_549").status_extra["error_detail"]
            == "broken_link"
        )
        assert dsm.download_station.get_task("dbid_549").type == "https"

    def test_surveillance_station(self, dsm):
        """Test SurveillanceStation."""
        dsm.with_surveillance = True
        assert dsm.surveillance_station
        assert not dsm.surveillance_station.get_all_cameras()

        dsm.surveillance_station.update()
        assert dsm.surveillance_station.get_all_cameras()
        assert dsm.surveillance_station.get_camera(1)
        assert dsm.surveillance_station.get_camera_live_view_path(1)
        assert dsm.surveillance_station.get_camera_live_view_path(1, "rtsp")

        # Motion detection
        assert dsm.surveillance_station.enable_motion_detection(1).get("success")
        assert dsm.surveillance_station.disable_motion_detection(1).get("success")

        # Home mode
        assert dsm.surveillance_station.get_home_mode_status()
        assert dsm.surveillance_station.set_home_mode(False)
        assert dsm.surveillance_station.set_home_mode(True)
