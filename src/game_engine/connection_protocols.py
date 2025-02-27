import sqlite3
import logging
from typing import Protocol, IO
from psycopg import connect
from psycopg.conninfo import make_conninfo
from psycopg.rows import tuple_row

from game_engine.configs import DataBaseConfig


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
        logger.info("Соединение открыто")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.info("Соединение закрыто")
            pass


class JsonConnectionEngine(ConnectionProtocol):
    """Менеджер для управления соединения
    игровых правил с хранилищем"""

    def __init__(self, settings: DataBaseConfig) -> None:
        self._file_path = settings.db_name
        self._pref = settings.db_host

    def __enter__(self) -> IO:
        self._resource = open(self._file_path, self._pref)
        logger.info("json file is open")
        return self._resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._resource is not None:
            self._resource.close()
        logger.info("json file is close")


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
