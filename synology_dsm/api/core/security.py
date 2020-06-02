# -*- coding: utf-8 -*-
"""DSM Security data."""


class SynoCoreSecurity(object):
    """Class containing Security data."""

    API_KEY = "SYNO.Core.SecurityScan.Status"

    def __init__(self, raw_data):
        self._data = {}
        self.update(raw_data)

    def update(self, raw_data):
        """Updates security data."""
        if raw_data:
            self._data = raw_data["data"]

    @property
    def checks(self):
        """Gets the checklist by check category."""
        return self._data.get("items", {})

    @property
    def last_scan_time(self):
        """Gets the last scan time."""
        return self._data.get("lastScanTime")

    @property
    def start_time(self):
        """Gets the start time (if in progress)."""
        return self._data.get("startTime")

    @property
    def success(self):
        """Gets the last scan success."""
        return self._data.get("success")

    @property
    def progress(self):
        """Gets the scan progress (100 if finished)."""
        return self._data.get("sysProgress")

    @property
    def status(self):
        """Gets the last scan status (safe, danger, info, outOfDate, risk, warning)."""
        return self._data.get("sysStatus")

    @property
    def status_by_check(self):
        """Gets the last scan status per check."""
        status = {}
        for category in self.checks:
            status[category] = self.checks[category]["failSeverity"]
        return status
