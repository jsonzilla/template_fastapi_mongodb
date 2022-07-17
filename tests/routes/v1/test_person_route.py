from typing import AsyncGenerator
from app.models.person_model import example as valid_json
from app.repositories.person_repository import PersonRepository

from bson import objectid
import pytest_asyncio

_BASE_PATH = '/v1/person/'


@pytest_asyncio.fixture
async def id(db, session) -> AsyncGenerator:
    repo = PersonRepository()
    valid_json['_id'] = objectid.ObjectId().__str__()
    insert_id = await repo.insert(valid_json, db, session)
    yield insert_id
    await db[repo.collection].drop()


def test_read_person(client, id):
    response = client.get(f'{_BASE_PATH}')
    assert response.status_code == 200
    assert response.json() != valid_json


def test_read_person_by_fake_id(client, id):
    response = client.get('{_BASE_PATH}fake')
    assert response.status_code == 404
    assert response.json() != {}


def test_read_person_by_filter(client, id):
    response = client.get(f'{_BASE_PATH}?hobby=Sleeping')
    assert response.status_code == 200
    assert response.json() != {}


def test_read_person_by_id(client, id):
    response = client.get(f'{_BASE_PATH}{id}')
    assert response.status_code == 200
    assert response.json() != {}


def test_update_person(client, id):
    copy_valid_json = valid_json.copy()
    response = client.patch(
        f'{_BASE_PATH}{id}',
        json=copy_valid_json)
    assert response.status_code == 200
    assert response.json() != {}


def test_update_person_without_content(client, id):
    response = client.patch(f'{_BASE_PATH}{id}')
    assert response.status_code == 422
    assert response.json() != {}


def test_write_person(client):
    response = client.post(
        f'{_BASE_PATH}',
        json=valid_json)
    assert response.status_code == 201


def test_delete_person_fake_id(client):
    response = client.delete(f'{_BASE_PATH}fake')
    assert response.status_code == 404
    assert response.json() != {}


def test_delete_person(client, id):
    response = client.delete(f'{_BASE_PATH}{id}')
    assert response.status_code == 202
