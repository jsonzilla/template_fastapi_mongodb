from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.repositories.base_repository import BaseRepository
from app.storages.database_storage import Database


class BasicRoutable(object):
    def __init__(self, repo, element_name: str = "element"):
        self.repo: BaseRepository = repo
        self.element_name: str = element_name

    async def create(self, element: BaseModel, db: Database):
        """ Create a new element """
        element = jsonable_encoder(element)
        return await self.repo.create(element, db)

    async def post(self, element: BaseModel, db: Database):
        """ Create a new element return a json response with the created element """
        element = jsonable_encoder(element)
        return await self.repo.create(element, db)

    async def create_list(self, elements: list, db: Database):
        """ Create a new elements return a list of created elements """
        elements = jsonable_encoder(elements)
        return await self.repo.create_many(elements, db)

    async def post_list(self, elements: list, db: Database):
        """ Create a new elements return a list of json response with the created elements """
        elements = jsonable_encoder(elements)
        return await self.repo.create_many(elements, db)

    async def get_all(self, db: Database):
        """ Get all elements """
        return await self.repo.get_all(db)

    async def get_all_by(self, filter: dict, db: Database):
        """ Get all elements by filter """
        return await self.repo.get_all_by(filter, db)

    async def get_by_id(self, element_id: str, db: Database):
        """ Get an element by id """
        if (element := await self.repo.get_by_id(element_id, db)) is not None:
            return element
        raise HTTPException(status_code=404, detail=f"{self.element_name} {element_id} not found")

    async def delete(self, element_id: str, db: Database):
        """ Delete an element """
        delete_result = await self.repo.delete(element_id, db)
        if delete_result.deleted_count != 1:
            raise HTTPException(status_code=404, detail=f"{self.element_name} {element_id} not found")

    async def exists(self, filter: dict, db: Database) -> bool:
        """ Check if an element exists """
        return await self.repo.exists(filter, db)

    async def update_element(self, element_id: str, element, db: Database):
        """ Update an element return True if the element was updated """
        if type(element) is not dict:
            element = {k: v for k, v in element.dict().items() if v is not None}
        if len(element) >= 1:
            update_result = await self.repo.update(element_id, element, db)
            if update_result.modified_count == 1:
                return True
        return False

    async def patch(self, element_id: str, element: BaseModel, db: Database):
        """ Update an element """
        update_ok = await self.update_element(element_id, element, db)
        if update_ok:
            if (updated := await self.repo.get_by_id(element_id, db)) is not None:
                return updated
        raise HTTPException(status_code=404, detail=f"{self.element_name} {element_id} not found")

    async def patch_list(self, elements: list, db: Database):
        """ Update a list of elements """
        elements = jsonable_encoder(elements)
        updated = []
        for element in elements:
            element_id = element["_id"]
            await self.update_element(element_id, element, db)
            if (updated_or_existing := await self.repo.get_by_id(element_id, db)) is not None:
                updated.append(updated_or_existing)
        if len(elements) >= 1:
            if len(elements) == len(updated):
                return updated
            raise HTTPException(status_code=404, detail=f"{self.element_name}s not complete updated")
        raise HTTPException(status_code=404, detail=f"{self.element_name} not found")
