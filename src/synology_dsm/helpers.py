"""Helpers."""


class SynoFormatHelper:
    """Class containing various formatting functions."""

    @staticmethod
    def bytes_to_readable(num):
        """Converts bytes to a human readable format."""
        if num < 512:  # pylint: disable=no-else-return
            return "0 Kb"
        elif num < 1024:
            return "1 Kb"

        for unit in ["", "Kb", "Mb", "Gb", "Tb", "Pb", "Eb", "Zb"]:
            if abs(num) < 1024.0:
                return "%3.1f%s" % (num, unit)
            num /= 1024.0
        return "%.1f%s" % (num, "Yb")

    @staticmethod
    def bytes_to_megabytes(num):
        """Converts bytes to megabytes."""
        var_mb = num / 1024.0 / 1024.0

        return round(var_mb, 1)

    @staticmethod
    def bytes_to_gigabytes(num):
        """Converts bytes to gigabytes."""
        var_gb = num / 1024.0 / 1024.0 / 1024.0

        return round(var_gb, 1)

    @staticmethod
    def bytes_to_terrabytes(num):
        """Converts bytes to terrabytes."""
        var_tb = num / 1024.0 / 1024.0 / 1024.0 / 1024.0

        return round(var_tb, 1)

    @staticmethod
    def megabytes_to_bytes(num):
        """Converts megabytes to bytes."""
        var_bytes = num * 1024.0 * 1024.0

        return round(var_bytes, 1)
