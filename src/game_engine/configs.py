import secrets
import string
from typing import Any, Dict, Annotated
from pydantic import Field
from pydantic_settings import BaseSettings


def generate_password(length: int = 12) -> str:
    """Генерирует случайный пароль заданной длины."""

    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


class DataBaseConfig(BaseSettings):
    """Класс структуры для настроек подключения к базам данных"""

    db_type: Annotated[str, Field(alias="db_type", description="Тип базы данных")]
    db_host: Annotated[
        str, Field(default="localhost", alias="db_host", description="Хост базы данных")
    ]
    db_port: Annotated[
        int,
        Field(
            default=4040,
            alias="db_port",
            description="Порт базы данных",
        ),
    ]
    db_username: Annotated[
        str,
        Field(
            alias="db_username",
            description="Имя пользователя для подключения к базе данных",
        ),
    ]
    db_password: Annotated[
        str,
        Field(
            default_factory=lambda: generate_password(),
            alias="db_password",
            description="Пароль для подключения к базе данных",
        ),
    ]

    db_name: Annotated[str, Field(alias="db_name", description="Название базы данных")]

    def get_db_config(self) -> Dict[str, Any]:
        return {
            "type": self.db_type,
            "host": self.db_host,
            "port": self.db_port,
            "user": self.db_username,
            "name": self.db_name,
            "password": self.db_password,
        }


class NotConfig(DataBaseConfig):
    """Класс конфигурации по умолчанию без сохранения"""

    db_type: str = "not config"
    db_host: str = "local"
    db_port: int = 1
    db_username: str = "neon"
    db_name: str = "msig"
    db_password: str = "vbnzq"


class JsonConfig(DataBaseConfig):
    """
    Тестовые настройки
    Вы можете построить свою структуру исходя из примера
    """

    db_type: str = "json"
    db_host: str = "w+"
    db_port: int = 1
    db_username: str = "neon"
    db_name: str = "game_rules.json"
    db_password: str = "vbnzq"


class PostgresConfig(DataBaseConfig):
    """
    Тестовые настройки
    Вы можете заполнить на свой вкус
    """

    db_type: str = Field(default="postgresql", alias="type_db")
    db_host: str = Field(default="localhost", alias="host db")
    db_port: int = Field(default=5432, alias="port")
    db_username: str = Field(default="myuser")
    db_password: str = Field(default="mypassword")
    db_name: str = Field(default="mydb")
