"""Synology Backup API models."""
from .const import PROP_TASKID
from .task import SynoBackupTask


class SynoBackup:
    """An implementaion of Synology HyperBackup."""

    API_KEY = "SYNO.Backup.*"
    API_KEY_TASK = "SYNO.Backup.Task"

    def __init__(self, dsm):
        """Initialize HyperBackup."""
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Update backup tasks settings and information from API."""
        self._data = {}
        task_list = self._dsm.get(self.API_KEY_TASK, "list", max_version=1)["data"].get(
            "task_list", []
        )
        for task in task_list:
            self._data[task[PROP_TASKID]] = SynoBackupTask(
                self._dsm.get(
                    self.API_KEY_TASK,
                    "get",
                    {PROP_TASKID: task[PROP_TASKID]},
                    max_version=1,
                )["data"]
            )

    def get_all_tasks(self):
        """Return a list of all tasks."""
        return self._data.values()

    def get_task(self, task_id):
        """Return task matching task_id."""
        return self._data[task_id]
