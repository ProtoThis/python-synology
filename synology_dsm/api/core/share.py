# -*- coding: utf-8 -*-
"""Shared Folders data."""
from synology_dsm.helpers import SynoFormatHelper


class SynoShare(object):
    """Class containing Share data."""

    API_KEY = "SYNO.Core.Share"
    # Syno supports two methods to retrieve resource details, GET and POST.
    # GET returns a limited set of keys. With POST the same keys as GET
    # are returned plus any keys listed in the "additional" parameter.
    # NOTE: The value of the additional key must be a string.
    REQUEST_DATA = {
        "additional": '["hidden","encryption","is_aclmode","unite_permission","is_support_acl",'
        '"is_sync_share","is_force_readonly","force_readonly_reason","recyclebin",'
        '"is_share_moving","is_cluster_share","is_exfat_share","is_cold_storage_share",'
        '"support_snapshot","share_quota","enable_share_compress","enable_share_cow",'
        '"include_cold_storage_share","is_cold_storage_share"]',
        "shareType": "all",
    }

    def __init__(self, dsm):
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates share data."""
        raw_data = self._dsm.post(self.API_KEY, "list", data=self.REQUEST_DATA)
        if raw_data:
            self._data = raw_data["data"]

    @property
    def shares(self):
        """Gets all shares."""
        return self._data.get("shares", [])

    def share(self, share_name):
        """Returns a specific share."""
        for share in self.shares:
            if share["name"] == share_name:
                return share
        return {}

    @property
    def shares_names(self):
        """Returns (internal) share names."""
        shares = []
        for share in self.shares:
            shares.append(share["name"])
        return shares

    def share_path(self, name):
        """The volume path of this share."""
        return self.share(name).get("vol_path")

    def share_recycle_bin(self, name):
        """Is the recycle bin enabled for this share?"""
        return self.share(name).get("enable_recycle_bin")

    def share_size(self, name, human_readable=False):
        """Total size of share."""
        share_size_mb = self.share(name).get("share_quota_used")
        # Share size is returned in MB so we convert it.
        share_size_bytes = SynoFormatHelper.megabytes_to_bytes(share_size_mb)
        if human_readable:
            return SynoFormatHelper.bytes_to_readable(share_size_bytes)
        return share_size_bytes

    def share_attribute(self, name, attribute):
        """Returns the value of the specified share attribute."""
        # Makes it easier to get a specific attribute without requiring a
        # function for each.
        if attribute in self.share(name):
            return self.share(name).get(attribute)
        raise ValueError("Specified attribute does not exist: " + attribute)
