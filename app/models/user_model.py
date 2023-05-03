from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, validator
from app.codecs import ObjectIdCodec
from app.models.examples.user_example import example, basic_request_example


class UserModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    username: str = Field(unique_items=None, min_length=3, max_length=50, description="The username of the user.")
    password: str = Field(description="The password of the user.", min_length=10, max_length=63)
    email: EmailStr = Field(unique_items=None, description="The email of the user.")
    last_update_datetime: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The date and time that this user was last updated.")

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": basic_request_example}
        extra = 'forbid'
        copy_on_model_validation = 'none'


class CreateUserModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    username: str = Field(unique_items=None, min_length=3, max_length=50, description="The username of the user.")
    password: str = Field(description="The password of the user.", min_length=10, max_length=63)
    email: EmailStr = Field(unique_items=None, description="The email of the user.")

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": basic_request_example}
        extra = 'forbid'
        copy_on_model_validation = 'none'


class ShowUserModel(BaseModel):
    id: ObjectIdCodec = Field(default_factory=ObjectIdCodec, alias="_id")
    username: str = Field(unique_items=None, min_length=3, max_length=50)
    email: EmailStr = Field(unique_items=None, description="The email of the user.")
    last_update_datetime: datetime = Field(default_factory=datetime.utcnow,
                                           description="The date and time that this user was last updated.")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
        extra = 'forbid'
        copy_on_model_validation = 'none'


class UpdateUserModel(BaseModel):
    password: Optional[str] = Field(description="The password of the user.", min_length=10, max_length=63)
    last_update_datetime: Optional[datetime] = Field(description="The date and time that this user was last updated.")

    class Config:
        json_encoders = {ObjectId: str, datetime: str}
        schema_extra = {"example": example}
        extra = 'forbid'
        copy_on_model_validation = 'none'
