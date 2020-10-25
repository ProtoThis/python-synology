"""DownloadStation task."""


class SynoDownloadTask:
    """An representation of a Synology DownloadStation task."""

    def __init__(self, data):
        """Initialize a Download Station task."""
        self._data = data

    def update(self, data):
        """Update the task."""
        self._data = data

    @property
    def id(self):
        """Return id of the task."""
        return self._data["id"]

    @property
    def title(self):
        """Return title of the task."""
        return self._data["title"]

    @property
    def type(self):
        """Return type of the task (bt, nzb, http(s), ftp, emule)."""
        return self._data["type"]

    @property
    def username(self):
        """Return username of the task."""
        return self._data["username"]

    @property
    def size(self):
        """Return size of the task."""
        return self._data["size"]

    @property
    def status(self):
        """Return status of the task.

        Possible values: waiting, downloading, paused, finishing, finished,
            hash_checking, seeding, filehosting_waiting, extracting, error
        """
        return self._data["status"]

    @property
    def status_extra(self):
        """Return status_extra of the task."""
        return self._data.get("status_extra")

    @property
    def additional(self):
        """Return additional data of the task."""
        return self._data["additional"]
