"""
Правила игры формируются пронумерованым списком
структура состоит из названия и описания
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from pydantic import BaseModel, Field, computed_field, field_validator


class PointRules(BaseModel):
    point_number: int
    title: str

    @field_validator("point_number", mode="before")
    def validate_point_number(cls, val):
        if isinstance(val, int):
            return val

        elif isinstance(val, str):
            return int(val)

        elif isinstance(val, float):
            return int(val)

        else:
            raise ValueError("Передан неверный тип данных в point_number")

    @computed_field
    def computed_title(self) -> str:
        return f"{self.point_number} {self.title}"


class SubPointRules(BaseModel):
    sub_point_number: float
    title: str
    description: str

    @field_validator("sub_point_number", mode="before")
    def validate_sub_point_number(cls, val):
        if isinstance(val, int):
            return float(val)

        elif isinstance(val, str):
            return float(val)

        elif isinstance(val, float):
            return val

        else:
            raise ValueError("Передан неверный тип данных в sub_point_number")

    @computed_field
    def computed_title(self) -> str:
        return f"{self.sub_point_number} {self.title}"


class GameRulesStruct(BaseModel):
    header: PointRules = Field(title="Основной заголовок списка правил")
    rules_list: List[SubPointRules] = Field(title="Список правил")


class RulesInterface(ABC):
    @abstractmethod
    def set_rules(self, value):
        """метод для добавления правила"""

    @abstractmethod
    def get_rules(self) -> object:
        """метод для возврата правила"""


class PointRulesInterface(RulesInterface):
    """Интерфейс для заголовка списка правил"""

    def __init__(self) -> None:
        self._point_rules: PointRules | None = None

    def set_rules(self, value: Tuple[int, str]):
        point = value[0]
        title = value[1]
        self._point_rules = PointRules(point_number=point, title=title)

    def get_rules(self) -> PointRules | None:
        if self._point_rules is not None:
            return self._point_rules


class SubPointRulesInterface(RulesInterface):
    """Интерфейс для списка правил"""

    def __init__(self) -> None:
        self._sub_point_rules: SubPointRules | None = None

    def set_rules(self, value: Tuple[float, str, str]):
        sub_point = value[0]
        title = value[1]
        description = value[2]
        self._sub_point_rules = SubPointRules(
            sub_point_number=sub_point,
            title=title,
            description=description,
        )

    def get_rules(self) -> SubPointRules | None:
        if self._sub_point_rules is not None:
            return self._sub_point_rules


class GameRulesInterface(RulesInterface):
    """Интерфейс для управления правилами игры"""

    def __init__(self, point: PointRules) -> None:
        self._rules_list: List[SubPointRules] = []
        self._header: PointRules = point

    def set_rules(self, value: SubPointRules):
        self._rules_list.append(value)

    def get_rules(self) -> GameRulesStruct:
        return GameRulesStruct(header=self._header, rules_list=self._rules_list)
