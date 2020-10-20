"""Synology DSM tests."""
from unittest import TestCase

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

# pylint: disable=no-self-use,protected-access,anomalous-backslash-in-string
class TestSynologyDSM(TestCase):
    """SynologyDSM test cases."""

    api = None

    def setUp(self):
        self.api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        self.api.dsm_version = 5

    def test_init(self):
        """Test init."""
        assert self.api.username
        assert self.api._base_url
        assert not self.api.apis.get(API_AUTH)
        assert not self.api._session_id

    def test_connection_failed(self):
        """Test failed connection."""
        api = SynologyDSMMock(
            "no_internet",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMRequestException):
            assert not api.login()
        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        api = SynologyDSMMock(
            "host",
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMRequestException):
            assert not api.login()
        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        api = SynologyDSMMock(
            VALID_HOST, 0, VALID_USER, VALID_PASSWORD, VALID_HTTPS, VALID_VERIFY_SSL
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMRequestException):
            assert not api.login()
        assert not api.apis.get(API_AUTH)
        assert not api._session_id

        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            VALID_PASSWORD,
            False,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMRequestException):
            assert not api.login()
        assert not api.apis.get(API_AUTH)
        assert not api._session_id

    def test_login(self):
        """Test login."""
        assert self.api.login()
        assert self.api.apis.get(API_AUTH)
        assert self.api._session_id == SESSION_ID
        assert self.api._syno_token is None

    def test_login_failed(self):
        """Test failed login."""
        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            "user",
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMLoginInvalidException):
            assert not api.login()
        assert api.apis.get(API_AUTH)
        assert not api._session_id

        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER,
            "pass",
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMLoginInvalidException):
            assert not api.login()
        assert api.apis.get(API_AUTH)
        assert not api._session_id

    def test_login_2sa(self):
        """Test login with 2SA."""
        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMLogin2SARequiredException):
            api.login()
        api.login(VALID_OTP)

        assert api._session_id == SESSION_ID
        assert api._syno_token is None
        assert api._device_token == DEVICE_TOKEN
        assert api.device_token == DEVICE_TOKEN

    def test_login_2sa_new_session(self):
        """Test login with 2SA and a new session with granted device."""
        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
            device_token=DEVICE_TOKEN,
        )
        api.dsm_version = 5
        assert api.login()

        assert api._session_id == SESSION_ID
        assert api._syno_token is None
        assert api._device_token == DEVICE_TOKEN
        assert api.device_token == DEVICE_TOKEN

    def test_login_2sa_failed(self):
        """Test failed login with 2SA."""
        api = SynologyDSMMock(
            VALID_HOST,
            VALID_PORT,
            VALID_USER_2SA,
            VALID_PASSWORD,
            VALID_HTTPS,
            VALID_VERIFY_SSL,
        )
        api.dsm_version = 5
        with self.assertRaises(SynologyDSMLogin2SARequiredException):
            api.login()
        with self.assertRaises(SynologyDSMLogin2SAFailedException):
            api.login(888888)

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
        with self.assertRaises(SynologyDSMAPINotExistsException):
            assert self.api.get("SYNO.Virtualization.API.Task.Info", "list")

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
        with self.assertRaises(SynologyDSMAPIErrorException):
            assert self.api.post(
                "SYNO.FileStation.Upload",
                "upload",
                params={"dest_folder_path": "/upload/test", "create_parents": True},
                files={"file": "open('file_already_exists.txt','rb')"},
            )

        with self.assertRaises(SynologyDSMAPIErrorException):
            assert self.api.post(
                "SYNO.DownloadStation2.Task",
                "create",
                params={
                    "uri": "ftps://192.0.0.1:21/test/test_not_exists.zip",
                    "username": "admin",
                    "password": "1234",
                },
            )

    def test_information(self):
        """Test information."""
        assert self.api.information
        self.api.information.update()
        assert self.api.information.model == "DS3615xs"
        assert self.api.information.ram == 6144
        assert self.api.information.serial == "B3J4N01003"
        assert self.api.information.temperature == 40
        assert not self.api.information.temperature_warn
        assert self.api.information.uptime == 3897
        assert self.api.information.version == "5967"
        assert self.api.information.version_string == "DSM 5.2-5967 Update 9"

    def test_network(self):
        """Test network."""
        assert self.api.network
        self.api.network.update()
        assert self.api.network.dns
        assert self.api.network.gateway
        assert self.api.network.hostname
        assert self.api.network.interfaces
        assert self.api.network.interface("eth0")
        assert self.api.network.interface("eth1") is None
        assert self.api.network.macs
        assert self.api.network.workgroup

    def test_utilisation(self):
        """Test utilization."""
        assert self.api.utilisation
        self.api.utilisation.update()

    def test_utilisation_cpu(self):
        """Test utilization CPU."""
        self.api.utilisation.update()
        assert self.api.utilisation.cpu
        assert self.api.utilisation.cpu_other_load
        assert self.api.utilisation.cpu_user_load
        assert self.api.utilisation.cpu_system_load
        assert self.api.utilisation.cpu_total_load
        assert self.api.utilisation.cpu_1min_load
        assert self.api.utilisation.cpu_5min_load
        assert self.api.utilisation.cpu_15min_load

    def test_utilisation_memory(self):
        """Test utilization memory."""
        self.api.utilisation.update()
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
        """Test utilization network."""
        self.api.utilisation.update()
        assert self.api.utilisation.network
        assert self.api.utilisation.network_up()
        assert self.api.utilisation.network_up(True)
        assert self.api.utilisation.network_down()
        assert self.api.utilisation.network_down(True)

    def test_storage(self):
        """Test storage roots."""
        assert self.api.storage
        self.api.storage.update()
        assert self.api.storage.disks
        assert self.api.storage.env
        assert self.api.storage.storage_pools == []
        assert self.api.storage.volumes

    def test_storage_volumes(self):
        """Test storage volumes."""
        self.api.storage.update()
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
            assert (
                self.api.storage.volume_disk_temp_avg(volume_id) is None
            )  # because of empty storagePools
            assert (
                self.api.storage.volume_disk_temp_max(volume_id) is None
            )  # because of empty storagePools

        # Existing volume
        assert self.api.storage.volume_status("volume_1") == "normal"
        assert self.api.storage.volume_device_type("volume_1") == "raid_5"
        assert self.api.storage.volume_size_total("volume_1") == 8846249701376
        assert self.api.storage.volume_size_total("volume_1", True) == "8.0Tb"
        assert self.api.storage.volume_size_used("volume_1") == 5719795761152
        assert self.api.storage.volume_size_used("volume_1", True) == "5.2Tb"
        assert self.api.storage.volume_percentage_used("volume_1") == 64.7
        assert (
            self.api.storage.volume_disk_temp_avg("volume_1") is None
        )  # because of empty storagePools
        assert (
            self.api.storage.volume_disk_temp_max("volume_1") is None
        )  # because of empty storagePools

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

    def test_storage_disks(self):
        """Test storage disks."""
        self.api.storage.update()
        # Basics
        assert self.api.storage.disks_ids
        for disk_id in self.api.storage.disks_ids:
            if disk_id == "test_disk":
                continue
            assert "Disk" in self.api.storage.disk_name(disk_id)
            assert "/dev/" in self.api.storage.disk_device(disk_id)
            if disk_id == "sda":
                assert self.api.storage.disk_smart_status(disk_id) == "90%"
            else:
                assert self.api.storage.disk_smart_status(disk_id) == "safe"
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
