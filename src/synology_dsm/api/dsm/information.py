"""DSM Information data."""


class SynoDSMInformation:
    """Class containing Information data."""

    API_KEY = "SYNO.DSM.Info"

    def __init__(self, dsm):
        """Constructor methods."""
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates information data."""
        raw_data = self._dsm.get(self.API_KEY, "getinfo")
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
    def version(self):
        """Version of the NAS (build version)."""
        return self._data.get("version")

    @property
    def version_string(self):
        """Version of the NAS."""
        return self._data.get("version_string")
