# -*- coding: utf-8 -*-
"""DSM Information data."""


class SynoDSMInformation(object):
    """Class containing Information data."""

    API_KEY = "SYNO.DSM.Info"

    def __init__(self, raw_data):
        self._data = {}
        self.update(raw_data)

    def update(self, raw_data):
        """Updates information data."""
        if raw_data:
            self._data = raw_data["data"]

    @property
    def model(self):
        """Model of the NAS."""
        return self._data.get("model")

    @property
    def ram(self):
        """RAM of the NAS (in MB)."""
        return self._data.get("ram")

    @property
    def serial(self):
        """Serial of the NAS."""
        return self._data.get("serial")

    @property
    def temperature(self):
        """Temperature of the NAS."""
        return self._data.get("temperature")

    @property
    def temperature_warn(self):
        """Temperature warning of the NAS."""
        return self._data.get("temperature_warn")

    @property
    def uptime(self):
        """Uptime of the NAS."""
        return self._data.get("uptime")

    @property
    def version_string(self):
        """Version of the NAS."""
        return self._data.get("version_string")
