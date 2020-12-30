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


class TestSynologyDSM6:
    """SynologyDSM 6 test cases."""

    def test_login(self, dsm_6):
        """Test login."""
        assert dsm_6.login()
        assert dsm_6.apis.get(API_AUTH)
        assert dsm_6._session_id == SESSION_ID
        assert dsm_6._syno_token == SYNO_TOKEN

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

    def test_information(self, dsm_6):
        """Test information."""
        assert dsm_6.information
        dsm_6.information.update()
        assert dsm_6.information.model == "DS918+"
        assert dsm_6.information.ram == 4096
        assert dsm_6.information.serial == "1920PDN001501"
        assert dsm_6.information.temperature == 40
        assert not dsm_6.information.temperature_warn
        assert dsm_6.information.uptime == 155084
        assert dsm_6.information.version == "24922"
        assert dsm_6.information.version_string == "DSM 6.2.2-24922 Update 4"

    def test_network(self, dsm_6):
        """Test network."""
        assert dsm_6.network
        dsm_6.network.update()
        assert dsm_6.network.dns
        assert dsm_6.network.gateway
        assert dsm_6.network.hostname
        assert dsm_6.network.interfaces
        assert dsm_6.network.interface("eth0")
        assert dsm_6.network.interface("eth1")
        assert dsm_6.network.macs
        assert dsm_6.network.workgroup

    def test_security(self, dsm_6):
        """Test security, safe status."""
        assert dsm_6.security
        dsm_6.security.update()
        assert dsm_6.security.checks
        assert dsm_6.security.last_scan_time
        assert not dsm_6.security.start_time  # Finished scan
        assert dsm_6.security.success
        assert dsm_6.security.progress
        assert dsm_6.security.status == "safe"
        assert dsm_6.security.status_by_check
        assert dsm_6.security.status_by_check["malware"] == "safe"
        assert dsm_6.security.status_by_check["network"] == "safe"
        assert dsm_6.security.status_by_check["securitySetting"] == "safe"
        assert dsm_6.security.status_by_check["systemCheck"] == "safe"
        assert dsm_6.security.status_by_check["update"] == "safe"
        assert dsm_6.security.status_by_check["userInfo"] == "safe"

    def test_security_error(self, dsm_6):
        """Test security, outOfDate status."""
        dsm_6.error = True
        assert dsm_6.security
        dsm_6.security.update()
        assert dsm_6.security.checks
        assert dsm_6.security.last_scan_time
        assert not dsm_6.security.start_time  # Finished scan
        assert dsm_6.security.success
        assert dsm_6.security.progress
        assert dsm_6.security.status == "outOfDate"
        assert dsm_6.security.status_by_check
        assert dsm_6.security.status_by_check["malware"] == "safe"
        assert dsm_6.security.status_by_check["network"] == "safe"
        assert dsm_6.security.status_by_check["securitySetting"] == "safe"
        assert dsm_6.security.status_by_check["systemCheck"] == "safe"
        assert dsm_6.security.status_by_check["update"] == "outOfDate"
        assert dsm_6.security.status_by_check["userInfo"] == "safe"

    def test_shares(self, dsm_6):
        """Test shares."""
        assert dsm_6.share
        dsm_6.share.update()
        assert dsm_6.share.shares
        for share_uuid in dsm_6.share.shares_uuids:
            assert dsm_6.share.share_name(share_uuid)
            assert dsm_6.share.share_path(share_uuid)
            assert dsm_6.share.share_recycle_bin(share_uuid) is not None
            assert dsm_6.share.share_size(share_uuid) is not None
            assert dsm_6.share.share_size(share_uuid, human_readable=True)

        assert (
            dsm_6.share.share_name("2ee6c06a-8766-48b5-013d-63b18652a393")
            == "test_share"
        )
        assert (
            dsm_6.share.share_path("2ee6c06a-8766-48b5-013d-63b18652a393") == "/volume1"
        )
        assert (
            dsm_6.share.share_recycle_bin("2ee6c06a-8766-48b5-013d-63b18652a393")
            is True
        )
        assert (
            dsm_6.share.share_size("2ee6c06a-8766-48b5-013d-63b18652a393")
            == 3.790251876432216e19
        )
        assert (
            dsm_6.share.share_size("2ee6c06a-8766-48b5-013d-63b18652a393", True)
            == "32.9Eb"
        )

    def test_system(self, dsm_6):
        """Test system."""
        assert dsm_6.system
        dsm_6.system.update()
        assert dsm_6.system.cpu_clock_speed
        assert dsm_6.system.cpu_cores
        assert dsm_6.system.cpu_family
        assert dsm_6.system.cpu_series
        assert dsm_6.system.firmware_ver
        assert dsm_6.system.model
        assert dsm_6.system.ram_size
        assert dsm_6.system.serial
        assert dsm_6.system.sys_temp
        assert dsm_6.system.time
        assert dsm_6.system.time_zone
        assert dsm_6.system.time_zone_desc
        assert dsm_6.system.up_time
        for usb_dev in dsm_6.system.usb_dev:
            assert usb_dev.get("cls")
            assert usb_dev.get("pid")
            assert usb_dev.get("producer")
            assert usb_dev.get("product")
            assert usb_dev.get("rev")
            assert usb_dev.get("vid")

    def test_upgrade(self, dsm_6):
        """Test upgrade."""
        assert dsm_6.upgrade
        dsm_6.upgrade.update()
        assert dsm_6.upgrade.update_available
        assert dsm_6.upgrade.available_version == "DSM 6.2.3-25426 Update 2"
        assert dsm_6.upgrade.reboot_needed == "now"
        assert dsm_6.upgrade.service_restarts == "some"

    def test_storage(self, dsm_6):
        """Test storage roots."""
        assert dsm_6.storage
        dsm_6.storage.update()
        assert dsm_6.storage.disks
        assert dsm_6.storage.env
        assert dsm_6.storage.storage_pools
        assert dsm_6.storage.volumes

    def test_storage_raid_volumes(self, dsm_6):
        """Test RAID storage volumes."""
        dsm_6.storage.update()
        # Basics
        assert dsm_6.storage.volumes_ids
        for volume_id in dsm_6.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert dsm_6.storage.volume_status(volume_id)
            assert dsm_6.storage.volume_device_type(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id, True)
            assert dsm_6.storage.volume_size_used(volume_id)
            assert dsm_6.storage.volume_size_used(volume_id, True)
            assert dsm_6.storage.volume_percentage_used(volume_id)
            assert dsm_6.storage.volume_disk_temp_avg(volume_id)
            assert dsm_6.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm_6.storage.volume_status("volume_1") == "normal"
        assert dsm_6.storage.volume_device_type("volume_1") == "raid_5"
        assert dsm_6.storage.volume_size_total("volume_1") == 7672030584832
        assert dsm_6.storage.volume_size_total("volume_1", True) == "7.0Tb"
        assert dsm_6.storage.volume_size_used("volume_1") == 4377452806144
        assert dsm_6.storage.volume_size_used("volume_1", True) == "4.0Tb"
        assert dsm_6.storage.volume_percentage_used("volume_1") == 57.1
        assert dsm_6.storage.volume_disk_temp_avg("volume_1") == 24.0
        assert dsm_6.storage.volume_disk_temp_max("volume_1") == 24

        # Non existing volume
        assert not dsm_6.storage.volume_status("not_a_volume")
        assert not dsm_6.storage.volume_device_type("not_a_volume")
        assert not dsm_6.storage.volume_size_total("not_a_volume")
        assert not dsm_6.storage.volume_size_total("not_a_volume", True)
        assert not dsm_6.storage.volume_size_used("not_a_volume")
        assert not dsm_6.storage.volume_size_used("not_a_volume", True)
        assert not dsm_6.storage.volume_percentage_used("not_a_volume")
        assert not dsm_6.storage.volume_disk_temp_avg("not_a_volume")
        assert not dsm_6.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert dsm_6.storage.volume_status("test_volume") is None
        assert dsm_6.storage.volume_device_type("test_volume") is None
        assert dsm_6.storage.volume_size_total("test_volume") is None
        assert dsm_6.storage.volume_size_total("test_volume", True) is None
        assert dsm_6.storage.volume_size_used("test_volume") is None
        assert dsm_6.storage.volume_size_used("test_volume", True) is None
        assert dsm_6.storage.volume_percentage_used("test_volume") is None
        assert dsm_6.storage.volume_disk_temp_avg("test_volume") is None
        assert dsm_6.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr_volumes(self, dsm_6):
        """Test SHR storage volumes."""
        dsm_6.disks_redundancy = "SHR1"
        dsm_6.storage.update()

        # Basics
        assert dsm_6.storage.volumes_ids
        for volume_id in dsm_6.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert dsm_6.storage.volume_status(volume_id)
            assert dsm_6.storage.volume_device_type(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id, True)
            assert dsm_6.storage.volume_size_used(volume_id)
            assert dsm_6.storage.volume_size_used(volume_id, True)
            assert dsm_6.storage.volume_percentage_used(volume_id)
            assert dsm_6.storage.volume_disk_temp_avg(volume_id)
            assert dsm_6.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm_6.storage.volume_status("volume_1") == "normal"
        assert (
            dsm_6.storage.volume_device_type("volume_1") == "shr_without_disk_protect"
        )
        assert dsm_6.storage.volume_size_total("volume_1") == 2948623499264
        assert dsm_6.storage.volume_size_total("volume_1", True) == "2.7Tb"
        assert dsm_6.storage.volume_size_used("volume_1") == 2710796488704
        assert dsm_6.storage.volume_size_used("volume_1", True) == "2.5Tb"
        assert dsm_6.storage.volume_percentage_used("volume_1") == 91.9
        assert dsm_6.storage.volume_disk_temp_avg("volume_1") == 29.0
        assert dsm_6.storage.volume_disk_temp_max("volume_1") == 29

        assert dsm_6.storage.volume_status("volume_2") == "normal"
        assert (
            dsm_6.storage.volume_device_type("volume_2") == "shr_without_disk_protect"
        )
        assert dsm_6.storage.volume_size_total("volume_2") == 1964124495872
        assert dsm_6.storage.volume_size_total("volume_2", True) == "1.8Tb"
        assert dsm_6.storage.volume_size_used("volume_2") == 1684179374080
        assert dsm_6.storage.volume_size_used("volume_2", True) == "1.5Tb"
        assert dsm_6.storage.volume_percentage_used("volume_2") == 85.7
        assert dsm_6.storage.volume_disk_temp_avg("volume_2") == 30.0
        assert dsm_6.storage.volume_disk_temp_max("volume_2") == 30

        # Non existing volume
        assert not dsm_6.storage.volume_status("not_a_volume")
        assert not dsm_6.storage.volume_device_type("not_a_volume")
        assert not dsm_6.storage.volume_size_total("not_a_volume")
        assert not dsm_6.storage.volume_size_total("not_a_volume", True)
        assert not dsm_6.storage.volume_size_used("not_a_volume")
        assert not dsm_6.storage.volume_size_used("not_a_volume", True)
        assert not dsm_6.storage.volume_percentage_used("not_a_volume")
        assert not dsm_6.storage.volume_disk_temp_avg("not_a_volume")
        assert not dsm_6.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert dsm_6.storage.volume_status("test_volume") is None
        assert dsm_6.storage.volume_device_type("test_volume") is None
        assert dsm_6.storage.volume_size_total("test_volume") is None
        assert dsm_6.storage.volume_size_total("test_volume", True) is None
        assert dsm_6.storage.volume_size_used("test_volume") is None
        assert dsm_6.storage.volume_size_used("test_volume", True) is None
        assert dsm_6.storage.volume_percentage_used("test_volume") is None
        assert dsm_6.storage.volume_disk_temp_avg("test_volume") is None
        assert dsm_6.storage.volume_disk_temp_max("test_volume") is None

    def test_storage_shr2_volumes(self, dsm_6):
        """Test SHR2 storage volumes."""
        dsm_6.disks_redundancy = "SHR2"
        dsm_6.storage.update()

        # Basics
        assert dsm_6.storage.volumes_ids
        for volume_id in dsm_6.storage.volumes_ids:
            assert dsm_6.storage.volume_status(volume_id)
            assert dsm_6.storage.volume_device_type(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id, True)
            assert dsm_6.storage.volume_size_used(volume_id)
            assert dsm_6.storage.volume_size_used(volume_id, True)
            assert dsm_6.storage.volume_percentage_used(volume_id)
            assert dsm_6.storage.volume_disk_temp_avg(volume_id)
            assert dsm_6.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm_6.storage.volume_status("volume_1") == "normal"
        assert dsm_6.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert dsm_6.storage.volume_size_total("volume_1") == 38378964738048
        assert dsm_6.storage.volume_size_total("volume_1", True) == "34.9Tb"
        assert dsm_6.storage.volume_size_used("volume_1") == 26724878606336
        assert dsm_6.storage.volume_size_used("volume_1", True) == "24.3Tb"
        assert dsm_6.storage.volume_percentage_used("volume_1") == 69.6
        assert dsm_6.storage.volume_disk_temp_avg("volume_1") == 37.0
        assert dsm_6.storage.volume_disk_temp_max("volume_1") == 41

    def test_storage_shr2_expansion_volumes(self, dsm_6):
        """Test SHR2 storage with expansion unit volumes."""
        dsm_6.disks_redundancy = "SHR2_EXPANSION"
        dsm_6.storage.update()

        # Basics
        assert dsm_6.storage.volumes_ids
        for volume_id in dsm_6.storage.volumes_ids:
            assert dsm_6.storage.volume_status(volume_id)
            assert dsm_6.storage.volume_device_type(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id)
            assert dsm_6.storage.volume_size_total(volume_id, True)
            assert dsm_6.storage.volume_size_used(volume_id)
            assert dsm_6.storage.volume_size_used(volume_id, True)
            assert dsm_6.storage.volume_percentage_used(volume_id)
            assert dsm_6.storage.volume_disk_temp_avg(volume_id)
            assert dsm_6.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert dsm_6.storage.volume_status("volume_1") == "normal"
        assert dsm_6.storage.volume_device_type("volume_1") == "shr_with_2_disk_protect"
        assert dsm_6.storage.volume_size_total("volume_1") == 31714659872768
        assert dsm_6.storage.volume_size_total("volume_1", True) == "28.8Tb"
        assert dsm_6.storage.volume_size_used("volume_1") == 25419707531264
        assert dsm_6.storage.volume_size_used("volume_1", True) == "23.1Tb"
        assert dsm_6.storage.volume_percentage_used("volume_1") == 80.2
        assert dsm_6.storage.volume_disk_temp_avg("volume_1") == 33.0
        assert dsm_6.storage.volume_disk_temp_max("volume_1") == 35

    def test_storage_disks(self, dsm_6):
        """Test storage disks."""
        dsm_6.storage.update()
        # Basics
        assert dsm_6.storage.disks_ids
        for disk_id in dsm_6.storage.disks_ids:
            if disk_id == "test_disk":
                continue
            assert "Drive" in dsm_6.storage.disk_name(disk_id)
            assert "/dev/" in dsm_6.storage.disk_device(disk_id)
            assert dsm_6.storage.disk_smart_status(disk_id) == "normal"
            assert dsm_6.storage.disk_status(disk_id) == "normal"
            assert not dsm_6.storage.disk_exceed_bad_sector_thr(disk_id)
            assert not dsm_6.storage.disk_below_remain_life_thr(disk_id)
            assert dsm_6.storage.disk_temp(disk_id)

        # Non existing disk
        assert not dsm_6.storage.disk_name("not_a_disk")
        assert not dsm_6.storage.disk_device("not_a_disk")
        assert not dsm_6.storage.disk_smart_status("not_a_disk")
        assert not dsm_6.storage.disk_status("not_a_disk")
        assert not dsm_6.storage.disk_exceed_bad_sector_thr("not_a_disk")
        assert not dsm_6.storage.disk_below_remain_life_thr("not_a_disk")
        assert not dsm_6.storage.disk_temp("not_a_disk")

        # Test disk
        assert dsm_6.storage.disk_name("test_disk") is None
        assert dsm_6.storage.disk_device("test_disk") is None
        assert dsm_6.storage.disk_smart_status("test_disk") is None
        assert dsm_6.storage.disk_status("test_disk") is None
        assert dsm_6.storage.disk_exceed_bad_sector_thr("test_disk") is None
        assert dsm_6.storage.disk_below_remain_life_thr("test_disk") is None
        assert dsm_6.storage.disk_temp("test_disk") is None

    def test_download_station(self, dsm_6):
        """Test DownloadStation."""
        assert dsm_6.download_station
        assert not dsm_6.download_station.get_all_tasks()

        assert dsm_6.download_station.get_info()["data"]["version"]
        assert dsm_6.download_station.get_config()["data"]["default_destination"]
        assert dsm_6.download_station.get_stat()["data"]["speed_download"]
        dsm_6.download_station.update()
        assert dsm_6.download_station.get_all_tasks()
        assert len(dsm_6.download_station.get_all_tasks()) == 8

        # BT DL
        assert dsm_6.download_station.get_task("dbid_86").status == "downloading"
        assert not dsm_6.download_station.get_task("dbid_86").status_extra
        assert dsm_6.download_station.get_task("dbid_86").type == "bt"
        assert dsm_6.download_station.get_task("dbid_86").additional.get("file")
        assert (
            len(dsm_6.download_station.get_task("dbid_86").additional.get("file")) == 9
        )

        # HTTPS error
        assert dsm_6.download_station.get_task("dbid_549").status == "error"
        assert (
            dsm_6.download_station.get_task("dbid_549").status_extra["error_detail"]
            == "broken_link"
        )
        assert dsm_6.download_station.get_task("dbid_549").type == "https"

    def test_surveillance_station(self, dsm_6):
        """Test SurveillanceStation."""
        dsm_6.with_surveillance = True
        assert dsm_6.surveillance_station
        assert not dsm_6.surveillance_station.get_all_cameras()

        dsm_6.surveillance_station.update()
        assert dsm_6.surveillance_station.get_all_cameras()
        assert dsm_6.surveillance_station.get_camera(1)
        assert dsm_6.surveillance_station.get_camera_live_view_path(1)
        assert dsm_6.surveillance_station.get_camera_live_view_path(1, "rtsp")

        # Motion detection
        assert dsm_6.surveillance_station.enable_motion_detection(1).get("success")
        assert dsm_6.surveillance_station.disable_motion_detection(1).get("success")

        # Home mode
        assert dsm_6.surveillance_station.get_home_mode_status()
        assert dsm_6.surveillance_station.set_home_mode(False)
        assert dsm_6.surveillance_station.set_home_mode(True)
