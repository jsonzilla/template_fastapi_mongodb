from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from app.codecs import ObjectIdCodec
from app.models.examples.person_example import example, example_update


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


def filter_to_nested_model(update_model: PersonFilterModel) -> PersonUpdateModel:
    if update_model.hobby:
        hobbies = [update_model.hobby]
    else:
        hobbies = []

    return PersonUpdateModel(
        name=update_model.name,
        age=update_model.age,
        occupation=update_model.occupation,
        hobbies=hobbies,
        friends=[],
    )
