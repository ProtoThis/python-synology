"""Synology DSM tests."""
import pytest

from . import SynologyDSMMock
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
from synology_dsm.const import API_AUTH
from synology_dsm.const import API_INFO
from synology_dsm.exceptions import SynologyDSMAPIErrorException
from synology_dsm.exceptions import SynologyDSMAPINotExistsException
from synology_dsm.exceptions import SynologyDSMLogin2SAFailedException
from synology_dsm.exceptions import SynologyDSMLogin2SARequiredException
from synology_dsm.exceptions import SynologyDSMLoginInvalidException
from synology_dsm.exceptions import SynologyDSMRequestException


class TestSynologyDSM:
    """SynologyDSM test cases."""

    def test_init(self, dsm_5):
        """Test init."""
        assert dsm_5.username
        assert dsm_5._base_url
        assert not dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

    def test_connection_failed(self):
        """Test failed connection."""
        dsm_5 = SynologyDSMMock(
            "no_internet",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMRequestException):
            assert not dsm_5.login()
        assert not dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

        dsm_5 = SynologyDSMMock(
            "host",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMRequestException):
            assert not dsm_5.login()
        assert not dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

        dsm_5 = SynologyDSMMock(
            VALID_HOST, 0, VALID_USER, VALID_PASSWORD, VALID_HTTPS, VALID_VERIFY_SSL
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMRequestException):
            assert not dsm_5.login()
        assert not dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            False,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMRequestException):
            assert not dsm_5.login()
        assert not dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

    def test_login(self, dsm_5):
        """Test login."""
        assert dsm_5.login()
        assert dsm_5.apis.get(API_AUTH)
        assert dsm_5._session_id == SESSION_ID
        assert dsm_5._syno_token is None

    def test_login_failed(self):
        """Test failed login."""
        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            "user",
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMLoginInvalidException):
            assert not dsm_5.login()
        assert dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            "pass",
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMLoginInvalidException):
            assert not dsm_5.login()
        assert dsm_5.apis.get(API_AUTH)
        assert not dsm_5._session_id

    def test_login_2sa(self):
        """Test login with 2SA."""
        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMLogin2SARequiredException):
            dsm_5.login()
        dsm_5.login(VALID_OTP)

        assert dsm_5._session_id == SESSION_ID
        assert dsm_5._syno_token is None
        assert dsm_5._device_token == DEVICE_TOKEN
        assert dsm_5.device_token == DEVICE_TOKEN

    def test_login_2sa_new_session(self):
        """Test login with 2SA and a new session with granted device."""
        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
            device_token=DEVICE_TOKEN,
        )
        dsm_5.dsm_version = 5
        assert dsm_5.login()

        assert dsm_5._session_id == SESSION_ID
        assert dsm_5._syno_token is None
        assert dsm_5._device_token == DEVICE_TOKEN
        assert dsm_5.device_token == DEVICE_TOKEN

    def test_login_2sa_failed(self):
        """Test failed login with 2SA."""
        dsm_5 = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        dsm_5.dsm_version = 5
        with pytest.raises(SynologyDSMLogin2SARequiredException):
            dsm_5.login()
        with pytest.raises(SynologyDSMLogin2SAFailedException):
            dsm_5.login(888888)

        assert dsm_5._session_id is None
        assert dsm_5._syno_token is None
        assert dsm_5._device_token is None

    def test_request_get(self, dsm_5):
        """Test get request."""
        assert dsm_5.get(API_INFO, "query")
        assert dsm_5.get(API_AUTH, "login")
        assert dsm_5.get("SYNO.DownloadStation2.Task", "list")
        assert dsm_5.get(API_AUTH, "logout")

    def test_request_get_failed(self, dsm_5):
        """Test failed get request."""
        with pytest.raises(SynologyDSMAPINotExistsException):
            assert dsm_5.get("SYNO.Virtualization.dsm_5.Task.Info", "list")

    def test_request_post(self, dsm_5):
        """Test post request."""
        assert dsm_5.post(
            "SYNO.FileStation.Upload",
            "upload",
            params={"dest_folder_path": "/upload/test", "create_parents": True},
            files={"file": "open('file.txt','rb')"},
        )

        assert dsm_5.post(
            "SYNO.DownloadStation2.Task",
            "create",
            params={
                "uri": "ftps://192.0.0.1:21/test/test.zip",
                "username": "admin",
                "password": "1234",
            },
        )

    def test_request_post_failed(self, dsm_5):
        """Test failed post request."""
        with pytest.raises(SynologyDSMAPIErrorException):
            assert dsm_5.post(
                "SYNO.FileStation.Upload",
                "upload",
                params={"dest_folder_path": "/upload/test", "create_parents": True},
                files={"file": "open('file_already_exists.txt','rb')"},
            )

        with pytest.raises(SynologyDSMAPIErrorException):
            assert dsm_5.post(
                "SYNO.DownloadStation2.Task",
                "create",
                params={
                    "uri": "ftps://192.0.0.1:21/test/test_not_exists.zip",
                    "username": "admin",
                    "password": "1234",
                },
            )

    def test_information(self, dsm_5):
        """Test information."""
        assert dsm_5.information
        dsm_5.information.update()
        assert dsm_5.information.model == "DS3615xs"
        assert dsm_5.information.ram == 6144
        assert dsm_5.information.serial == "B3J4N01003"
        assert dsm_5.information.temperature == 40
        assert not dsm_5.information.temperature_warn
        assert dsm_5.information.uptime == 3897
        assert dsm_5.information.version == "5967"
        assert dsm_5.information.version_string == "DSM 5.2-5967 Update 9"

    def test_network(self, dsm_5):
        """Test network."""
        assert dsm_5.network
        dsm_5.network.update()
        assert dsm_5.network.dns
        assert dsm_5.network.gateway
        assert dsm_5.network.hostname
        assert dsm_5.network.interfaces
        assert dsm_5.network.interface("eth0")
        assert dsm_5.network.interface("eth1") is None
        assert dsm_5.network.macs
        assert dsm_5.network.workgroup

    def test_utilisation(self, dsm_5):
        """Test utilization."""
        assert dsm_5.utilisation
        dsm_5.utilisation.update()

    def test_utilisation_cpu(self, dsm_5):
        """Test utilization CPU."""
        dsm_5.utilisation.update()
        assert dsm_5.utilisation.cpu
        assert dsm_5.utilisation.cpu_other_load
        assert dsm_5.utilisation.cpu_user_load
        assert dsm_5.utilisation.cpu_system_load
        assert dsm_5.utilisation.cpu_total_load
        assert dsm_5.utilisation.cpu_1min_load
        assert dsm_5.utilisation.cpu_5min_load
        assert dsm_5.utilisation.cpu_15min_load

    def test_utilisation_memory(self, dsm_5):
        """Test utilization memory."""
        dsm_5.utilisation.update()
        assert dsm_5.utilisation.memory
        assert dsm_5.utilisation.memory_real_usage
        assert dsm_5.utilisation.memory_size()
        assert dsm_5.utilisation.memory_size(True)
        assert dsm_5.utilisation.memory_available_swap()
        assert dsm_5.utilisation.memory_available_swap(True)
        assert dsm_5.utilisation.memory_cached()
        assert dsm_5.utilisation.memory_cached(True)
        assert dsm_5.utilisation.memory_available_real()
        assert dsm_5.utilisation.memory_available_real(True)
        assert dsm_5.utilisation.memory_total_real()
        assert dsm_5.utilisation.memory_total_real(True)
        assert dsm_5.utilisation.memory_total_swap()
        assert dsm_5.utilisation.memory_total_swap(True)

    def test_utilisation_network(self, dsm_5):
        """Test utilization network."""
        dsm_5.utilisation.update()
        assert dsm_5.utilisation.network
        assert dsm_5.utilisation.network_up()
        assert dsm_5.utilisation.network_up(True)
        assert dsm_5.utilisation.network_down()
        assert dsm_5.utilisation.network_down(True)

    def test_storage(self, dsm_5):
        """Test storage roots."""
        assert dsm_5.storage
        dsm_5.storage.update()
        assert dsm_5.storage.disks
        assert dsm_5.storage.env
        assert dsm_5.storage.storage_pools == []
        assert dsm_5.storage.volumes

    def test_storage_volumes(self, dsm_5):
        """Test storage volumes."""
        dsm_5.storage.update()
        # Basics
        assert dsm_5.storage.volumes_ids
        for volume_id in dsm_5.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert dsm_5.storage.volume_status(volume_id)
            assert dsm_5.storage.volume_device_type(volume_id)
            assert dsm_5.storage.volume_size_total(volume_id)
            assert dsm_5.storage.volume_size_total(volume_id, True)
            assert dsm_5.storage.volume_size_used(volume_id)
            assert dsm_5.storage.volume_size_used(volume_id, True)
            assert dsm_5.storage.volume_percentage_used(volume_id)
            assert (
                dsm_5.storage.volume_disk_temp_avg(volume_id) is None
            )  # because of empty storagePools
            assert (
                dsm_5.storage.volume_disk_temp_max(volume_id) is None
            )  # because of empty storagePools

        # Existing volume
        assert dsm_5.storage.volume_status("volume_1") == "normal"
        assert dsm_5.storage.volume_device_type("volume_1") == "raid_5"
        assert dsm_5.storage.volume_size_total("volume_1") == 8846249701376
        assert dsm_5.storage.volume_size_total("volume_1", True) == "8.0Tb"
        assert dsm_5.storage.volume_size_used("volume_1") == 5719795761152
        assert dsm_5.storage.volume_size_used("volume_1", True) == "5.2Tb"
        assert dsm_5.storage.volume_percentage_used("volume_1") == 64.7
        assert (
            dsm_5.storage.volume_disk_temp_avg("volume_1") is None
        )  # because of empty storagePools
        assert (
            dsm_5.storage.volume_disk_temp_max("volume_1") is None
        )  # because of empty storagePools

        # Non existing volume
        assert not dsm_5.storage.volume_status("not_a_volume")
        assert not dsm_5.storage.volume_device_type("not_a_volume")
        assert not dsm_5.storage.volume_size_total("not_a_volume")
        assert not dsm_5.storage.volume_size_total("not_a_volume", True)
        assert not dsm_5.storage.volume_size_used("not_a_volume")
        assert not dsm_5.storage.volume_size_used("not_a_volume", True)
        assert not dsm_5.storage.volume_percentage_used("not_a_volume")
        assert not dsm_5.storage.volume_disk_temp_avg("not_a_volume")
        assert not dsm_5.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert dsm_5.storage.volume_status("test_volume") is None
        assert dsm_5.storage.volume_device_type("test_volume") is None
        assert dsm_5.storage.volume_size_total("test_volume") is None
        assert dsm_5.storage.volume_size_total("test_volume", True) is None
        assert dsm_5.storage.volume_size_used("test_volume") is None
        assert dsm_5.storage.volume_size_used("test_volume", True) is None
        assert dsm_5.storage.volume_percentage_used("test_volume") is None
        assert dsm_5.storage.volume_disk_temp_avg("test_volume") is None
        assert dsm_5.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_disks(self, dsm_5):
        """Test storage disks."""
        dsm_5.storage.update()
        # Basics
        assert dsm_5.storage.disks_ids
        for disk_id in dsm_5.storage.disks_ids:
            if disk_id == "test_disk":
                continue
            assert "Disk" in dsm_5.storage.disk_name(disk_id)
            assert "/dev/" in dsm_5.storage.disk_device(disk_id)
            if disk_id == "sda":
                assert dsm_5.storage.disk_smart_status(disk_id) == "90%"
            else:
                assert dsm_5.storage.disk_smart_status(disk_id) == "safe"
            assert dsm_5.storage.disk_status(disk_id) == "normal"
            assert not dsm_5.storage.disk_exceed_bad_sector_thr(disk_id)
            assert not dsm_5.storage.disk_below_remain_life_thr(disk_id)
            assert dsm_5.storage.disk_temp(disk_id)

        # Non existing disk
        assert not dsm_5.storage.disk_name("not_a_disk")
        assert not dsm_5.storage.disk_device("not_a_disk")
        assert not dsm_5.storage.disk_smart_status("not_a_disk")
        assert not dsm_5.storage.disk_status("not_a_disk")
        assert not dsm_5.storage.disk_exceed_bad_sector_thr("not_a_disk")
        assert not dsm_5.storage.disk_below_remain_life_thr("not_a_disk")
        assert not dsm_5.storage.disk_temp("not_a_disk")

        # Test disk
        assert dsm_5.storage.disk_name("test_disk") is None
        assert dsm_5.storage.disk_device("test_disk") is None
        assert dsm_5.storage.disk_smart_status("test_disk") is None
        assert dsm_5.storage.disk_status("test_disk") is None
        assert dsm_5.storage.disk_exceed_bad_sector_thr("test_disk") is None
        assert dsm_5.storage.disk_below_remain_life_thr("test_disk") is None
        assert dsm_5.storage.disk_temp("test_disk") is None
