import logging
from contextlib import asynccontextmanager
from typing import Protocol
from dotenv import load_dotenv, dotenv_values
from psycopg import AsyncConnection
from psycopg.errors import ConnectionException
from psycopg.pq import PGconn
from pydantic import BaseModel, Json

from game_engine.struct_game_rules import StructGameRules

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


config = dotenv_values(".env")
load_dotenv()


@asynccontextmanager
async def manager_pg():
    """менеджер для подключения к бд"""

    settings = {}
    pgconn = PGconn()
    conn = AsyncConnection(pgconn=pgconn).connect(**settings, autocommit=True)

    try:
        yield conn

    except ConnectionException as err:
        raise ConnectionException(f"{err}")

    finally:
        conn.close()


class GameRulesManagerProtocol(Protocol):
    """Класс протокол менеджера для управлением
    открытия соединения с хранилищем данных"""

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_val, exc_tb): ...

    def save_state(self, value): ...

    def get_state(self): ...


class GameRulesJsonManager:
    """Менеджер для управления соединения
    игровых правил с хранилищем"""

    def __init__(self, file_path: str, pref: str = "w+") -> None:
        self._file_path = file_path
        self._pref = pref
        self._resource = None

    def __enter__(self):
        self._resource = open(self._file_path, self._pref)
        return self._resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._resource is not None:
            self._resource.close()

    def save_state(self, value: Json):
        """сохраняем состояние в файле json"""

        if self._resource is not None:
            self._resource.write(value)

    def get_state(self) -> BaseModel | None:
        """возврат данных из json"""

        if isinstance(self._resource, dict):
            return StructGameRules(**self._resource.read())
        elif self._resource is not None:
            return StructGameRules(**dict(self._resource.read()))
        else:
            logger.warning(f"Не верный формат данных {self._resource}")
