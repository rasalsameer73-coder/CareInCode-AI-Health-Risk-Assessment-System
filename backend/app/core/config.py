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

    MONGO_URI: str = (
        "mongodb+srv://jadhavdarshan259_db_user:Px1EsTz926RYefOe@cluster0.u039uiu.mongodb.net/?appName=Cluster0"
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