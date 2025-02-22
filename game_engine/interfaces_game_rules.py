from typing import Protocol

from pydantic import BaseModel


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
