import pytest
import os
from .models import CustomUser
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        username="test",
        password="test1234",
    )


@pytest.fixture
def super_user(db):
    return CustomUser.objects.create_superuser(
        username="supertest",
        password="supertest1234",
    )


@pytest.fixture
def auth_client(user):
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client


@pytest.fixture
def auth_super_client(super_user):
    token = RefreshToken.for_user(super_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client


@pytest.fixture
def second_user(db):
    return CustomUser.objects.create_user(
        username="test_test",
        password="test1234",
    )


@pytest.fixture
def second_auth_client(second_user):
    token = RefreshToken.for_user(second_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client


@pytest.fixture(autouse=True)
def force_eager_celery(settings):
    """
    This fixture will run automatically before EVERY test.
    It switches Celery to synchronous mode, eliminating the need for Redis.
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
