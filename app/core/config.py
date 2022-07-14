from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="TemplateFastAPIMongoDb", description="The name of the project")
    PROJECT_VERSION: str = Field(env="PROJECT_VERSION", default="0.0.1", description="The version of the project")
    PROJECT_DESCRIPTION: str = Field(env="PROJECT_DESCRIPTION", default="Template for FastAPI with MongoDB")

    MONGO_URL: str = Field(env="MONGO_URL", default="mongodb://localhost:27017/", description="The url of the MongoDB")
    DEFAULT_DATABASE: str = Field(env="DEFAULT_DATABASE", default="your_database", description="Default database name")

    class Config:
        validate_assignment = True
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
