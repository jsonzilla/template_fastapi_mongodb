from app.storages.database_filter import format_to_database_filter
from fastapi import APIRouter, Depends, Body
from typing import List
from app.storages.database_storage import Database, get_db
from app.models.person_model import PersonModel, PersonUpdateModel, filter_to_nested_model, PersonFilterModel
from app.repositories.person_repository import PersonRepository
from app.routes import BasicRoutable

_SHOW_NAME = "person"
router = APIRouter(
    prefix=f"/v1/{_SHOW_NAME}",
    tags=[_SHOW_NAME],
    responses={404: {"description": "Not found"}}
)
_ROUTER = BasicRoutable(PersonRepository(), _SHOW_NAME)
_MODEL = PersonModel
_UPDATE_MODEL = PersonUpdateModel
_FILTER = PersonFilterModel


@router.get("/", response_description=f"List all {_SHOW_NAME}s", response_model=List[_UPDATE_MODEL])
async def list(filter: _FILTER = Depends(_FILTER), db: Database = Depends(get_db)):
    nested = filter_to_nested_model(filter)
    db_filter = format_to_database_filter(nested.dict())
    return await _ROUTER.get_all_by(db_filter, db)


@router.get("/{id}", response_description=f"Get by id {_SHOW_NAME}", response_model=_UPDATE_MODEL)
async def show_by_id(id: str, db: Database = Depends(get_db)):
    return await _ROUTER.get_by_id(id, db)


@router.post("/", response_description=f"Add new {_SHOW_NAME}", response_model=_UPDATE_MODEL, status_code=201)
async def create(model: _MODEL = Body(...), db: Database = Depends(get_db)):
    return await _ROUTER.post(model, db)


@router.delete("/{id}", response_description=f"Delete a {_SHOW_NAME}", status_code=202)
async def delete(id: str, db: Database = Depends(get_db)):
    return await _ROUTER.delete(id, db)


@router.patch("/{id}", response_description=f"Update a {_SHOW_NAME}", response_model=_UPDATE_MODEL)
async def update(id: str, model: _UPDATE_MODEL = Body(...), db: Database = Depends(get_db)):
    return await _ROUTER.patch(id, model, db)
