from typing import Optional
from app.storages.database_storage import Database, Session


class BaseRepository(object):
    __slots__ = ['collection']

    def __init__(self, table_name):
        self.collection: str = table_name

    async def create(self, element, db: Database, s: Optional[Session] = None):
        """ Create a new element in the repository. """
        insert_id = await self.insert(element, db, s)
        return await self.get_by_id(insert_id, db, s)

    async def insert(self, element, db: Database, s: Optional[Session] = None) -> str:
        """ Insert a new element in the repository. """
        return (await db[self.collection].insert_one(element, session=s)).inserted_id

    async def create_many(self, elements: list, db: Database, s: Optional[Session] = None) -> list:
        """ Create a new element in the repository. """
        ids_list = await self.insert_many(elements, db, s)
        return await db[self.collection].find({"_id": {"$in": ids_list}}, session=s).to_list(None)

    async def insert_many(self, elements: list, db: Database, s: Optional[Session] = None) -> list:
        """ Insert a new element in the repository. """
        return (await db[self.collection].insert_many(elements, session=s)).inserted_ids

    async def get_by_id(self, id: str, db: Database, s: Optional[Session] = None):
        """ Get an element by id. """
        return await db[self.collection].find_one({'_id': id}, session=s)

    async def get_one(self, filter: dict, db: Database, s: Optional[Session] = None):
        """ Get an element by id. """
        return await db[self.collection].find_one(filter, session=s)

    async def get_by(self, filter: dict, db: Database, s: Optional[Session] = None) -> list:
        """ Get an element by id. """
        return await db[self.collection].find(filter, session=s).to_list(None)

    async def get_by_and_sort(self, filter: dict, sort_field, db: Database, s: Optional[Session] = None) -> list:
        """ Get an element by id. """
        return await db[self.collection].find(filter, session=s).sort(sort_field).to_list(None)

    async def get_all(self, db: Database, s: Optional[Session] = None) -> list:
        """ Get all elements in the repository. """
        return await db[self.collection].find(session=s).to_list(None)

    async def get_all_by(self, filter: dict, db: Database, s: Optional[Session] = None) -> list:
        """ Get all elements in the repository. """
        return await db[self.collection].find(filter, session=s).to_list(None)

    async def update(self, id: str, element, db: Database, s: Optional[Session] = None):
        """ Update an element in the repository. """
        return await db[self.collection].update_one({'_id': id}, {'$set': element}, session=s)

    async def update_list(self, elements: list, db: Database, s: Optional[Session] = None) -> list:
        """ Update a list of elements in the repository. """
        results = []
        for element in elements:
            result = await self.update(element['_id'], element, db, s)
            results.append(result)
        return results

    async def delete(self, id: str, db: Database, s: Optional[Session] = None):
        """ Delete an element by id. """
        return await db[self.collection].delete_one({'_id': id}, session=s)

    async def delete_many(self, filter: dict, db: Database, s: Optional[Session] = None):
        """ Delete an element by id. """
        return await db[self.collection].delete_many(filter, session=s)

    async def get_by_and_sort_with_pagination(self, filter: dict, sort_field, page: int, per_page: int, db: Database, s: Optional[Session] = None) -> list:
        """ Get an element by id. """
        return await db[self.collection].find(filter, session=s).sort(sort_field).skip(page * per_page).limit(per_page).to_list(None)

    async def exists(self, filter: dict, db: Database, s: Optional[Session] = None) -> bool:
        """ Check if an element exists. """
        return await db[self.collection].count_documents(filter, session=s) > 0
