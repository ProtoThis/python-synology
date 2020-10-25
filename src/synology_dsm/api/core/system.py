"""DSM System data and actions."""


class SynoCoreSystem:
    """Class containing System data and actions."""

    API_KEY = "SYNO.Core.System"

    def __init__(self, dsm):
        """Constructor method."""
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates System data."""
        raw_data = self._dsm.get(self.API_KEY, "info")
        if raw_data:
            self._data = raw_data["data"]

    #
    # get information
    #
    @property
    def cpu_clock_speed(self):
        """Gets System CPU clock speed."""
        return self._data.get("cpu_clock_speed")

    @property
    def cpu_cores(self):
        """Gets System CPU cores."""
        return self._data.get("cpu_cores")

    @property
    def cpu_family(self):
        """Gets System CPU family."""
        return self._data.get("cpu_family")

    @property
    def cpu_series(self):
        """Gets System CPU series."""
        return self._data.get("cpu_series")

    @property
    def enabled_ntp(self):
        """Gets System NTP state."""
        return self._data.get("enabled_ntp")

    @property
    def ntp_server(self):
        """Gets System NTP server."""
        return self._data.get("ntp_server")

    @property
    def firmware_ver(self):
        """Gets System firmware version."""
        return self._data.get("firmware_ver")

    @property
    def model(self):
        """Gets System model."""
        return self._data.get("model")

    @property
    def ram_size(self):
        """Gets System ram size."""
        return self._data.get("ram_size")

    @property
    def serial(self):
        """Gets System serial number."""
        return self._data.get("serial")

    @property
    def sys_temp(self):
        """Gets System temperature."""
        return self._data.get("sys_temp")

    @property
    def time(self):
        """Gets System time."""
        return self._data.get("time")

    @property
    def time_zone(self):
        """Gets System time zone."""
        return self._data.get("time_zone")

    @property
    def time_zone_desc(self):
        """Gets System time zone description."""
        return self._data.get("time_zone_desc")

    @property
    def up_time(self):
        """Gets System uptime."""
        return self._data.get("up_time")

    @property
    def usb_dev(self):
        """Gets System connected usb devices."""
        return self._data.get("usb_dev", [])

    #
    # do system actions
    #
    def shutdown(self):
        """Shutdown NAS."""
        res = self._dsm.get(
            self.API_KEY,
            "shutdown",
            max_version=1,  # shutdown method is only available on api version 1
        )
        return res

    def reboot(self):
        """Reboot NAS."""
        res = self._dsm.get(
            self.API_KEY,
            "reboot",
            max_version=1,  # reboot method is only available on api version 1
        )
        return res
