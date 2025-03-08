"""
Как только будут новые протоколы доступа к базе данных
нужно их обработать в api
"""

import logging
from typing import Generic, List, Tuple, TypeVar
import json

from pydantic import BaseModel

from game_engine.configs import DataBaseConfig, NotConfig
from game_engine.connection_protocols import JsonConnectionEngine
from game_engine.game_rules_infrastructure import (
    GameRulesInterface,
    PointGameRules,
    SubPointGameRules,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class UndefindTypeError(Exception):
    """Ошибка неверного типа структуры предмета"""

    def __init__(self, item_type: str, item) -> None:
        super().__init__(item_type)
        self.item_type = item_type
        self.item = item

    def __str__(self) -> str:
        return f"{self.item_type} ошибка структуры типа {self.item}"


class GameRulesController:
    """
    Класс контроллер обработки данных из
    разных источников на примере игровых правил
    -------------------------------------------
    settings = JsonConfig()
    controller = GameRulesController()
    settings = settings
    settings # Pydantic class()
    rules # call rules
    rules = rules # set rules
    get_by_idx
    set_by_idx
    delete_by_idx
    get_subpoint_by_idx
    set_subpoint_by_idx
    delete_subpoint_by_idx
    """

    def __init__(self) -> None:
        self._game_rules = GameRulesInterface()
        self._settings: DataBaseConfig = NotConfig()

    @staticmethod
    def game_rules_sorted(collect: List[PointGameRules]) -> List[PointGameRules]:
        """метод сортировки списка правил по id"""

        sort_lst = collect.sort(key=lambda x: x.id)

        if sort_lst is None:
            raise UndefindTypeError(
                item="После сортировки возвращается None", item_type="None"
            )

        return sort_lst

    @property
    def settings(self) -> DataBaseConfig:
        """возвращаем настройки"""

        if isinstance(self._settings, DataBaseConfig):
            return self._settings

        else:
            raise TypeError(
                "self._settings is None. Нужно задать настройки перед вызовом правил"
            )

    @settings.setter
    def settings(self, values: DataBaseConfig):
        """передаем новые настройки"""

        if isinstance(values, DataBaseConfig):
            logger.info(f"{self._settings} записаны")
            self._settings = values

    @property
    def rules(self) -> GameRulesInterface:
        """метод для загрузки правил из баз данных"""

        if isinstance(self._settings, DataBaseConfig):
            match self.settings.db_type:
                case "not config":
                    logger.info("NotConfig. Игровые правила готовы")
                    return self._game_rules

                case "json":
                    self.settings.db_host = "r"

                    with JsonConnectionEngine(settings=self.settings) as conn:
                        if conn is not None:
                            self._game_rules.game_rules = json.load(conn)

                    logger.info("Игровые правила готовы в controller через json")
                    return self._game_rules

                case _:
                    raise TypeError(
                        """Упала при попытке вывести правила. 
                        Неизвестный тип переданный json get в controller"""
                    )
        else:
            raise TypeError("Тип settings None")

    @rules.setter
    def rules(self, values: List[PointGameRules]):
        """метод дабавить правило"""

        if isinstance(values, List):
            match self.settings.db_type:
                case "not config":
                    self._game_rules.game_rules = values
                    logger.info("Игровые правила записаны из not config в controller")

                case "json":
                    self.settings.db_host = "w"

                    with JsonConnectionEngine(settings=self.settings) as conn:
                        if self._game_rules.game_rules != values:
                            self._game_rules.game_rules = values

                        json.dump(
                            [item.model_dump() for item in self._game_rules],
                            sort_keys=True,
                            fp=conn,
                        )
                    logger.info("Игровые правила записаны из json в controller")

                case _:
                    raise TypeError(
                        """Ошибка падает при попытке добавить данные. 
                        json set Ошибка сериализации"""
                    )

    def get_by_idx(self, idx: int) -> PointGameRules:
        """возврат правил по индексу"""

        try:
            logger.info("успешно исполнен  controller.get_by_idx")
            return self._game_rules.game_rules[idx]

        except IndexError:
            raise IndexError(
                f"Элемента с таким индексом = {idx} не существует в правилах"
            )

    def set_by_idx(self, idx: int, value: PointGameRules):
        """вставка правил по индексу"""

        try:
            if isinstance(value, PointGameRules):
                if self._game_rules.game_rules[idx] != value:
                    logger.warning(f"успешно записан {value} в Controller.get_by_idx")
                    self._game_rules.game_rules[idx] = value

        except IndexError:
            logger.warning(
                IndexError(
                    f"{idx} не существует в последовательности. Добавляем объект в список"
                )
            )
            self._game_rules._game_rules.append(value)

        except TypeError:
            raise TypeError(f"Неизвестный тип {value}")

    def delete_by_idx(self, idx: int):
        """метод для удаления правила по индексу"""

        try:
            del_el = self._game_rules.game_rules.pop(idx)
            logger.info(f"выполнено удаление {del_el}")

        except IndexError:
            raise IndexError(f"Ошибка. {idx} недопустимый индекс элемента")

    def get_subpoint_by_idx(self, indexes: Tuple[int, int]) -> SubPointGameRules:
        """метод отвечающий за отображение данных из списка подпунктов"""

        idx, subidx = indexes

        try:
            logger.info(f"получено правило по индексам {indexes}")
            return self._game_rules[idx].sub_point_list[subidx]

        except IndexError as err:
            raise IndexError(f"Ошибка индекса {err}")

    def set_subpoint_by_idx(self, indexes: Tuple[int, int], value: SubPointGameRules):
        """метод записи данных в список подправил"""

        idx, subidx = indexes

        try:
            if isinstance(value, SubPointGameRules):
                self._game_rules[idx].sub_point_list[subidx] = value

        except IndexError:
            logger.warning(f"Ошибка объявления элемента {value} по индексам {indexes}")
            self._game_rules[idx].sub_point_list.append(value)

        except TypeError:
            logger.warning(f"Неизвестный тип {value}")
            raise TypeError("Неизвестный тип value")

    def delete_subpoint_by_idx(self, indexes: Tuple[int, int]):
        """метод удаления подправила по индексу"""

        idx, subidx = indexes

        try:
            del_el = self._game_rules[idx].sub_point_list.pop(subidx)
            logger.info(f"выполнено удаление {del_el}")

        except IndexError:
            raise IndexError(
                f"Ошибка. {indexes} недопустимый индекс правила или подправила"
            )


T = TypeVar("T", bound="BaseModel")


class Descriptor(Generic[T]):
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> T:
        if isinstance(instance.__dict__[self._name], BaseModel):
            return instance.__dict__[self._name]
        else:
            raise UndefindTypeError(item_type="BaseModel", item=self._name)

    def __set__(self, instance, value: T):
        if isinstance(value, BaseModel):
            instance.__dict__[self._name] = value


class GameItemController:
    """
    Класс для публичного доступа к интерфейсу структуры предметов
    -------------------------------------------------------------
    """

    item_class = Descriptor()
    item_type = Descriptor()
    item_option = Descriptor()
    item_parametr = Descriptor()
    game_item = Descriptor()


class GameEffectController:
    """
    Класс для публичного доступа к интерфейсу структуры эффектов
    -------------------------------------------------------------
    """

    effect_class = Descriptor()
    effect_type = Descriptor()
    effect_option = Descriptor()
    effect_parametr = Descriptor()
    game_effect = Descriptor()
