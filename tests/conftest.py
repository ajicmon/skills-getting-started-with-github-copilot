import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store

INITIAL_ACTIVITIES = copy.deepcopy(activities_store)


@pytest.fixture(autouse=True)
def reset_activities():
    activities_store.clear()
    activities_store.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    activities_store.clear()
    activities_store.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)
