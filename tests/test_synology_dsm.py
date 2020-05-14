# -*- coding: utf-8 -*-
"""Synology DSM tests."""
from unittest import TestCase
import pytest

from synology_dsm.api.core.security import SynoCoreSecurity
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.exceptions import (
    SynologyDSMRequestException,
    SynologyDSMAPINotExistsException,
    SynologyDSMAPIErrorException,
    SynologyDSMLoginInvalidException,
    SynologyDSMLogin2SARequiredException,
    SynologyDSMLogin2SAFailedException,
)
from synology_dsm.const import API_AUTH, API_INFO

from . import (
    SynologyDSMMock,
    VALID_HOST,
    VALID_PORT,
    VALID_SSL,
    VALID_OTP,
    VALID_PASSWORD,
    VALID_USER,
    VALID_USER_2SA,
)
from .const import SESSION_ID, DEVICE_TOKEN, SYNO_TOKEN

# pylint: disable=no-self-use,protected-access,anomalous-backslash-in-string
class TestSynologyDSM(TestCase):
    """SynologyDSM test cases."""

    api = None

    def setUp(self):
        self.api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )

    def test_init(self):
        """Test init."""
        assert self.api.username
        assert self.api._base_url
        assert not self.api.apis.get(API_AUTH)
        assert not self.api._session_id

    def test_connection_failed(self):
        """Test failed connection."""
        # No internet
        api = SynologyDSMMock(
            "no_internet", VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )
        with pytest.raises(SynologyDSMRequestException) as error:
            api.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            "ConnectionError = <urllib3.connection.VerifiedHTTPSConnection "
            in error_value["details"]
        )

        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        # Wrong host
        api = SynologyDSMMock("host", VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL)
        with pytest.raises(SynologyDSMRequestException) as error:
            api.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            "ConnectionError = <urllib3.connection.HTTPConnection "
            in error_value["details"]
        )

        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        # Wrong port
        api = SynologyDSMMock(VALID_HOST, 0, VALID_USER, VALID_PASSWORD, VALID_SSL)
        with pytest.raises(SynologyDSMRequestException) as error:
            api.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert (
            error_value["details"]
            == "SSLError = [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1076)"
        )

        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        # Wrong SSL
        api = SynologyDSMMock(VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, False)
        with pytest.raises(SynologyDSMRequestException) as error:
            api.login()
        error_value = error.value.args[0]
        assert not error_value["api"]
        assert error_value["code"] == -1
        assert error_value["reason"] == "Unknown"
        assert error_value["details"] == "RequestException = Bad request"

        assert not api.apis.get(API_AUTH)
        assert not api._session_id

    def test_login(self):
        """Test login."""
        assert self.api.login()
        assert self.api.apis.get(API_AUTH)
        assert self.api._session_id == SESSION_ID
        assert self.api._syno_token == SYNO_TOKEN

    def test_login_failed(self):
        """Test failed login."""
        api = SynologyDSMMock(VALID_HOST, VALID_PORT, "user", VALID_PASSWORD, VALID_SSL)
        with pytest.raises(SynologyDSMLoginInvalidException) as error:
            api.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 400
        assert error_value["reason"] == "Invalid credentials"
        assert error_value["details"] == "Invalid password or not admin account: user"

        assert api.apis.get(API_AUTH)
        assert not api._session_id

        api = SynologyDSMMock(VALID_HOST, VALID_PORT, VALID_USER, "pass", VALID_SSL)
        with pytest.raises(SynologyDSMLoginInvalidException) as error:
            api.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 400
        assert error_value["reason"] == "Invalid credentials"
        assert (
            error_value["details"]
            == "Invalid password or not admin account: valid_user"
        )

        assert api.apis.get(API_AUTH)
        assert not api._session_id

    def test_login_2sa(self):
        """Test login with 2SA."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER_2SA, VALID_PASSWORD, VALID_SSL
        )

        with pytest.raises(SynologyDSMLogin2SARequiredException) as error:
            api.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 403
        assert error_value["reason"] == "One time password not specified"
        assert (
            error_value["details"]
            == "Two-step authentication required for account: valid_user_2sa"
        )

        assert api.login(VALID_OTP)

        assert api._session_id == SESSION_ID
        assert api._syno_token == SYNO_TOKEN
        assert api._device_token == DEVICE_TOKEN
        assert api.device_token == DEVICE_TOKEN

    def test_login_2sa_new_session(self):  # pylint: disable=no-self-use
        """Test login with 2SA and a new session with granted device."""
        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_SSL,
            device_token=DEVICE_TOKEN,
        )
        assert api.login()

        assert api._session_id == SESSION_ID
        assert api._syno_token == SYNO_TOKEN
        assert api._device_token == DEVICE_TOKEN
        assert api.device_token == DEVICE_TOKEN

    def test_login_2sa_failed(self):
        """Test failed login with 2SA."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER_2SA, VALID_PASSWORD, VALID_SSL
        )

        with pytest.raises(SynologyDSMLogin2SARequiredException) as error:
            api.login()
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 403
        assert error_value["reason"] == "One time password not specified"
        assert (
            error_value["details"]
            == "Two-step authentication required for account: valid_user_2sa"
        )

        with pytest.raises(SynologyDSMLogin2SAFailedException) as error:
            api.login(888888)
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.API.Auth"
        assert error_value["code"] == 404
        assert error_value["reason"] == "One time password authenticate failed"
        assert (
            error_value["details"]
            == "Two-step authentication failed, retry with a new pass code"
        )

        assert api._session_id is None
        assert api._syno_token is None
        assert api._device_token is None

    def test_request_get(self):
        """Test get request."""
        assert self.api.get(API_INFO, "query")
        assert self.api.get(API_AUTH, "login")
        assert self.api.get("SYNO.DownloadStation2.Task", "list")
        assert self.api.get(API_AUTH, "logout")

    def test_request_get_failed(self):
        """Test failed get request."""
        with pytest.raises(SynologyDSMAPINotExistsException) as error:
            self.api.get("SYNO.Virtualization.API.Task.Info", "list")
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.Virtualization.API.Task.Info"
        assert error_value["code"] == -2
        assert error_value["reason"] == "Unknown"
        assert (
            error_value["details"]
            == "API SYNO.Virtualization.API.Task.Info does not exists"
        )

    def test_request_post(self):
        """Test post request."""
        assert self.api.post(
            "SYNO.FileStation.Upload",
            "upload",
            params={"dest_folder_path": "/upload/test", "create_parents": True},
            files={"file": "open('file.txt','rb')"},
        )

        assert self.api.post(
            "SYNO.DownloadStation2.Task",
            "create",
            params={
                "uri": "ftps://192.0.0.1:21/test/test.zip",
                "username": "admin",
                "password": "1234",
            },
        )

    def test_request_post_failed(self):
        """Test failed post request."""
        with pytest.raises(SynologyDSMAPIErrorException) as error:
            self.api.post(
                "SYNO.FileStation.Upload",
                "upload",
                params={"dest_folder_path": "/upload/test", "create_parents": True},
                files={"file": "open('file_already_exists.txt','rb')"},
            )
        error_value = error.value.args[0]
        assert error_value["api"] == "SYNO.FileStation.Upload"
        assert error_value["code"] == 1805
        assert (
            error_value["reason"]
            == "Can’t overwrite or skip the existed file, if no overwrite parameter is given"
        )
        assert not error_value["details"]

        with pytest.raises(SynologyDSMAPIErrorException) as error:
            self.api.post(
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

    def test_reset_str_attr(self):
        """Test reset with string attr."""
        assert not self.api._security
        assert self.api.security
        assert self.api._security
        assert self.api.reset("security")
        assert not self.api._security

    def test_reset_str_key(self):
        """Test reset with string API key."""
        assert not self.api._security
        assert self.api.security
        assert self.api._security
        assert self.api.reset(SynoCoreSecurity.API_KEY)
        assert not self.api._security

    def test_reset_object(self):
        """Test reset with object."""
        assert not self.api._security
        assert self.api.security
        assert self.api._security
        assert self.api.reset(self.api.security)
        assert not self.api._security

    def test_reset_str_attr_information(self):
        """Test reset with string information attr (should not be reset)."""
        assert not self.api._information
        assert self.api.information
        assert self.api._information
        assert not self.api.reset("information")
        assert self.api._information

    def test_reset_str_key_information(self):
        """Test reset with string information API key (should not be reset)."""
        assert not self.api._information
        assert self.api.information
        assert self.api._information
        assert not self.api.reset(SynoDSMInformation.API_KEY)
        assert self.api._information

    def test_reset_object_information(self):
        """Test reset with information object (should not be reset)."""
        assert not self.api._information
        assert self.api.information
        assert self.api._information
        assert not self.api.reset(self.api.information)
        assert self.api._information

    def test_information(self):
        """Test information."""
        assert self.api.information
        assert self.api.information.model == "DS918+"
        assert self.api.information.ram == 4096
        assert self.api.information.serial == "1920PDN001501"
        assert self.api.information.temperature == 40
        assert not self.api.information.temperature_warn
        assert self.api.information.uptime == 155084
        assert self.api.information.version == "24922"
        assert self.api.information.version_string == "DSM 6.2.2-24922 Update 4"

    def test_network(self):
        """Test network."""
        assert self.api.network
        assert self.api.network.dns
        assert self.api.network.gateway
        assert self.api.network.hostname
        assert self.api.network.interfaces
        assert self.api.network.interface("eth0")
        assert self.api.network.interface("eth1")
        assert self.api.network.macs
        assert self.api.network.workgroup

    def test_security(self):
        """Test security."""
        assert self.api.security
        assert self.api.security.checks
        assert self.api.security.last_scan_time
        assert not self.api.security.start_time  # Finished scan
        assert self.api.security.success
        assert self.api.security.progress
        assert self.api.security.status

    def test_utilisation(self):
        """Test utilisation."""
        assert self.api.utilisation

    def test_utilisation_error(self):
        """Test utilisation error."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )
        api.error = True
        with pytest.raises(SynologyDSMAPIErrorException) as error:
            assert api.utilisation
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

    def test_utilisation_cpu(self):
        """Test utilisation CPU."""
        assert self.api.utilisation.cpu
        assert self.api.utilisation.cpu_other_load
        assert self.api.utilisation.cpu_user_load
        assert self.api.utilisation.cpu_system_load
        assert self.api.utilisation.cpu_total_load
        assert self.api.utilisation.cpu_1min_load
        assert self.api.utilisation.cpu_5min_load
        assert self.api.utilisation.cpu_15min_load

    def test_utilisation_memory(self):
        """Test utilisation memory."""
        assert self.api.utilisation.memory
        assert self.api.utilisation.memory_real_usage
        assert self.api.utilisation.memory_size()
        assert self.api.utilisation.memory_size(True)
        assert self.api.utilisation.memory_available_swap()
        assert self.api.utilisation.memory_available_swap(True)
        assert self.api.utilisation.memory_cached()
        assert self.api.utilisation.memory_cached(True)
        assert self.api.utilisation.memory_available_real()
        assert self.api.utilisation.memory_available_real(True)
        assert self.api.utilisation.memory_total_real()
        assert self.api.utilisation.memory_total_real(True)
        assert self.api.utilisation.memory_total_swap()
        assert self.api.utilisation.memory_total_swap(True)

    def test_utilisation_network(self):
        """Test utilisation network."""
        assert self.api.utilisation.network
        assert self.api.utilisation.network_up()
        assert self.api.utilisation.network_up(True)
        assert self.api.utilisation.network_down()
        assert self.api.utilisation.network_down(True)

    def test_storage(self):
        """Test storage roots."""
        assert self.api.storage
        assert self.api.storage.disks
        assert self.api.storage.env
        assert self.api.storage.storage_pools
        assert self.api.storage.volumes

    def test_storage_raid_volumes(self):
        """Test RAID storage volumes."""
        # Basics
        assert self.api.storage.volumes_ids
        for volume_id in self.api.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert self.api.storage.volume_status(volume_id)
            assert self.api.storage.volume_device_type(volume_id)
            assert self.api.storage.volume_size_total(volume_id)
            assert self.api.storage.volume_size_total(volume_id, True)
            assert self.api.storage.volume_size_used(volume_id)
            assert self.api.storage.volume_size_used(volume_id, True)
            assert self.api.storage.volume_percentage_used(volume_id)
            assert self.api.storage.volume_disk_temp_avg(volume_id)
            assert self.api.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert self.api.storage.volume_status("volume_1") == "normal"
        assert self.api.storage.volume_device_type("volume_1") == "raid_5"
        assert self.api.storage.volume_size_total("volume_1") == 7672030584832
        assert self.api.storage.volume_size_total("volume_1", True) == "7.0Tb"
        assert self.api.storage.volume_size_used("volume_1") == 4377452806144
        assert self.api.storage.volume_size_used("volume_1", True) == "4.0Tb"
        assert self.api.storage.volume_percentage_used("volume_1") == 57.1
        assert self.api.storage.volume_disk_temp_avg("volume_1") == 24.0
        assert self.api.storage.volume_disk_temp_max("volume_1") == 24

        # Non existing volume
        assert not self.api.storage.volume_status("not_a_volume")
        assert not self.api.storage.volume_device_type("not_a_volume")
        assert not self.api.storage.volume_size_total("not_a_volume")
        assert not self.api.storage.volume_size_total("not_a_volume", True)
        assert not self.api.storage.volume_size_used("not_a_volume")
        assert not self.api.storage.volume_size_used("not_a_volume", True)
        assert not self.api.storage.volume_percentage_used("not_a_volume")
        assert not self.api.storage.volume_disk_temp_avg("not_a_volume")
        assert not self.api.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert self.api.storage.volume_status("test_volume") is None
        assert self.api.storage.volume_device_type("test_volume") is None
        assert self.api.storage.volume_size_total("test_volume") is None
        assert self.api.storage.volume_size_total("test_volume", True) is None
        assert self.api.storage.volume_size_used("test_volume") is None
        assert self.api.storage.volume_size_used("test_volume", True) is None
        assert self.api.storage.volume_percentage_used("test_volume") is None
        assert self.api.storage.volume_disk_temp_avg("test_volume") is None
        assert self.api.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr_volumes(self):
        """Test SHR storage volumes."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )
        api.disks_redundancy = "SHR1"

        # Basics
        assert api.storage.volumes_ids
        for volume_id in api.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert api.storage.volume_status(volume_id)
            assert api.storage.volume_device_type(volume_id)
            assert api.storage.volume_size_total(volume_id)
            assert api.storage.volume_size_total(volume_id, True)
            assert api.storage.volume_size_used(volume_id)
            assert api.storage.volume_size_used(volume_id, True)
            assert api.storage.volume_percentage_used(volume_id)
            assert api.storage.volume_disk_temp_avg(volume_id)
            assert api.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert api.storage.volume_status("volume_1") == "normal"
        assert api.storage.volume_device_type("volume_1") == "shr_without_disk_protect"
        assert api.storage.volume_size_total("volume_1") == 2948623499264
        assert api.storage.volume_size_total("volume_1", True) == "2.7Tb"
        assert api.storage.volume_size_used("volume_1") == 2710796488704
        assert api.storage.volume_size_used("volume_1", True) == "2.5Tb"
        assert api.storage.volume_percentage_used("volume_1") == 91.9
        assert api.storage.volume_disk_temp_avg("volume_1") == 29.0
        assert api.storage.volume_disk_temp_max("volume_1") == 29

        assert api.storage.volume_status("volume_2") == "normal"
        assert api.storage.volume_device_type("volume_2") == "shr_without_disk_protect"
        assert api.storage.volume_size_total("volume_2") == 1964124495872
        assert api.storage.volume_size_total("volume_2", True) == "1.8Tb"
        assert api.storage.volume_size_used("volume_2") == 1684179374080
        assert api.storage.volume_size_used("volume_2", True) == "1.5Tb"
        assert api.storage.volume_percentage_used("volume_2") == 85.7
        assert api.storage.volume_disk_temp_avg("volume_2") == 30.0
        assert api.storage.volume_disk_temp_max("volume_2") == 30

        # Non existing volume
        assert not api.storage.volume_status("not_a_volume")
        assert not api.storage.volume_device_type("not_a_volume")
        assert not api.storage.volume_size_total("not_a_volume")
        assert not api.storage.volume_size_total("not_a_volume", True)
        assert not api.storage.volume_size_used("not_a_volume")
        assert not api.storage.volume_size_used("not_a_volume", True)
        assert not api.storage.volume_percentage_used("not_a_volume")
        assert not api.storage.volume_disk_temp_avg("not_a_volume")
        assert not api.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert api.storage.volume_status("test_volume") is None
        assert api.storage.volume_device_type("test_volume") is None
        assert api.storage.volume_size_total("test_volume") is None
        assert api.storage.volume_size_total("test_volume", True) is None
        assert api.storage.volume_size_used("test_volume") is None
        assert api.storage.volume_size_used("test_volume", True) is None
        assert api.storage.volume_percentage_used("test_volume") is None
        assert api.storage.volume_disk_temp_avg("test_volume") is None
        assert api.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr2_volumes(self):
        """Test SHR2 storage volumes."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )
        api.disks_redundancy = "SHR2"

        # Basics
        assert api.storage.volumes_ids
        for volume_id in api.storage.volumes_ids:
            assert api.storage.volume_status(volume_id)
            assert api.storage.volume_device_type(volume_id)
            assert api.storage.volume_size_total(volume_id)
            assert api.storage.volume_size_total(volume_id, True)
            assert api.storage.volume_size_used(volume_id)
            assert api.storage.volume_size_used(volume_id, True)
            assert api.storage.volume_percentage_used(volume_id)
            assert api.storage.volume_disk_temp_avg(volume_id)
            assert api.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert api.storage.volume_status("volume_1") == "normal"
        assert api.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert api.storage.volume_size_total("volume_1") == 38378964738048
        assert api.storage.volume_size_total("volume_1", True) == "34.9Tb"
        assert api.storage.volume_size_used("volume_1") == 26724878606336
        assert api.storage.volume_size_used("volume_1", True) == "24.3Tb"
        assert api.storage.volume_percentage_used("volume_1") == 69.6
        assert api.storage.volume_disk_temp_avg("volume_1") == 37.0
        assert api.storage.volume_disk_temp_max("volume_1") == 41

    def test_storage_shr2_expansion_volumes(self):
        """Test SHR2 storage with expansion unit volumes."""
        api = SynologyDSMMock(
            VALID_HOST, VALID_PORT, VALID_USER, VALID_PASSWORD, VALID_SSL
        )
        api.disks_redundancy = "SHR2_EXPANSION"

        # Basics
        assert api.storage.volumes_ids
        for volume_id in api.storage.volumes_ids:
            assert api.storage.volume_status(volume_id)
            assert api.storage.volume_device_type(volume_id)
            assert api.storage.volume_size_total(volume_id)
            assert api.storage.volume_size_total(volume_id, True)
            assert api.storage.volume_size_used(volume_id)
            assert api.storage.volume_size_used(volume_id, True)
            assert api.storage.volume_percentage_used(volume_id)
            assert api.storage.volume_disk_temp_avg(volume_id)
            assert api.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert api.storage.volume_status("volume_1") == "normal"
        assert api.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert api.storage.volume_size_total("volume_1") == 31714659872768
        assert api.storage.volume_size_total("volume_1", True) == "28.8Tb"
        assert api.storage.volume_size_used("volume_1") == 25419707531264
        assert api.storage.volume_size_used("volume_1", True) == "23.1Tb"
        assert api.storage.volume_percentage_used("volume_1") == 80.2
        assert api.storage.volume_disk_temp_avg("volume_1") == 33.0
        assert api.storage.volume_disk_temp_max("volume_1") == 35

    def test_storage_disks(self):
        """Test storage disks."""
        # Basics
        assert self.api.storage.disks_ids
        for disk_id in self.api.storage.disks_ids:
            if disk_id == "test_disk":
                continue
            assert "Drive" in self.api.storage.disk_name(disk_id)
            assert "/dev/" in self.api.storage.disk_device(disk_id)
            assert self.api.storage.disk_smart_status(disk_id) == "normal"
            assert self.api.storage.disk_status(disk_id) == "normal"
            assert not self.api.storage.disk_exceed_bad_sector_thr(disk_id)
            assert not self.api.storage.disk_below_remain_life_thr(disk_id)
            assert self.api.storage.disk_temp(disk_id)

        # Non existing disk
        assert not self.api.storage.disk_name("not_a_disk")
        assert not self.api.storage.disk_device("not_a_disk")
        assert not self.api.storage.disk_smart_status("not_a_disk")
        assert not self.api.storage.disk_status("not_a_disk")
        assert not self.api.storage.disk_exceed_bad_sector_thr("not_a_disk")
        assert not self.api.storage.disk_below_remain_life_thr("not_a_disk")
        assert not self.api.storage.disk_temp("not_a_disk")

        # Test disk
        assert self.api.storage.disk_name("test_disk") is None
        assert self.api.storage.disk_device("test_disk") is None
        assert self.api.storage.disk_smart_status("test_disk") is None
        assert self.api.storage.disk_status("test_disk") is None
        assert self.api.storage.disk_exceed_bad_sector_thr("test_disk") is None
        assert self.api.storage.disk_below_remain_life_thr("test_disk") is None
        assert self.api.storage.disk_temp("test_disk") is None
