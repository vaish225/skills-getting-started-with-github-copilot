import copy
import urllib.parse
import warnings

# Silence Starlette/httpx deprecation warning from TestClient
# (Using `httpx` with `starlette.testclient` is deprecated)
warnings.filterwarnings(
    "ignore",
    message=r"Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead\.",
)

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


# Snapshot of initial activities to restore between tests
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` structure before each test."""
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)
