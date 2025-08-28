from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_google : str
    model : str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"


settings=Settings()