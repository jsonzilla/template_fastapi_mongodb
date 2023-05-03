from copy import deepcopy
from typing import AsyncGenerator
from app.core.config import settings
from app.models.examples.user_example import another_example, basic_request_example
from app.storages.database_storage import Database
from app.repositories import UserRepository

from bson import objectid
import pytest_asyncio

valid_json = another_example

_APP_JSON = 'application/json'
_BASE_PATH = '/v1/admin/user/'


@pytest_asyncio.fixture
async def id(db: Database) -> AsyncGenerator:
    repo = UserRepository()
    valid_json['_id'] = objectid.ObjectId().__str__()
    inserted_id = await repo.insert(valid_json, db)
    yield inserted_id
    await db[repo.collection].drop()


def test_write_users(client, basic_auth_hash):
    example_copy = deepcopy(basic_request_example)
    example_copy['username'] = 'test'
    example_copy['email'] = 'j@j.com'
    response = client.post(
        _BASE_PATH,
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=example_copy)
    assert response.json()
    assert response.status_code == 201


def test_write_twice_same_users_must_trigger_an_error(client, basic_auth_hash):
    example_copy = deepcopy(basic_request_example)
    example_copy['username'] = 'twice'
    example_copy['email'] = 'j@j.com'
    response = client.post(
        _BASE_PATH,
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=example_copy)
    assert response.json()
    assert response.status_code == 201

    response = client.post(
        _BASE_PATH,
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=example_copy)
    assert response.json()
    assert response.status_code == 409


def test_read_users(client, basic_auth_hash):
    response = client.get(_BASE_PATH,
                          headers={
                              'Authorization': basic_auth_hash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert response.json() != {}


def test_read_users_by_fake_id(client, basic_auth_hash):
    response = client.get(f'{_BASE_PATH}fake',
                          headers={
                              'Authorization': basic_auth_hash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 404
    assert response.json() != {}


def test_read_users_by_id(client, id, basic_auth_hash):
    response = client.get(f'{_BASE_PATH}{id}',
                          headers={
                              'Authorization': basic_auth_hash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert response.json() != {}


def test_try_update_users_without_data(client, id, basic_auth_hash):
    response = client.put(f'{_BASE_PATH}{id}',
                          headers={
                              'Authorization': basic_auth_hash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 422
    assert response.json() != {}


def test_update_users(client, id, basic_auth_hash):
    basic_request_example_copy = deepcopy(basic_request_example)
    basic_request_example_copy.pop('username')
    basic_request_example_copy.pop('email')
    basic_request_example_copy['password'] = 'new_password'
    response = client.put(
        f'{_BASE_PATH}{id}',
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=basic_request_example_copy)
    assert response.status_code == 200
    assert response.json() != {}


def test_update_users_twice(client, id, basic_auth_hash):
    basic_request_example_copy = deepcopy(basic_request_example)
    basic_request_example_copy.pop('username')
    basic_request_example_copy.pop('email')
    basic_request_example_copy['password'] = 'new_password'

    response = client.put(
        f'{_BASE_PATH}{id}',
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=basic_request_example_copy)
    assert response.status_code == 200
    assert response.json() != {}


def test_update_with_empty_pass(client, id, basic_auth_hash):
    basic_request_example_copy = deepcopy(basic_request_example)
    basic_request_example_copy['password'] = ''

    response = client.put(
        f'{_BASE_PATH}{id}',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json=basic_request_example_copy)
    assert response.status_code == 422
    assert response.json() != {}


def test_update_non_existing_users(client, basic_auth_hash):
    response = client.put(
        f'{_BASE_PATH}fake',
        headers={
            'Content-Type': _APP_JSON,
            'Authorization': basic_auth_hash,
            'x-token': settings.API_TOKEN,
        },
        json={})
    assert response.status_code == 409
    assert response.json() != {'Invalid user'}


def test_delete_users_fake(client, basic_auth_hash):
    response = client.delete('{_BASE_PATH}fake',
                             headers={
                                 'Authorization': basic_auth_hash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 404
    assert response.json() != {}


def test_delete_users(client, id, basic_auth_hash):
    response = client.delete(f'{_BASE_PATH}{id}',
                             headers={
                                 'Authorization': basic_auth_hash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 204
