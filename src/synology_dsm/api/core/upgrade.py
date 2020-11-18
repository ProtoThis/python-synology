"""DSM Upgrade data and actions."""


class SynoCoreUpgrade:
    """Class containing upgrade data and actions."""

    API_KEY = "SYNO.Core.Upgrade"
    API_SERVER_KEY = API_KEY + ".Server"

    def __init__(self, dsm):
        """Constructor method."""
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates Upgrade data."""
        raw_data = self._dsm.get(self.API_SERVER_KEY, "check")
        if raw_data:
            self._data = raw_data["data"].get("update", raw_data["data"])

    @property
    def update_available(self):
        """Gets available update info."""
        return self._data.get("available")

    @property
    def available_version(self):
        """Gets available verion info."""
        return self._data.get("version")

    @property
    def reboot_needed(self):
        """Gets info if reboot is needed."""
        return self._data.get("reboot")

    @property
    def service_restarts(self):
        """Gets info if services are restarted."""
        return self._data.get("restart")
