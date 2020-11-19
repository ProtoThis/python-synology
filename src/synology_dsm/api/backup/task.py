"""HyperBackup task data."""
from .const import PROP_DATA_ENCRYPTION
from .const import PROP_DATA_TYPE
from .const import PROP_NAME
from .const import PROP_SOURCE
from .const import PROP_STATE
from .const import PROP_STATUS
from .const import PROP_TARGET_ID
from .const import PROP_TARGET_TYPE
from .const import PROP_TASKID
from .const import PROP_TRANSFER_TYPE
from .const import PROP_TYPE


class SynoBackupTask:
    """Class containing HyperBackup task data."""

    def __init__(self, data):
        """Initialize a HyperBackup task."""
        self._data = data

    def update(self, data):
        """Update the task."""
        self._data = data

    @property
    def as_dict(self):
        """Return all details as dictionary."""
        return self._data

    @property
    def data_enc(self):
        """Return data encryption."""
        return self._data.get(PROP_DATA_ENCRYPTION)

    @property
    def data_type(self):
        """Return data type."""
        return self._data.get(PROP_DATA_TYPE)

    @property
    def name(self):
        """Return name."""
        return self._data.get(PROP_NAME)

    @property
    def source(self):
        """Return source."""
        return self._data.get(PROP_SOURCE)

    @property
    def state(self):
        """Return state."""
        return self._data.get(PROP_STATE)

    @property
    def status(self):
        """Return status."""
        return self._data.get(PROP_STATUS)

    @property
    def target_id(self):
        """Return target id."""
        return self._data.get(PROP_TARGET_ID)

    @property
    def target_type(self):
        """Return target type."""
        return self._data.get(PROP_TARGET_TYPE)

    @property
    def task_id(self):
        """Return task id."""
        return self._data.get(PROP_TASKID)

    @property
    def transfer_type(self):
        """Return transfer type."""
        return self._data.get(PROP_TRANSFER_TYPE)

    @property
    def type(self):
        """Return type."""
        return self._data.get(PROP_TYPE)
