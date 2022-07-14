
from app.storages.database_storage import Database


class BaseRepository(object):
    __slots__ = ['collection']

    def __init__(self, table_name):
        self.collection: str = table_name

    async def create(self, element, db: Database):
        """ Create a new element in the repository. """
        insert_id = await self.insert(element, db)
        return await self.get_by_id(insert_id, db)

    async def insert(self, element, db: Database) -> str:
        """ Insert a new element in the repository. """
        return (await db[self.collection].insert_one(element)).inserted_id

    async def create_many(self, elements: list, db: Database) -> list:
        """ Create a new element in the repository. """
        ids_list = await self.insert_many(elements, db)
        return await db[self.collection].find({"_id": {"$in": ids_list}}).to_list(None)

    async def insert_many(self, elements: list, db: Database) -> list:
        """ Insert a new element in the repository. """
        return (await db[self.collection].insert_many(elements)).inserted_ids

    async def get_by_id(self, id: str, db: Database):
        """ Get an element by id. """
        return await db[self.collection].find_one({'_id': id})

    async def get_one(self, filter: dict, db: Database):
        """ Get an element by id. """
        return await db[self.collection].find_one(filter)

    async def get_by(self, filter: dict, db: Database) -> list:
        """ Get an element by id. """
        return await db[self.collection].find(filter).to_list(None)

    async def get_by_and_sort(self, filter: dict, sort_field, db: Database) -> list:
        """ Get an element by id. """
        return await db[self.collection].find(filter).sort(sort_field).to_list(None)

    async def get_all(self, db: Database) -> list:
        """ Get all elements in the repository. """
        return await db[self.collection].find().to_list(None)

    async def get_all_by(self, filter: dict, db: Database) -> list:
        """ Get all elements in the repository. """
        return await db[self.collection].find(filter).to_list(None)

    async def update(self, id: str, element, db: Database):
        """ Update an element in the repository. """
        return await db[self.collection].update_one({'_id': id}, {'$set': element})

    async def update_list(self, elements: list, db: Database) -> list:
        """ Update a list of elements in the repository. """
        results = []
        for element in elements:
            result = await self.update(element['_id'], element, db)
            results.append(result)
        return results

    async def delete(self, id: str, db: Database):
        """ Delete an element by id. """
        return await db[self.collection].delete_one({'_id': id})

    async def delete_many(self, filter: dict, db: Database):
        """ Delete an element by id. """
        return await db[self.collection].delete_many(filter)

    async def get_by_and_sort_with_pagination(self, filter: dict, sort_field, page: int, per_page: int, db):
        """ Get an element by id. """
        return await db[self.collection].find(filter).sort(sort_field).skip(page * per_page).limit(per_page).to_list(None)

    async def exists(self, filter: dict, db: Database) -> bool:
        """ Check if an element exists. """
        return await db[self.collection].count_documents(filter) > 0
