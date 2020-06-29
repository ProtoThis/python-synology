class SynoShare(object):
    """Class containing Share data."""

    API_KEY = "SYNO.Core.Share"
    SHARE_PARAMS = {"additional": '"hidden", "encryption", "is_aclmode", '
                                  '"unite_permission", "is_support_acl", '
                                  '"is_sync_share", "is_force_readonly", '
                                  '"force_readonly_reason", "recyclebin", '
                                  '"is_share_moving", "is_cluster_share", '
                                  '"is_exfat_share", "is_cold_storage_share", '
                                  '"support_snapshot", "share_quota", '
                                  '"enable_share_compress", "enable_share_cow", '
                                  '"include_cold_storage_share", '
                                  '"is_cold_storage_share"',
                    "shareType": "all"}

    def __init__(self, raw_data):
        self._data = {}
        self.update(raw_data)

    def update(self, raw_data):
        """Updates share data."""
        if raw_data:
            self._data = raw_data
            if raw_data.get("data"):
                self._data = raw_data["data"]

    @property
    # Some changes required here to support SHARE_PARAMS.
    def shares(self):
        """Gets all shares."""
        return self._data.get("shares", [])

    def share(self, share_name):
        """Returns a specific share."""
        for share in self.shares:
            if share["name"] == share_name:
                return share
        return {}
