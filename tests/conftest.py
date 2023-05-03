import os
import sys
import base64
from typing import Any, AsyncGenerator, Generator
from app.repositories.user_repository import UserRepository
from bson import objectid
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.storages.database_storage import Database, get_db
from app.main import get_application
from app.models.examples.user_example import basic_request_example, example

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
def db() -> Generator[Database, Any, None]:
    """
    Create a new MongoDB mock database.
    """
    client = AsyncMongoMockClient()
    return client.test_base


@pytest_asyncio.fixture
async def basic_auth_hash(db: Database) -> AsyncGenerator:
    repo = UserRepository()
    example['_id'] = objectid.ObjectId().__str__()
    await repo.insert(example, db)
    auth: str = basic_request_example['username'] + ":" + basic_request_example['password']
    base64_hash = "Basic " + str(base64.b64encode(auth.encode())).replace("b'", "").replace("'", "")
    yield base64_hash
    await db[repo.collection].drop()
