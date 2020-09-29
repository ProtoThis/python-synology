"""DSM Utilization data."""
from synology_dsm.helpers import SynoFormatHelper


class SynoCoreUtilization:
    """Class containing Utilization data."""

    API_KEY = "SYNO.Core.System.Utilization"

    def __init__(self, dsm):
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates utilization data."""
        raw_data = self._dsm.get(self.API_KEY, "get")
        if raw_data:
            self._data = raw_data["data"]

    @property
    def cpu(self):
        """Gets CPU utilization."""
        return self._data.get("cpu", {})

    @property
    def cpu_other_load(self):
        """'Other' percentage of the total CPU load."""
        return self.cpu.get("other_load")

    @property
    def cpu_user_load(self):
        """'User' percentage of the total CPU load."""
        return self.cpu.get("user_load")

    @property
    def cpu_system_load(self):
        """'System' percentage of the total CPU load."""
        return self.cpu.get("system_load")

    @property
    def cpu_total_load(self):
        """Total CPU load for Synology DSM."""
        system_load = self.cpu_system_load
        user_load = self.cpu_user_load
        other_load = self.cpu_other_load

        if system_load is not None and user_load is not None and other_load is not None:
            return system_load + user_load + other_load
        return None

    @property
    def cpu_1min_load(self):
        """Average CPU load past minute."""
        return self.cpu.get("1min_load")

    @property
    def cpu_5min_load(self):
        """Average CPU load past 5 minutes."""
        return self.cpu.get("5min_load")

    @property
    def cpu_15min_load(self):
        """Average CPU load past 15 minutes."""
        return self.cpu.get("15min_load")

    @property
    def memory(self):
        """Gets memory utilization."""
        return self._data.get("memory")

    @property
    def memory_real_usage(self):
        """Real Memory usage from Synology DSM."""
        if self.memory:
            return str(self._data["memory"]["real_usage"])
        return None

    def memory_size(self, human_readable=False):
        """Total memory size of Synology DSM."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["memory_size"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def memory_available_swap(self, human_readable=False):
        """Total available memory swap."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["avail_swap"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def memory_cached(self, human_readable=False):
        """Total cached memory."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["cached"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def memory_available_real(self, human_readable=False):
        """Real available memory."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["avail_real"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def memory_total_real(self, human_readable=False):
        """Total available real memory."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["total_real"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def memory_total_swap(self, human_readable=False):
        """Total swap memory."""
        if self.memory:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["total_swap"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    @property
    def network(self):
        """Gets network utilization."""
        return self._data.get("network", [])

    def _get_network(self, network_id):
        """Function to get specific network (eth0, total, etc)."""
        for network in self.network:
            if network["device"] == network_id:
                return network
        return None

    def network_up(self, human_readable=False):
        """Total upload speed being used."""
        network = self._get_network("total")
        if network:
            return_data = int(network["tx"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None

    def network_down(self, human_readable=False):
        """Total download speed being used."""
        network = self._get_network("total")
        if network:
            return_data = int(network["rx"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            return return_data
        return None
