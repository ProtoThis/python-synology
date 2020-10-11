"""DSM Storage data."""
from synology_dsm.helpers import SynoFormatHelper


class SynoStorage:
    """Class containing Storage data."""

    API_KEY = "SYNO.Storage.CGI.Storage"

    def __init__(self, dsm):
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates storage data."""
        raw_data = self._dsm.get(self.API_KEY, "load_info")
        if raw_data:
            self._data = raw_data
            if raw_data.get("data"):
                self._data = raw_data["data"]

    # Root
    @property
    def disks(self):
        """Gets all (internal) disks."""
        return self._data.get("disks", [])

    @property
    def env(self):
        """Gets storage env."""
        return self._data.get("env")

    @property
    def storage_pools(self):
        """Gets all storage pools."""
        return self._data.get("storagePools", [])

    @property
    def volumes(self):
        """Gets all volumes."""
        return self._data.get("volumes", [])

    # Volume
    @property
    def volumes_ids(self):
        """Returns volumes ids."""
        volumes = []
        for volume in self.volumes:
            volumes.append(volume["id"])
        return volumes

    def get_volume(self, volume_id):
        """Returns a specific volume."""
        for volume in self.volumes:
            if volume["id"] == volume_id:
                return volume
        return {}

    def volume_status(self, volume_id):
        """Status of the volume (normal, degraded, etc)."""
        return self.get_volume(volume_id).get("status")

    def volume_device_type(self, volume_id):
        """Returns the volume type (RAID1, RAID2, etc)."""
        return self.get_volume(volume_id).get("device_type")

    def volume_size_total(self, volume_id, human_readable=False):
        """Total size of volume."""
        volume = self.get_volume(volume_id)
        if volume.get("size"):
            return_data = int(volume["size"]["total"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def volume_size_used(self, volume_id, human_readable=False):
        """Total used size in volume."""
        volume = self.get_volume(volume_id)
        if volume.get("size"):
            return_data = int(volume["size"]["used"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def volume_percentage_used(self, volume_id):
        """Total used size in percentage for volume."""
        volume = self.get_volume(volume_id)
        if volume.get("size"):
            total = int(volume["size"]["total"])
            used = int(volume["size"]["used"])

            if used and used > 0 and total and total > 0:
                return round((float(used) / float(total)) * 100.0, 1)
        return None

    def volume_disk_temp_avg(self, volume_id):
        """Average temperature of all disks making up the volume."""
        vol_disks = self._get_disks_for_volume(volume_id)
        if vol_disks:
            total_temp = 0
            total_disks = 0

            for vol_disk in vol_disks:
                disk_temp = self.disk_temp(vol_disk["id"])
                if disk_temp:
                    total_disks += 1
                    total_temp += disk_temp

            if total_temp > 0 and total_disks > 0:
                return round(total_temp / total_disks, 0)
        return None

    def volume_disk_temp_max(self, volume_id):
        """Maximum temperature of all disks making up the volume."""
        vol_disks = self._get_disks_for_volume(volume_id)
        if vol_disks:
            max_temp = 0

            for vol_disk in vol_disks:
                disk_temp = self.disk_temp(vol_disk["id"])
                if disk_temp and disk_temp > max_temp:
                    max_temp = disk_temp
            return max_temp
        return None

    # Disk
    @property
    def disks_ids(self):
        """Returns (internal) disks ids."""
        disks = []
        for disk in self.disks:
            disks.append(disk["id"])
        return disks

    def get_disk(self, disk_id):
        """Returns a specific disk."""
        for disk in self.disks:
            if disk["id"] == disk_id:
                return disk
        return {}

    def _get_disks_for_volume(self, volume_id):
        """Returns a list of disk for a specific volume."""
        disks = []
        for pool in self.storage_pools:

            if pool.get("deploy_path") == volume_id:
                # RAID disk redundancy
                for disk_id in pool["disks"]:
                    disks.append(self.get_disk(disk_id))

            if pool.get("pool_child"):
                # SHR disk redundancy
                for pool_child in pool.get("pool_child"):
                    if pool_child["id"] == volume_id:
                        for disk_id in pool["disks"]:
                            disks.append(self.get_disk(disk_id))

        return disks

    def disk_name(self, disk_id):
        """The name of this disk."""
        return self.get_disk(disk_id).get("name")

    def disk_device(self, disk_id):
        """The mount point of this disk."""
        return self.get_disk(disk_id).get("device")

    def disk_smart_status(self, disk_id):
        """Status of disk according to S.M.A.R.T)."""
        return self.get_disk(disk_id).get("smart_status")

    def disk_status(self, disk_id):
        """Status of disk."""
        return self.get_disk(disk_id).get("status")

    def disk_exceed_bad_sector_thr(self, disk_id):
        """Checks if disk has exceeded maximum bad sector threshold."""
        return self.get_disk(disk_id).get("exceed_bad_sector_thr")

    def disk_below_remain_life_thr(self, disk_id):
        """Checks if disk has fallen below minimum life threshold."""
        return self.get_disk(disk_id).get("below_remain_life_thr")

    def disk_temp(self, disk_id):
        """Returns the temperature of the disk."""
        return self.get_disk(disk_id).get("temp")
