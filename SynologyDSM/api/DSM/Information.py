"""DSM Information data."""
# -*- coding:utf-8 -*-


class SynoDSMInformation(object):
    """Class containing Information data."""
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)

    def update(self, raw_input):
        """Allows updating Information data with raw_input data."""
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def model(self) -> str:
        """Model of the NAS."""
        if self._data is not None:
            return self._data["model"]

    @property
    def ram(self) -> int:
        """RAM of the NAS (in MB)."""
        if self._data is not None:
            return self._data["ram"]

    @property
    def serial(self) -> str:
        """Serial of the NAS."""
        if self._data is not None:
            return self._data["serial"]

    @property
    def temperature(self) -> int:
        """Temperature of the NAS."""
        if self._data is not None:
            return self._data["temperature"]

    @property
    def temperature_warn(self) -> bool:
        """Temperature warning of the NAS."""
        if self._data is not None:
            return self._data["temperature_warn"]

    @property
    def uptime(self) -> int:
        """Uptime of the NAS."""
        if self._data is not None:
            return self._data["uptime"]

    @property
    def version_string(self) -> str:
        """Version of the NAS."""
        if self._data is not None:
            return self._data["version_string"]
