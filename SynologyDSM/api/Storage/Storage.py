"""DSM Storage data."""
# -*- coding:utf-8 -*-
from SynologyDSM.helpers import SynoFormatHelper


class SynoStorage(object):
    """Class containing Storage data."""

    def __init__(self, raw_data):
        self._data = {}
        self.update(raw_data)

    def update(self, raw_data):
        """Updates storage data."""
        if raw_data:
            self._data = raw_data["data"]

    @property
    def volumes(self):
        """Returns all available volumes."""
        volumes = []
        for volume in self._data.get("volumes"):
            volumes.append(volume["id"])
        return volumes

    def _get_volume(self, volume_id):
        """Returns a specific volume."""
        for volume in self._data.get("volumes"):
            if volume["id"] == volume_id:
                return volume
        return {}

    def volume_status(self, volume_id):
        """Status of the volume (normal, degraded, etc)."""
        volume = self._get_volume(volume_id)
        return volume.get("status")

    def volume_device_type(self, volume_id):
        """Returns the volume type (RAID1, RAID2, etc)."""
        volume = self._get_volume(volume_id)
        return volume.get("device_type")

    def volume_size_total(self, volume_id, human_readable=True):
        """Total size of volume."""
        volume = self._get_volume(volume_id)
        if volume.get("size"):
            return_data = int(volume["size"]["total"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def volume_size_used(self, volume_id, human_readable=True):
        """Total used size in volume."""
        volume = self._get_volume(volume_id)
        if volume.get("size"):
            return_data = int(volume["size"]["used"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def volume_percentage_used(self, volume_id):
        """Total used size in percentage for volume."""
        volume = self._get_volume(volume_id)
        if volume.get("size"):
            total = int(volume["size"]["total"])
            used = int(volume["size"]["used"])

            if used and used > 0 and total and total > 0:
                return round((float(used) / float(total)) * 100.0, 1)
        return None

    def volume_disk_temp_avg(self, volume_id):
        """Average temperature of all disks making up the volume."""
        volume = self._get_volume(volume_id)
        if volume:
            vol_disks = self.disks
            if vol_disks:
                total_temp = 0
                total_disks = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp:
                        total_disks += 1
                        total_temp += disk_temp

                if total_temp > 0 and total_disks > 0:
                    return round(total_temp / total_disks, 0)
        return None

    def volume_disk_temp_max(self, volume_id):
        """Maximum temperature of all disks making up the volume."""
        volume = self._get_volume(volume_id)
        if volume:
            vol_disks = self.disks
            if vol_disks:
                max_temp = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp and disk_temp > max_temp:
                        max_temp = disk_temp
                return max_temp
        return None

    @property
    def disks(self):
        """Returns all available (internal) disks."""
        disks = []
        for disk in self._data.get("disks"):
            disks.append(disk["id"])
        return disks

    def _get_disk(self, disk_id):
        """Returns a specific disk."""
        for disk in self._data.get("disks"):
            if disk["id"] == disk_id:
                return disk
        return {}

    def disk_name(self, disk_id):
        """The name of this disk."""
        disk = self._get_disk(disk_id)
        return disk.get("name")

    def disk_device(self, disk_id):
        """The mount point of this disk."""
        disk = self._get_disk(disk_id)
        return disk.get("device")

    def disk_smart_status(self, disk_id):
        """Status of disk according to S.M.A.R.T)."""
        disk = self._get_disk(disk_id)
        return disk.get("smart_status")

    def disk_status(self, disk_id):
        """Status of disk."""
        disk = self._get_disk(disk_id)
        return disk.get("status")

    def disk_exceed_bad_sector_thr(self, disk_id):
        """Checks if disk has exceeded maximum bad sector threshold."""
        disk = self._get_disk(disk_id)
        return disk.get("exceed_bad_sector_thr")

    def disk_below_remain_life_thr(self, disk_id):
        """Checks if disk has fallen below minimum life threshold."""
        disk = self._get_disk(disk_id)
        return disk.get("below_remain_life_thr")

    def disk_temp(self, disk_id):
        """Returns the temperature of the disk."""
        disk = self._get_disk(disk_id)
        return disk.get("temp")
