"""DSM Utilisation data."""
# -*- coding:utf-8 -*-
from SynologyDSM.helpers import SynoFormatHelper


class SynoCoreUtilization(object):
    """Class containing Utilisation data."""

    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)

    def update(self, raw_input):
        """Allows updating Utilisation data with raw_input data."""
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def cpu_other_load(self):
        """'Other' percentage of the total cpu load."""
        if self._data is not None:
            return self._data["cpu"]["other_load"]

    @property
    def cpu_user_load(self):
        """'User' percentage of the total cpu load."""
        if self._data is not None:
            return self._data["cpu"]["user_load"]

    @property
    def cpu_system_load(self):
        """'System' percentage of the total cpu load."""
        if self._data is not None:
            return self._data["cpu"]["system_load"]

    @property
    def cpu_total_load(self):
        """Total CPU load for Synology DSM."""
        system_load = self.cpu_system_load
        user_load = self.cpu_user_load
        other_load = self.cpu_other_load

        if system_load is not None and user_load is not None and other_load is not None:
            return system_load + user_load + other_load

    @property
    def cpu_1min_load(self):
        """Average CPU load past minute."""
        if self._data is not None:
            return self._data["cpu"]["1min_load"]

    @property
    def cpu_5min_load(self):
        """Average CPU load past 5 minutes."""
        if self._data is not None:
            return self._data["cpu"]["5min_load"]

    @property
    def cpu_15min_load(self):
        """Average CPU load past 15 minutes."""
        if self._data is not None:
            return self._data["cpu"]["15min_load"]

    @property
    def memory_real_usage(self):
        """Real Memory Usage from Synology DSM."""
        if self._data is not None:
            return str(self._data["memory"]["real_usage"])

    def memory_size(self, human_readable=True):
        """Total Memory Size of Synology DSM."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["memory_size"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def memory_available_swap(self, human_readable=True):
        """Total Available Memory Swap."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["avail_swap"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def memory_cached(self, human_readable=True):
        """Total Cached Memory."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["cached"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def memory_available_real(self, human_readable=True):
        """Real available memory."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["avail_real"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def memory_total_real(self, human_readable=True):
        """Total available real memory."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["total_real"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def memory_total_swap(self, human_readable=True):
        """Total Swap Memory."""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return_data = int(self._data["memory"]["total_swap"]) * 1024
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def _get_network(self, network_id):
        """Function to get specific network (eth0, total, etc)."""
        if self._data is not None:
            for network in self._data["network"]:
                if network["device"] == network_id:
                    return network

    def network_up(self, human_readable=True):
        """Total upload speed being used."""
        network = self._get_network("total")
        if network is not None:
            return_data = int(network["tx"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data

    def network_down(self, human_readable=True):
        """Total download speed being used."""
        network = self._get_network("total")
        if network is not None:
            return_data = int(network["rx"])
            if human_readable:
                return SynoFormatHelper.bytes_to_readable(return_data)
            else:
                return return_data
