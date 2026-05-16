from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    APP_NAME: str = "CareInCode+"

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = (
        "models/gemini-2.5-flash"
    )

    MONGO_URI: str = (
        "MONGO_URI = mongodb+srv://jadhavdarshan259_db_user:Px1EsTz926RYefOe@cluster0.u039uiu.mongodb.net/?appName=Cluster0"
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