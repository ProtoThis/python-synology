"""DSM Storage data."""
# -*- coding:utf-8 -*-
from SynologyDSM.helpers import SynoFormatHelper


class SynoStorage(object):
    """Class containing Storage data"""
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)

    def update(self, raw_input):
        """Allows updating Utilisation data with raw_input data"""
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def volumes(self):
        """Returns all available volumes"""
        if self._data is not None:
            volumes = []
            for volume in self._data["volumes"]:
                volumes.append(volume["id"])
            return volumes

    def _get_volume(self, volume_id):
        """Returns a specific volume"""
        if self._data is not None:
            for volume in self._data["volumes"]:
                if volume["id"] == volume_id:
                    return volume

    def volume_status(self, volume):
        """Status of the volume (normal, degraded, etc)"""
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["status"]

    def volume_device_type(self, volume):
        """Returns the volume type (RAID1, RAID2, etc)"""
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["device_type"]

    def volume_size_total(self, volume, human_readable=True):
        """Total size of volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            return_data = int(volume["size"]["total"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(
                    return_data)
            else:
                return return_data

    def volume_size_used(self, volume, human_readable=True):
        """Total used size in volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            return_data = int(volume["size"]["used"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(
                    return_data)
            else:
                return return_data

    def volume_percentage_used(self, volume):
        """Total used size in percentage for volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            total = int(volume["size"]["total"])
            used = int(volume["size"]["used"])

            if used is not None and used > 0 and \
               total is not None and total > 0:
                return round((float(used) / float(total)) * 100.0, 1)

    def volume_disk_temp_avg(self, volume):
        """Average temperature of all disks making up the volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            vol_disks = self.disks
            if vol_disks is not None:
                total_temp = 0
                total_disks = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp is not None:
                        total_disks += 1
                        total_temp += disk_temp

                if total_temp > 0 and total_disks > 0:
                    return round(total_temp / total_disks, 0)

    def volume_disk_temp_max(self, volume):
        """Maximum temperature of all disks making up the volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            vol_disks = self.disks
            if vol_disks is not None:
                max_temp = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp is not None and disk_temp > max_temp:
                        max_temp = disk_temp

                return max_temp

    @property
    def disks(self):
        """Returns all available (internal) disks"""
        if self._data is not None:
            disks = []
            for disk in self._data["disks"]:
                disks.append(disk["id"])
            return disks

    def _get_disk(self, disk_id):
        """Returns a specific disk"""
        if self._data is not None:
            for disk in self._data["disks"]:
                if disk["id"] == disk_id:
                    return disk

    def disk_name(self, disk):
        """The name of this disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["name"]

    def disk_device(self, disk):
        """The mount point of this disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["device"]

    def disk_smart_status(self, disk):
        """Status of disk according to S.M.A.R.T)"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["smart_status"]

    def disk_status(self, disk):
        """Status of disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["status"]

    def disk_exceed_bad_sector_thr(self, disk):
        """Checks if disk has exceeded maximum bad sector threshold"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["exceed_bad_sector_thr"]

    def disk_below_remain_life_thr(self, disk):
        """Checks if disk has fallen below minimum life threshold"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["below_remain_life_thr"]

    def disk_temp(self, disk):
        """Returns the temperature of the disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["temp"]
