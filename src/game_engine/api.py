import logging
from typing import List, Tuple

import json
from game_engine.game_rules_infrastructure import (
    DataBaseConfig,
    DictGameRules,
    GameRulesInterface,
    JsonConnectionEngine,
    PointGameRules,
    TypeUndefind,
)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Api:
    """
    Класс контроллер обработки данных из
    разных источников на примере игровых правил
    -------------------------------------------
    settings = JsonConfig()
    api = Api()
    api.settings = settings
    api.settings
    """

    def __init__(self) -> None:
        self._game_rules = GameRulesInterface()
        self._settings: DataBaseConfig | None = None

    @property
    def settings(self) -> DataBaseConfig:
        """возвращаем настройки"""

        if isinstance(self._settings, DataBaseConfig):
            return self._settings

        else:
            logger.info("self._settings is None")
            raise TypeUndefind("self._settings is None")

    @settings.setter
    def settings(self, values: DataBaseConfig):
        """передаем новые настройки"""

        if isinstance(values, DataBaseConfig):
            self._settings = values
        logger.info(f"{self._settings} записаны")

    @property
    def rules(self) -> GameRulesInterface:
        """метод для публикации всех данных"""
        if isinstance(self._settings, DataBaseConfig):
            match self.settings.db_type:
                case "not config":
                    logger.info("Игровые правила готовы")
                    return self._game_rules

                case "json":
                    self.settings.db_host = "r"

                    with JsonConnectionEngine(settings=self.settings) as conn:
                        if conn is not None:
                            self._game_rules.game_rules = json.load(conn)

                    logger.info("Игровые правила готовы в api")
                    return self._game_rules

                case _:
                    logger.warning(
                        "Упала при попытке вывести правила. Неизвестный тип переданный json get в api"
                    )
                    raise TypeUndefind("Неизвестный тип")
        else:
            raise TypeError("Тип settings None")

    @rules.setter
    def rules(self, values: List[DictGameRules]):
        """метод дабавить правило"""

        if isinstance(values, List):
            match self.settings.db_type:
                case "not config":
                    self._game_rules.game_rules = values
                    logger.info("Игровые правила записаны из not config в api")

                case "json":
                    self.settings.db_host = "w"

                    with JsonConnectionEngine(settings=self.settings) as conn:
                        if self._game_rules.game_rules != values:
                            self._game_rules.game_rules = values

                        json.dump(
                            [item.model_dump() for item in self._game_rules.game_rules],
                            sort_keys=True,
                            fp=conn,
                        )
                    logger.info("Игровые правила записаны из json в api")

                case _:
                    logger.warning(
                        "Ошибка падает при попытке добавить данные. json set Ошибка сериализации"
                    )
                    raise TypeUndefind("Неизвестный тип")

    def get_by_idx(self, idx: int) -> DictGameRules:
        """возврат правил по индексу"""

        try:
            logger.warning("успешно исполнен  Api.get_by_idx")
            return self._game_rules.game_rules[idx]

        except IndexError:
            raise IndexError(f"{idx} не существует в правилах")

    def set_by_idx(self, idx: int, value: DictGameRules):
        """вставка правил по индексу"""

        try:
            if isinstance(value, DictGameRules):
                try:
                    if self._game_rules.game_rules[idx] != value:
                        logger.warning(f"успешно записан {value} в Api.get_by_idx")
                        self._game_rules.game_rules[idx] = value

                except IndexError:
                    logger.warning(
                        IndexError(
                            f"{idx} не существует в последовательности. Добавляем объект в список"
                        )
                    )
                    self._game_rules._game_rules.append(value)

        except TypeError:
            logger.warning(f"Неизвестный тип {value}")
            raise TypeError("Неизвестный тип value")

    def get_subpoint_by_idx(self, indexes: Tuple[int, int]) -> PointGameRules:
        """метод отвечающий за отображение данных из списка подпунктов"""

        idx, subidx = indexes
        return self._game_rules.game_rules[idx].sub_point_list[subidx]

    def set_subpoint_by_idx(self, indexes: Tuple[int, int], value: PointGameRules):
        """метод записи данных в список подправил"""

        idx, subidx = indexes
        self._game_rules.game_rules[idx].sub_point_list[subidx] = value
