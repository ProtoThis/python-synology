"""SurveillanceStation camera."""
from .const import MOTION_DETECTION_DISABLED
from .const import RECORDING_STATUS


class SynoCamera:
    """An representation of a Synology SurveillanceStation camera."""

    def __init__(self, data, live_view_data=None):
        """Initialize a Surveillance Station camera."""
        self._data = data
        self.live_view = SynoCameraLiveView(live_view_data)
        self._motion_detection_enabled = None

    def update(self, data):
        """Update the camera."""
        self._data = data

    def update_motion_detection(self, data):
        """Update the camera motion detection."""
        self._motion_detection_enabled = (
            MOTION_DETECTION_DISABLED != data["MDParam"]["source"]
        )

    @property
    def id(self):
        """Return id of the camera."""
        return self._data["id"]

    @property
    def name(self):
        """Return name of the camera."""
        return self._data["name"]

    @property
    def model(self):
        """Return model of the camera."""
        return self._data["model"]

    @property
    def resolution(self):
        """Return resolution of the camera."""
        return self._data["resolution"]

    @property
    def fps(self):
        """Return FPS of the camera."""
        return self._data["fps"]

    @property
    def is_enabled(self):
        """Return true if camera is enabled."""
        return self._data["enabled"]

    @property
    def is_motion_detection_enabled(self):
        """Return true if motion detection is enabled."""
        return self._motion_detection_enabled

    @property
    def is_recording(self):
        """Return true if camera is recording."""
        return self._data["recStatus"] in RECORDING_STATUS


class SynoCameraLiveView:
    """An representation of a Synology SurveillanceStation camera live view."""

    def __init__(self, data):
        """Initialize a Surveillance Station camera live view."""
        self.update(data)

    def update(self, data):
        """Update the camera live view."""
        self._data = data

    @property
    def mjpeg_http(self):
        """Return the mjpeg stream (over http) path of the camera."""
        return self._data["mjpegHttpPath"]

    @property
    def multicast(self):
        """Return the multi-cast path of the camera."""
        return self._data["multicstPath"]

    @property
    def mxpeg_http(self):
        """Return the mxpeg stream path of the camera."""
        return self._data["mxpegHttpPath"]

    @property
    def rtsp_http(self):
        """Return the RTSP stream (over http) path of the camera."""
        return self._data["rtspOverHttpPath"]

    @property
    def rtsp(self):
        """Return the RTSP stream path of the camera."""
        return self._data["rtspPath"]
