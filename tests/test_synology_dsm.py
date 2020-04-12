# -*- coding: utf-8 -*-
"""Synology DSM tests."""
from unittest import TestCase

from synology_dsm.exceptions import (
    SynologyDSMLogin2SARequiredException,
    SynologyDSMLogin2SAFailedException,
)

from . import (
    SynologyDSMMock,
    VALID_DSM_HOST,
    VALID_DSM_PORT,
    VALID_OTP,
    VALID_PASSWORD,
    VALID_USER,
    VALID_USER_2SA,
)
from .const import SESSION_ID, SERIAL, DEVICE_TOKEN, SYNO_TOKEN


class TestSynologyDSM(TestCase):
    """SynologyDSM test cases."""

    api = None

    def setUp(self):
        self.api = SynologyDSMMock(
            VALID_DSM_HOST, VALID_DSM_PORT, VALID_USER, VALID_PASSWORD
        )

    def test_init(self):
        """Test init."""
        assert self.api.username
        assert not self.api._session_id  # pylint: disable=protected-access
        assert self.api.base_url

    def test_login(self):
        """Test login."""
        assert self.api.login()
        assert self.api._session_id == SESSION_ID  # pylint: disable=protected-access
        assert self.api._syno_token == SYNO_TOKEN  # pylint: disable=protected-access

    def test_login_failed(self):  # pylint: disable=no-self-use
        """Test failed login."""
        api = SynologyDSMMock("host", VALID_DSM_PORT, VALID_USER, VALID_PASSWORD)
        assert not api.login()
        assert not api._session_id  # pylint: disable=protected-access

        api = SynologyDSMMock(VALID_DSM_HOST, 0, VALID_USER, VALID_PASSWORD)
        assert not api.login()
        assert not api._session_id  # pylint: disable=protected-access

        api = SynologyDSMMock(VALID_DSM_HOST, VALID_DSM_PORT, "user", VALID_PASSWORD)
        assert not api.login()
        assert not api._session_id  # pylint: disable=protected-access

        api = SynologyDSMMock(VALID_DSM_HOST, VALID_DSM_PORT, VALID_USER, "pass")
        assert not api.login()
        assert not api._session_id  # pylint: disable=protected-access

    def test_login_2sa(self):
        """Test login with 2SA."""
        api = SynologyDSMMock(
            VALID_DSM_HOST, VALID_DSM_PORT, VALID_USER_2SA, VALID_PASSWORD
        )
        with self.assertRaises(SynologyDSMLogin2SARequiredException):
            api.login()
        api.login(VALID_OTP)

        assert api._session_id == SESSION_ID  # pylint: disable=protected-access
        assert api._syno_token == SYNO_TOKEN  # pylint: disable=protected-access
        assert api._device_token == DEVICE_TOKEN  # pylint: disable=protected-access
        assert api.device_token == DEVICE_TOKEN

    def test_login_2sa_failed(self):
        """Test failed login with 2SA."""
        api = SynologyDSMMock(
            VALID_DSM_HOST, VALID_DSM_PORT, VALID_USER_2SA, VALID_PASSWORD
        )
        with self.assertRaises(SynologyDSMLogin2SARequiredException):
            api.login()
        with self.assertRaises(SynologyDSMLogin2SAFailedException):
            api.login(888888)

        assert api._session_id is None  # pylint: disable=protected-access
        assert api._syno_token is None  # pylint: disable=protected-access
        assert api._device_token is None  # pylint: disable=protected-access

    def test_information(self):
        """Test information."""
        assert self.api.information
        assert self.api.information.model == "DS918+"
        assert self.api.information.ram == 4096
        assert self.api.information.serial == SERIAL
        assert self.api.information.temperature == 40
        assert not self.api.information.temperature_warn
        assert self.api.information.uptime == 155084
        assert self.api.information.version_string == "DSM 6.2.2-24922 Update 4"

    def test_utilisation(self):
        """Test utilization."""
        assert self.api.utilisation

    def test_utilisation_cpu(self):
        """Test utilization CPU."""
        assert self.api.utilisation.cpu
        assert self.api.utilisation.cpu_other_load
        assert self.api.utilisation.cpu_user_load
        assert self.api.utilisation.cpu_system_load == 0
        assert self.api.utilisation.cpu_total_load
        assert self.api.utilisation.cpu_1min_load
        assert self.api.utilisation.cpu_5min_load
        assert self.api.utilisation.cpu_15min_load

    def test_utilisation_memory(self):
        """Test utilization memory."""
        assert self.api.utilisation.memory
        assert self.api.utilisation.memory_real_usage
        assert self.api.utilisation.memory_size
        assert self.api.utilisation.memory_available_swap
        assert self.api.utilisation.memory_cached
        assert self.api.utilisation.memory_available_real
        assert self.api.utilisation.memory_total_real
        assert self.api.utilisation.memory_total_swap

    def test_utilisation_network(self):
        """Test utilization network."""
        assert self.api.utilisation.network
        assert self.api.utilisation.network_up
        assert self.api.utilisation.network_down

    def test_storage(self):
        """Test storage roots."""
        assert self.api.storage
        assert self.api.storage.disks
        assert self.api.storage.env
        assert self.api.storage.storage_pools
        assert self.api.storage.volumes

    def test_storage_volumes(self):
        """Test storage volumes."""
        # Basics
        assert self.api.storage.volumes_ids
        for volume_id in self.api.storage.volumes_ids:
            if volume_id == "test_volume":
                continue
            assert self.api.storage.volume_status(volume_id)
            assert self.api.storage.volume_device_type(volume_id)
            assert self.api.storage.volume_size_total(volume_id)
            assert self.api.storage.volume_size_total(volume_id, False)
            assert self.api.storage.volume_size_used(volume_id)
            assert self.api.storage.volume_size_used(volume_id, False)
            assert self.api.storage.volume_percentage_used(volume_id)
            assert self.api.storage.volume_disk_temp_avg(volume_id)
            assert self.api.storage.volume_disk_temp_max(volume_id)

        # Existing volume
        assert self.api.storage.volume_status("volume_1") == "normal"
        assert self.api.storage.volume_device_type("volume_1") == "raid_5"
        assert self.api.storage.volume_size_total("volume_1") == "7.0Tb"
        assert self.api.storage.volume_size_total("volume_1", False) == 7672030584832
        assert self.api.storage.volume_size_used("volume_1") == "4.0Tb"
        assert self.api.storage.volume_size_used("volume_1", False) == 4377452806144
        assert self.api.storage.volume_percentage_used("volume_1") == 57.1
        assert self.api.storage.volume_disk_temp_avg("volume_1") == 24.0
        assert self.api.storage.volume_disk_temp_max("volume_1") == 24

        # Non existing volume
        assert not self.api.storage.volume_status("not_a_volume")
        assert not self.api.storage.volume_device_type("not_a_volume")
        assert not self.api.storage.volume_size_total("not_a_volume")
        assert not self.api.storage.volume_size_total("not_a_volume", False)
        assert not self.api.storage.volume_size_used("not_a_volume")
        assert not self.api.storage.volume_size_used("not_a_volume", False)
        assert not self.api.storage.volume_percentage_used("not_a_volume")
        assert not self.api.storage.volume_disk_temp_avg("not_a_volume")
        assert not self.api.storage.volume_disk_temp_max("not_a_volume")

        # Test volume
        assert self.api.storage.volume_status("test_volume") is None
        assert self.api.storage.volume_device_type("test_volume") is None
        assert self.api.storage.volume_size_total("test_volume") is None
        assert self.api.storage.volume_size_total("test_volume", False) is None
        assert self.api.storage.volume_size_used("test_volume") is None
        assert self.api.storage.volume_size_used("test_volume", False) is None
        assert self.api.storage.volume_percentage_used("test_volume") is None
        assert self.api.storage.volume_disk_temp_avg("test_volume") is None
        assert self.api.storage.volume_disk_temp_max("test_volume") is None

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
