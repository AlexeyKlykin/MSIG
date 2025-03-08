"""
Правила игры формируются в виде пронумерованых списков
структура состоит из номера, названия и описания
Интерфейс позволяет добавлять правила и возвращать
"""

import logging
from typing import List, Annotated
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class PointGameRulesMixin(BaseModel):
    """Примесь для структуры игровых правил"""

    id: Annotated[int, Field(gt=0, description="Номер для пункта правил")]
    title: Annotated[str, Field(max_length=300, description="Название пункта правила")]
    description: str


class SubPointGameRules(PointGameRulesMixin):
    """
    Класс структуры подзаголовочного правила
    ---------------------------------------
    id generated always as identity int
    title Правило 1
    description Описание правила 1
    """

    point_game_rules_id: Annotated[
        int, Field(gt=0, description="Связь с родительским пунктом")
    ]


class PointGameRules(PointGameRulesMixin):
    """
    Класс структуры заголовочных пунктов правил
    -------------------------------------------
    id generated always as identity int
    title Правило 1
    description Описание правила 1
    list[PointGameRules, ]  Список подпунктов для правила
    """

    sub_point_list: Annotated[
        List[SubPointGameRules],
        Field(
            default_factory=List[SubPointGameRules],
            description="Список правил под заголовком",
        ),
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


class GameRulesInterface:
    """Интерфейс взаимодействия с json"""

    def __init__(self) -> None:
        self._game_rules: List[PointGameRules] = []
        self.idx: int = 0

    def __iter__(self):
        return self

    def __next__(self) -> PointGameRules:
        if self.idx < len(self._game_rules):
            res = self._game_rules[self.idx]
            self.idx += 1
            return res
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> PointGameRules:
        if 0 < len(self._game_rules) and index >= 0:
            return self._game_rules[index]
        else:
            raise IndexError("Индекс выходит за пределы допустимого значения")

    def __setitem__(self, key: int, value: PointGameRules):
        if isinstance(key, int) or key >= 0:
            self._game_rules[key] = value

    def __delitem__(self, key: int):
        if isinstance(key, int):
            del self._game_rules[key]

    @property
    def game_rules(self) -> List[PointGameRules]:
        """вернуть все данные"""

        logger.info("возврат правил")
        return self._game_rules

    @game_rules.setter
    def game_rules(self, values: List[PointGameRules]):
        """вставить данные"""

        if isinstance(values, List):
            self._game_rules = values
        logger.info(f"{values} записан в правила")
