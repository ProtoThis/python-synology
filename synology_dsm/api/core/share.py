# -*- coding: utf-8 -*-
"""Shared Folders data."""


class SynoShare(object):
    """Class containing Share data."""

    API_KEY = "SYNO.Core.Share"

    def __init__(self, dsm):
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates share data."""
        raw_data = self._dsm.get(self.API_KEY, "list")
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
    def shares_uuids(self):
        """Returns (internal) share UUIDs."""
        shares = []
        for share in self.shares:
            shares.append(share["uuid"])
        return shares

    def _get_share(self, uuid):
        """Returns a specific share."""
        for share in self.shares:
            if share["uuid"] == uuid:
                return share
        return {}

    def share_name(self, uuid):
        """The name of this share."""
        return self._get_share(uuid).get("name")

    def share_path(self, uuid):
        """The volume path of this share."""
        return self._get_share(uuid).get("vol_path")
