from typing import List, Union
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body
from app.core.hasher import Hasher
from app.core.security import validate_auth
from app.storages.database_storage import get_db
from app.models import UserModel, UpdateUserModel, ShowUserModel, CreateUserModel
from app.repositories import UserRepository
from app.routes import BasicRouter

_name = "user"
router = APIRouter(
    prefix=f"/v1/admin/{_name}",
    tags=[_name],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(validate_auth)]
)
_repo = UserRepository()
_impl = BasicRouter(_repo, _name)


def _clean_user(user):
    """
    Remove password from user
    :param user:
    :return: user without password
    """
    del user['password']
    return user


def _clean_users(users):
    """
    Remove password from user
    :param users:
    :return: users without password
    """
    for user in users:
        _clean_user(user)
    return users


@router.post("/", response_description=f"Add new {_name}", response_model=Union[UserModel, None], status_code=201)
async def create(user_insert: CreateUserModel = Body(...), db=Depends(get_db)):
    user = user_insert.dict()
    user["last_update_datetime"] = datetime.utcnow().timestamp()
    user["password"] = Hasher.get_password_hash(user["password"])
    if await _repo.exists({'$or': [{"username": user["username"]}, {"email": user["email"]}]}, db):
        raise HTTPException(status_code=409, detail="Already exists")

    return await _impl.post(UserModel(**user), db)


@router.get("/", response_description=f"List all {_name}s", response_model=Union[List[ShowUserModel], None])
async def list(db=Depends(get_db)):
    return _clean_users(await _impl.get_all(db))


@router.get("/{id}", response_description=f"Get a single {_name}", response_model=Union[ShowUserModel, None])
async def show(id: str, db=Depends(get_db)):
    return _clean_user(await _impl.get_by_id(id, db))


@router.put("/{id}", response_description=f"Update a {_name}", response_model=Union[ShowUserModel, None])
async def update(id: str, user: UpdateUserModel = Body(...), db=Depends(get_db)):
    if user is None or user.password is None:
        raise HTTPException(status_code=409, detail="Invalid user")
    user.password = Hasher.get_password_hash(user.password)
    user.last_update_datetime = datetime.utcnow()

    return _clean_user(await _impl.put(id, user, db))


@ router.delete("/{id}", response_description=f"Delete a {_name}", status_code=204)
async def delete(id: str, db=Depends(get_db)):
    return await _impl.delete(id, db)
