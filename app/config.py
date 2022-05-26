from pydantic import BaseSettings


class Settings(BaseSettings):
    fasty_db_hostname: str;
    fasty_db_port: str;
    fasty_db_username: str;
    fasty_db_password: str;
    fasty_db_name: str;
    
    fasty_secret_key: str;
    fasty_algorithm: str;
    fasty_access_token_expire_minutes: int;

    class Config:
        env_file=".env";

settings = Settings();
    