from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = "master"
    DB_USERNAME: str = "sa"
    DB_PASSWORD: str = "Olgakempinnen0609"
    DB_HOST: str = "localhost"


settings = Settings()
