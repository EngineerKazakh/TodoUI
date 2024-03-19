from pydantic_settings import BaseSettings
import os
from typing import ClassVar
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    app_name: ClassVar[str] = 'Plannner Fast - Твой менеджер задач'
    # app_name=os.getenv('NAME_APP')
    db_url: str='sqlite:///.\\todo\\database\\DB\\todo.db'

    class Config:
        env_file: str='../.env'


settings=Settings()


