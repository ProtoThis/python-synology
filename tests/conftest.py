"""Main conftest."""
import pytest

from . import SynologyDSMMock
from . import VALID_HOST
from . import VALID_HTTPS
from . import VALID_PASSWORD
from . import VALID_PORT
from . import VALID_USER
from . import VALID_VERIFY_SSL
from synology_dsm.synology_dsm import SynologyDSM


@pytest.fixture
def api() -> SynologyDSM:
    """Return a mock DSM API."""
    return SynologyDSMMock(
        VALID_HOST,
        VALID_PORT,
        VALID_USER,
        VALID_PASSWORD,
        VALID_HTTPS,
        VALID_VERIFY_SSL,
    )


@pytest.fixture
def dsm(api) -> SynologyDSM:
    """Alias for api fixture."""
    return api


@pytest.fixture
def dsm_5(api) -> SynologyDSM:
    """Return a mock DSM 5 API."""
    api.dsm_version = 5
    return api
