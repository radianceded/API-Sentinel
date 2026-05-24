from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str="API Sentinel"
    app_env: str="development"
    #密钥
    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    #通行证有效期24h
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    debug: bool=True
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    
    )
settings = Settings()


