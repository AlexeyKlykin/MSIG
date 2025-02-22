"""
Правила игры формируются в виде пронумерованых списков
структура состоит из номера, названия и описания
"""

from typing import List, Protocol
from pydantic import BaseModel, Field, Json
from typing_extensions import Annotated
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class PointGameRules(BaseModel):
    """Класс структуры под заголовочного правила"""

    id: Annotated[int, Field(gt=0, description="Номер для пункта правил")]
    title: Annotated[str, Field(max_length=300, description="Название пункта правила")]
    description: str


class StructGameRules(PointGameRules):
    """Класс структуры заголовочных пунктов правил"""

    sub_point_list: Annotated[
        List[PointGameRules] | None,
        Field(..., title="Список правил под заголовком", alias="subPointList"),
    ]


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


class GameRulesProtocol(Protocol):
    """Протокол интерфейса игровых правил"""

    def print_all_data(self): ...

    def select_data_by_key(self, key): ...

    def insert_data_by_key(self, key, value): ...

    def remove_data_by_key(self, key): ...


class GameRulesJson:
    """Интерфейс взаимодействия с json"""

    def __init__(self, game_rules: BaseModel) -> None:
        self._game_rules = game_rules

    def print_all_data(self): ...

    def select_data_by_key(self, key):
        """возврат данных по ключу"""

    def insert_data(self): ...

    def remove_data_by_key(self): ...

    def get_state(self): ...


class GameRulesPgInterface: ...


class GameRulesSqliteInterface: ...


if __name__ == "__main__":
    with open("game_rules.json", "w+") as js:
        print(type(js))
