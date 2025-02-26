from typing import List

import json
from game_engine.game_rules_interface import (
    DataBaseConfig,
    DictGameRules,
    GameRulesInterface,
    JsonConnectionEngine,
    TypeUndefind,
)


class Api:
    """
    Класс контроллер обработки данных из разных источников на примере игровых правил
    ---------------------------------------
    settings = JsonConfig()
    api = Api()
    api.settings = settings
    api.settings
    """

    @property
    def settings(self):
        """возвращаем настройки"""

        return self._settings

    @settings.setter
    def settings(self, values: DataBaseConfig):
        """передаем новые настройки"""

        self._settings = values

    def get_rules(self) -> GameRulesInterface:
        """метод для публикации всех данных"""

        self.game_rules = GameRulesInterface()

        match self._settings.db_type:
            case "not config":
                return self.game_rules

            case "json":
                self._settings.db_host = "r+"

                with JsonConnectionEngine(settings=self._settings) as conn:
                    if conn is not None:
                        self.game_rules.game_rules = json.load(conn)

                return self.game_rules

            case _:
                raise TypeUndefind("Неизвестный тип")

    def set_rules(self, values: List[DictGameRules]):
        """метод дабавить правило"""

        self.game_rules = GameRulesInterface()
        self._settings.db_host = "w"

        match self._settings.db_type:
            case "not config":
                self.game_rules.game_rules = values

            case "json":
                self._settings.db_host = "w"

                with JsonConnectionEngine(settings=self._settings) as conn:
                    if self.game_rules.game_rules != values:
                        self.game_rules.game_rules = values

                    json.dump(
                        [item.model_dump() for item in self.game_rules.game_rules],
                        sort_keys=True,
                        fp=conn,
                    )

            case _:
                print("Неизвестный тип")
