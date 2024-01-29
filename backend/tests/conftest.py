import pytest
from rest_framework.test import APIClient
from auth_api.models import CustomUser

@pytest.fixture(scope="function")
def client() -> APIClient:
    yield APIClient()