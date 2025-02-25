"""
Правила игры формируются в виде пронумерованых списков
структура состоит из номера, названия и описания
Интерфейс позволяет добавлять правила
"""

import logging
import sqlite3
from psycopg import connect
from psycopg.conninfo import make_conninfo
from typing import IO, Any, Dict, List, Protocol
from psycopg.rows import tuple_row
from pydantic import (
    BaseModel,
    Field,
    Json,
    computed_field,
    field_validator,
    model_validator,
    validator,
)
from pydantic_core import to_json
from pydantic_settings import BaseSettings
from typing_extensions import Annotated
import secrets
import string


def generate_password(length: int = 12) -> str:
    """Генерирует случайный пароль заданной длины."""

    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class ConnectionProtocol(Protocol):
    """Протокол для менеджера"""

    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            pass


class SqliteConnectionEngine(ConnectionProtocol):
    """Контекстный менеджер для
    подключения к базе данных sqlite3"""

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self) -> sqlite3.Connection:
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn

        except sqlite3.Error as err:
            logger.warning(f"{err} потеряно соединение")
            raise sqlite3.Error(err, "Потеряно соединение")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class PointGameRules(BaseModel):
    """
    Класс структуры подзаголовочного правила
    ---------------------------------------
    id generated always as identity int
    title Правило 1
    description Описание правила 1
    """

    id: Annotated[int, Field(gt=0, description="Номер для пункта правил")]
    title: Annotated[str, Field(max_length=300, description="Название пункта правила")]
    description: str


class DictGameRules(PointGameRules):
    """
    Класс структуры заголовочных пунктов правил
    id generated always as identity int
    title Правило 1
    description Описание правила 1
    list[PointGameRules, ]  Список подпунктов для правила
    """

    sub_point_list: Annotated[
        List[PointGameRules],
        Field(default=[], description="Список правил под заголовком"),
    ]

    @model_validator(mode="after")
    def check_title(self):
        """
        преобразуем подпункты правил если список подпарвил не пустой
        --------------------------------
        нумерация под правил на основании id родительского правила
        """

        self.title = f"{self.id}. {self.title}"
        if self.sub_point_list is not None:
            for spl in self.sub_point_list:
                spl.title = f"{self.id}.{spl.id}. {spl.title}"
        return self


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


class JsonConnectionEngine(ConnectionProtocol):
    """Менеджер для управления соединения
    игровых правил с хранилищем"""

    def __init__(self, settings: DataBaseConfig) -> None:
        self._file_path = settings.db_name
        self._pref = settings.db_host

    def __enter__(self) -> IO:
        self._resource = open(self._file_path, self._pref)
        return self._resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._resource is not None:
            self._resource.close()


class PgConnectionEngine(ConnectionProtocol):
    """Контекстный менеджер для
    подключения к postgres"""

    def __init__(self, settings: DataBaseConfig):
        self._settings = settings

    def __enter__(self):
        self.connect = connect(
            make_conninfo("", **self._settings.model_dump()), row_factory=tuple_row
        )
        return self.connect

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connect is not None:
            self.connect.close()


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
    db_name: str = "game_rules.json"
    db_host: str = "w+"
    db_port: int = 1
    db_username: str = "neon"
    db_name: str = "msig"
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


class TypeUndefind(Exception): ...


class GameRulesInterface:
    """Интерфейс взаимодействия с json"""

    def __init__(self, config: DataBaseConfig) -> None:
        self._game_rules = []
        self._config = config

    @property
    def game_rules(self) -> List[DictGameRules | PointGameRules]:
        """вернуть все данные"""

        return self._game_rules

    @game_rules.setter
    def game_rules(self, values: List[DictGameRules | PointGameRules]):
        """вставить данные"""

        self._game_rules = values

    @property
    def config(self) -> Dict:
        """вывести конфиг"""

        return self._config.model_dump()

    @config.setter
    def config(self, config: DataBaseConfig):
        """записать конфиг"""

        self._config = config
