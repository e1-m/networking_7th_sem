from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')

    KEY_POOL_SIZE: int = 10

    REDIS_HOST: str
    REDIS_PORT: int


settings = Settings()
