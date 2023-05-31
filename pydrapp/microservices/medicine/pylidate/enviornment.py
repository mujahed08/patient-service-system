from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    mysql_database:str = Field(..., env='MYSQL_DATABASE')
    mysql_user:str = Field(..., env='MYSQL_USER')
    mysql_password:str = Field(..., env='MYSQL_PASSWORD')
    mysql_root_password:str = Field(..., env='MYSQL_ROOT_PASSWORD')
    mysql_host:str = Field(..., env='MYSQL_HOST')
    run_env:str = Field(..., env='RUN_ENV')


    class Config:
        env_file = None
        env_file_encoding = 'utf-8'
