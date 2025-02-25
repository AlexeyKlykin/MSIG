"""
Правила игры формируются в виде пронумерованых списков
структура состоит из номера, названия и описания
Интерфейс позволяет добавлять правила
Интрефейс подключения

    rule_one = PointGameRules(id=1, title="Правило", description="Описание правила 1")
    rule_two = PointGameRules(id=2, title="Правило", description="Описание правила 2")
    rule_thri = PointGameRules(id=3, title="Правило", description="Описание правила 3")

    sub_point_list: List[PointGameRules] = [
        rule_one,
        rule_two,
        rule_thri,
    ]

    struct_rule = DictGameRules(
        id=1,
        title="Правило 1",
        description="Описание правила 1",
        sub_point_list=sub_point_list,
    )

    write_data = [
        struct_rule,
    ]

    config = NotConfig(db_type="", db_name="")
    gri = GameRulesInterface(config)
    gri.game_rules = write_data

    yield gri.game_rules

   output  = [
       {
           'description': 'Описание правила 1',
           'id': 1,
           'sub_point_list': [
               {
                   'description': 'Описание правила 1',
                   'id': 1,
                   'title': '1.1. Правило',
               },
               {
                   'description': 'Описание правила 2',
                   'id': 2,
                   'title': '1.2. Правило',
               },
               {
                   'description': 'Описание правила 3',
                   'id': 3,
                   'title': '1.3. Правило',
               },
           ],
           'title': '1. Правило 1',
       },
   ]
"""

import logging
import sqlite3
from psycopg import connect
from psycopg.conninfo import make_conninfo
from typing import IO, Any, Dict, List
from psycopg.rows import tuple_row
from pydantic import BaseModel, Field, model_validator
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


class DataBaseConfig(BaseSettings):
    db_type: str = Field(alias="db_type", description="Тип базы данных")
    db_host: str = Field(
        default="localhost", alias="db_host", description="Хост базы данных"
    )
    db_port: int = Field(
        default=4040,
        alias="db_port",
        description="Порт базы данных",
    )
    db_username: str = Field(
        default="neon185a",
        alias="db_username",
        description="Имя пользователя для подключения к базе данных",
    )
    db_password: str = Field(
        default_factory=lambda: generate_password(),
        alias="db_password",
        description="Пароль для подключения к базе данных",
    )

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


class PostgresConfig(DataBaseConfig):
    db_type: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_username: str = "myuser"
    db_password: str = "mypassword"
    db_name: str = "mydb"


class JsonConfig(DataBaseConfig):
    db_type: str = "json"
    db_name: str = "game_rules.json"
    db_host: str = "w+"


class PointGameRules(BaseModel):
    """Класс структуры подзаголовочного правила"""

    id: Annotated[int, Field(gt=0, description="Номер для пункта правил")]
    title: Annotated[str, Field(max_length=300, description="Название пункта правила")]
    description: str


class DictGameRules(PointGameRules):
    """Класс структуры заголовочных пунктов правил"""

    sub_point_list: Annotated[
        List[PointGameRules],
        Field(default=[], description="Список правил под заголовком"),
    ]

    @model_validator(mode="after")
    def check_title(self):
        """преобразуем подпункты правил
        если список подпарвил не пустой"""

        self.title = f"{self.id}. {self.title}"
        if self.sub_point_list is not None:
            for spl in self.sub_point_list:
                spl.title = f"{self.id}.{spl.id}. {spl.title}"
        return self


class ConnectionProtocol:
    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            pass


class JsonConnectionEngine(ConnectionProtocol):
    """Менеджер для управления соединения
    игровых правил с хранилищем"""

    def __init__(self, settings: DataBaseConfig = JsonConfig()) -> None:
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


class TypeUndefind(Exception): ...


class GameRulesInterface:
    """Интерфейс взаимодействия с json"""

    def __init__(self, config: DataBaseConfig) -> None:
        self._game_rules = []
        self._config = config

    @property
    def game_rules(self) -> List[DictGameRules]:
        """вернуть все данные"""

        return self._game_rules

    @game_rules.setter
    def game_rules(self, values: List):
        """вставить данные"""

        self._game_rules = values
