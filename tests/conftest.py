from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as application


@pytest.fixture(scope="session")
def client():
    """TestClient instance for the FastAPI app."""
    return TestClient(application.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the global activities dictionary around each test.

    A deepcopy of the original `application.activities` is taken before a test
    runs and then the shared object is replaced after the test finishes. This
    prevents state leakage between tests.
    """
    original = deepcopy(application.activities)
    yield
    application.activities.clear()
    application.activities.update(original)
