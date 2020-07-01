"""Synology DownloadStation API wrapper."""
from .task import SynoDownloadTask


class SynoDownloadStation(object):
    """An implementation of a Synology DownloadStation."""

    API_KEY = "SYNO.DownloadStation.*"
    INFO_API_KEY = "SYNO.DownloadStation.Info"
    TASK_API_KEY = "SYNO.DownloadStation.Task"

    def __init__(self, dsm):
        """Initialize a Download Station."""
        self._dsm = dsm
        self._tasks_by_id = {}
        self.additionals = [
            "detail",
            "file",
        ]  # Can contain: detail, transfer, file, tracker, peer

    def update(self):
        """Update tasks from API."""
        list_data = self._dsm.get(
            self.TASK_API_KEY, "List", {"additional": ",".join(self.additionals)}
        )["data"]
        for task_data in list_data["tasks"]:
            if task_data["id"] in self._tasks_by_id:
                self._tasks_by_id[task_data["id"]].update(task_data)
            else:
                self._tasks_by_id[task_data["id"]] = SynoDownloadTask(task_data)

    # Global
    def get_info(self):
        """Return general informations about the Download Station instance."""
        return self._dsm.get(self.INFO_API_KEY, "GetInfo")

    # Downloads
    def get_all_tasks(self):
        """Return a list of tasks."""
        return self._tasks_by_id.values()

    def get_task(self, task_id):
        """Return task matching task_id."""
        return self._tasks_by_id[task_id]

    def create(self, uri, unzip_password=None):
        """Create a new task (uri accepts HTTP/FTP/magnet/ED2K links)."""
        return self._dsm.get(
            self.TASK_API_KEY,
            "create",
            {"uri": ",".join(uri), "unzip_password": unzip_password},
        )

    def pause(self, task_id):
        """Pause a download task."""
        return self._dsm.get(self.TASK_API_KEY, "pause", {"id": ",".join(task_id)})

    def delete(self, task_id, force_complete=False):
        """Delete a download task."""
        return self._dsm.get(
            self.TASK_API_KEY,
            "delete",
            {"id": ",".join(task_id), "force_complete": force_complete},
        )
