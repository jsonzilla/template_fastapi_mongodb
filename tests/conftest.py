import os
import sys
from typing import Any, Generator, Optional
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.storages.database_storage import Database, Session, get_db, get_db_session
from app.main import get_application

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a new FastAPI application.
    """
    _app = get_application()
    yield _app


@pytest.fixture(scope="module")
def client(app: FastAPI, db) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI test client.
    """
    async def _get_test_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def session(app: FastAPI) -> Generator[Optional[Session], Any, None]:
    """
    Create a new FastAPI test client.
    """
    async def _get_test_session():
        try:
            yield None
        finally:
            pass

    app.dependency_overrides[get_db_session] = _get_test_session
    yield None


@pytest.fixture(scope="module")
def db() -> Generator[Database, Any, None]:
    """
    Create a new MongoDB mock database.
    """
    client = AsyncMongoMockClient()
    return client.test_base
