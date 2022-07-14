# Template project FastAPI with MongoDB

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

## Install the requirements:
A mongo database is required to run the server.
Get one from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), for free.
```bash
pip install -r requirements.txt
```

## Run locally
```bash
uvicorn app.main:app --reload
```
To see the Swagger documentation, visit:
http://localhost:8000/docs

### Test
```bash
python -m pytest -W ignore::DeprecationWarning
pytest --cov=app --cov-report=html
python -m pytest_watch
```

### Test watch
```bash
ptw
```

## [Config .env](https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file)
Configure the location of your MongoDB database in a .env file:
```
MONGO_URL="mongodb://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
```



# Steps to create a new model
Using the tools below, you can create a new model.
**Tools**:
* [jsontopydantic](https://jsontopydantic.com/)
* [datamodel-code-generator](https://koxudaxi.github.io/datamodel-code-generator/)

## 1. Define a new model
Json base for our model:
```json
{
    "name": "Jack of all trades",
    "age": "42",
    "occupation": "King of the world",
    "hobbies": [
        "Sleeping",
        "Eating",
        "Being a jack of all trades"
    ],
    "friends": [
        {"name": "Jill", "age": "42", "occupation": "King of the another world"},
        {"name": "Jane", "age": "50", "occupation": "Queen of the another world"}
    ],
    "created_at": "2020-01-01T00:00:00.000Z",
    "last_update": "2020-01-01T00:00:00.000Z"
}
```
Copy this example to your project folder ```models/examples``` and rename it to ```<model_name>_example.py```.
This will be user for swagger documentation and unit tests.
```python
example = ...code above...
example_update = example
```


### 1.1 Generate the model with the tools:
use the site or datamodel-code-generator to generate all models from json. **Tool**: [jsontopydantic](https://jsontopydantic.com/)

```python
from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Friend(BaseModel):
    name: str
    age: str
    occupation: str


class Model(BaseModel):
    name: str
    age: str
    occupation: str
    hobbies: List[str]
    friends: List[Friend]
    created_at: str
    last_update: str
```


## 2. Create the model in project
In models folder, create a new file with the name of the model and the extension .py.
In this example the file name is ```<model_name>_model.py```..

### Import to the librarys:
```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from app.codecs import ObjectIdCodec
from app.models.examples.person_example import example, example_update
```

### 2.1 Copy the models and format the code:
Create the models, add the fields and the validators.
```python
class Friend(BaseModel):
    name: str = Field(description='Name of the friend', min_length=1, max_length=100)
    age: Optional[int] = Field(description='Age of the friend', ge=0)
    occupation: Optional[str] = Field(description='Occupation of the friend', min_length=1, max_length=255)


class PersonModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    name: str = Field(description="The name of the person", min_length=1, max_length=255)
    age: int = Field(description="The age of the person", gt=0)
    occupation: str = Field(description="The occupation of the person", min_length=1, max_length=255)
    hobbies: List[str] = Field(description="The hobbies of the person")
    friends: List[Friend] = Field(description="The friends of the person")
    created_at: datetime = Field(description="The creation date of the person")
    last_update: datetime = Field(description="The last update of the person")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}


class PersonUpdateModel(BaseModel):
    name: Optional[str] = Field(description="The name of the person", min_length=1, max_length=255)
    age: Optional[str] = Field(description="The age of the person", min_length=1, max_length=255)
    occupation: Optional[str] = Field(description="The occupation of the person", min_length=1, max_length=255)
    hobbies: Optional[List[str]] = Field(description="The hobbies of the person")
    friends: Optional[List[Friend]] = Field(description="The friends of the person")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example_update}
```

### 2.2 Create additional model for update:
```python
class PersonFilterModel(BaseModel):
    name: Optional[str] = Field(description="The name of the person", min_length=1, max_length=255)
    age: Optional[str] = Field(description="The age of the person", min_length=1, max_length=255)
    occupation: Optional[str] = Field(description="The occupation of the person", min_length=1, max_length=255)
    hobby: Optional[str] = Field(description="The hobby of the person")
    friend_name: Optional[str] = Field(description="The friends of the person")
    created_at: Optional[datetime] = Field(description="The creation date of the person")
    last_update: Optional[datetime] = Field(description="The last update of the person")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str, datetime: str}
```


### 2.3 Filter model
Create another model, for correct capture nested fields py query string:
Example: ```https://example.com/api/v1/persons?name=John&age=42```

```python
class PersonFilterModel(BaseModel):
    name: Optional[str] = Field(description="The name of the person", min_length=1, max_length=255)
    age: Optional[str] = Field(description="The age of the person", min_length=1, max_length=255)
    occupation: Optional[str] = Field(description="The occupation of the person", min_length=1, max_length=255)
    hobby: Optional[str] = Field(description="The hobby of the person")
    friend_name: Optional[str] = Field(description="The friends of the person")
    created_at: Optional[datetime] = Field(description="The creation date of the person")
    last_update: Optional[datetime] = Field(description="The last update of the person")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str, datetime: str}
```

### 2.4 Converter
Create a converter for the update model:
```python
def filter_to_nested_model(update_model: PersonFilterModel) -> PersonUpdateModel:
    if update_model.hobby:
        hobbies = [update_model.hobby]
    else:
        hobbies = []

    return PersonUpdateModel(
        name=update_model.name,
        age=update_model.age,
        occupation=update_model.occupation,
        hobbies=hobbies
    )  # type: ignore
```

### 3 Repository
Create a repository for the model, with a new file in the repository folder:
```python
from app.repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    def __init__(self):
        super().__init__('_person_collection')
```

### 4 Route
Create the route:
In router folder create a file called ```<model_name>_route.py```:

The imports examples:
```python
from app.storages.database_filter import format_to_database_filter
from fastapi import APIRouter, Depends, Body
from typing import List
from app.storages.database_storage import Database, get_db
from app.models.person_model import PersonModel, PersonUpdateModel, filter_to_nested_model, PersonFilterModel
from app.repositories.person_repository import PersonRepository
from app.routes import BasicRoutable
```

Change the variables below:
```python
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
```

Copy the code below to the file, to create a generic route:
```python
@router.get("/", response_description=f"List all {_SHOW_NAME}s", response_model=List[_UPDATE_MODEL])
async def list(filter: _FILTER = Depends(_FILTER), db: Database =Depends(get_db)):
    nested = filter_to_nested_model(filter)
    db_filter = format_to_database_filter(nested.dict())
    return await _ROUTER.get_all_by(db_filter, db)


@router.get("/{id}", response_description=f"Get by id {_SHOW_NAME}", response_model=_UPDATE_MODEL)
async def show_by_id(id: str, db: Database =Depends(get_db)):
    return await _ROUTER.get_by_id(id, db)


@router.post("/", response_description=f"Add new {_SHOW_NAME}", response_model=_UPDATE_MODEL)
async def create(model: _MODEL = Body(...), db: Database =Depends(get_db)):
    return await _ROUTER.post(model, db)


@router.delete("/{id}", response_description=f"Delete a {_SHOW_NAME}")
async def delete(id: str, db: Database =Depends(get_db)):
    return await _ROUTER.delete(id, db)


@router.patch("/{id}", response_description=f"Update a {_SHOW_NAME}", response_model=_UPDATE_MODEL)
async def update(id: str, model: _UPDATE_MODEL = Body(...), db: Database =Depends(get_db)):
    return await _ROUTER.patch(id, model, db)
```

## 5 Create the tests
In tests folder create a file called ```test_<model_name>.py```:
```python
def test_read_person(client, id):
    response = client.get(f'{_BASE_PATH}')
    assert response.status_code == 200
    assert response.json() != valid_json
```


## Documentation of libraries
To see the documentation, visit:
* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [Motor](https://motor.readthedocs.io/)
