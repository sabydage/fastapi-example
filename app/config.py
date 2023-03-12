from pydantic import BaseSettings

class Settings(BaseSettings): 
    #provide list of all environment variables. It will perform automatic validation and that will make our life easier.
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
