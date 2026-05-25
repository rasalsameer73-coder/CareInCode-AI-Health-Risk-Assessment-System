from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from pymongo import MongoClient


class Settings(BaseSettings):

    APP_NAME: str = "CareInCode+"

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = (
        "models/gemini-2.5-flash"
    )

    MONGO_URI: str = Field(
        default="mongodb://localhost:27017",
        env=("MONGO_URI", "MONGODB_URI")
    )
    
    DATABASE_NAME: str = (
        "careincode"
    )

    JWT_SECRET: str = (
        "careincode_jwt_secret"
    )

    ENCRYPTION_KEY: str = (
        "careincode_secure_key_32"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

client = MongoClient(settings.MONGO_URI)

try:
    client.admin.command('ping')
    print("MongoDB Connected Successfully")
except Exception as e:
    print("MongoDB Connection Failed:", e)