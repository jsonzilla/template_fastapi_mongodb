from typing import AsyncGenerator
from app.codecs.object_id_codec import ObjectIdCodec
from app.repositories.base_repository import BaseRepository
from pydantic import BaseModel, Field
from bson import objectid
import pytest_asyncio

repo = BaseRepository('test_base_repository')


class BaseCaseModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    blablabla: str
    name: str


valid_json = {'Diana': '1', 'name': 'test'}


@pytest_asyncio.fixture
async def id(db) -> AsyncGenerator:
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    insert_id = await repo.insert(valid_json, db)
    yield insert_id
    await db[repo.collection].drop()


def generate_valid_json_list(n_items):
    xs = [{'Diana': '1', 'name': 'test'} for i in range(n_items)]
    for x in xs:
        x['_id'] = objectid.ObjectId().__str__()  # type: ignore
    return xs


async def test_create(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    assert valid_json == obj


async def test_insert(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert(valid_json, db)
    assert id == (await repo.get_by_id(id, db))['_id']


async def test_insert_many(db):
    a = valid_json.copy()
    a['_id'] = objectid.ObjectId().__str__()  # type: ignore
    b = valid_json.copy()
    b['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert_many([a, b], db)
    assert len(id) == 2
    assert id[0] == (await repo.get_by_id(id[0], db))['_id']
    assert id[1] == (await repo.get_by_id(id[1], db))['_id']


async def test_get_by_id(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert(valid_json, db)
    assert id == (await repo.get_by_id(id, db))['_id']


async def test_get_one(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert(valid_json, db)
    assert id == (await repo.get_one({'_id': id}, db))['_id']


async def test_get_by_with_id(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert(valid_json, db)
    assert id == (await repo.get_by({'_id': id}, db))[0]['_id']


async def test_get_by_with_name(db):
    await db[repo.collection].drop()
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    assert obj == (await repo.get_by({'name': valid_json['name']}, db))[0]


async def test_get_by_and_sort(db):
    await db[repo.collection].drop()
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    assert obj == (await repo.get_by_and_sort({'name': valid_json['name']}, 'name', db))[0]


async def test_get_all(db):
    await db[repo.collection].drop()
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    assert obj == (await repo.get_all(db))[0]


async def test_update(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    obj['name'] = 'test2'
    await repo.update(obj['_id'], obj, db)
    assert obj == (await repo.get_by_id(obj['_id'], db))


async def test_update_list(db):
    await db[repo.collection].drop()
    xs = generate_valid_json_list(105)
    res_xs = await repo.insert_many(xs, db)
    assert len(res_xs) == 105
    for x in xs:
        x['name'] = 'test_nam_changed'

    res_update = await repo.update_list(xs, db)
    assert len(res_update) == 105


async def test_delete(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    obj = await repo.create(valid_json, db)
    await repo.delete(obj['_id'], db)
    assert (await repo.get_by_id(obj['_id'], db)) is None


async def test_get_by_and_sort_with_pagination(db):
    await db[repo.collection].drop()
    xs = await repo.insert_many(generate_valid_json_list(105), db)
    assert len(xs) == 105
    assert len(await repo.get_by_and_sort_with_pagination({'name': 'test'}, 'name', page=1, per_page=10, db=db)) == 10
    assert len(await repo.get_by_and_sort_with_pagination({'name': 'test'}, 'name', page=2, per_page=10, db=db)) == 10
    assert len(await repo.get_by_and_sort_with_pagination({'name': 'test'}, 'name', page=10, per_page=10, db=db)) == 5


async def test_exists(db):
    valid_json['_id'] = objectid.ObjectId().__str__()  # type: ignore
    id = await repo.insert(valid_json, db)
    assert await repo.exists({'_id': id}, db) is True
    assert await repo.exists({'_id': '123'}, db) is False
