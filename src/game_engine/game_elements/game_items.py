"""
Предметы в игре
---------------
Структура предметов
Категории предметов
Типы предметов
Опции предмета - могут меняться. И числовые и текстовые
Параметры предмета - привязаны на постоянной основе, числовые
Интерфейс доступа к предмету
"""

from typing import Generic, List, Annotated, Tuple, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T", bound=BaseModel)


class GameItemClass(BaseModel):
    """Класс предметов игры"""

    class_item_id: Annotated[
        int, Field(default=0, description="Идентификатор класса предмета")
    ]
    class_item_title: Annotated[str, Field(..., description="Название класса предмета")]
    class_item_description: Annotated[
        str, Field(..., description="Описание класса предмета")
    ]


class GameItemType(BaseModel):
    """Тип предметов игры"""

    type_item_id: Annotated[
        int, Field(default=0, description="Идентификатор типа предмета")
    ]
    type_item_title: Annotated[str, Field(..., description="Название типа предмета")]
    type_item_description: Annotated[
        str, Field(..., description="Описание типа предмета")
    ]


class GameItemOption(BaseModel):
    """Опции предмета игры"""

    item_option_id: Annotated[
        int, Field(default=0, description="Идентификатор опции предмета")
    ]
    item_option_title: Annotated[str, Field(..., description="Название опции")]
    item_option_description: Annotated[str, Field(..., description="Описание опции")]
    range_of_numeric_values: Annotated[
        Tuple[int, int], Field(..., description="Числовой диапазон от min до max")
    ]


class GameItemParametr(BaseModel):
    """Параметры предмета игры"""

    item_id: Annotated[
        int,
        Field(
            default=0,
            description="ID предмета в параметрах связано с самим предметом",
        ),
    ]
    power: Annotated[int, Field(default=0, description="Параметр силы на предмете")]
    distance: Annotated[int, Field(default=0, description="Параметр дистанции")]
    over_damage: Annotated[
        int, Field(default=0, description="Параметр растояния действия")
    ]
    mass_damage: Annotated[
        int,
        Field(
            default=0,
            description="Параметр максимальное количество целей для нанесения урона",
        ),
    ]


class GameItem(BaseModel):
    """Класс предмета игры"""

    item_id: Annotated[int, Field(gt=0, description="id предмета")]
    item_title: Annotated[str, Field(max_length=300, description="название предмета")]
    item_class: Annotated[GameItemClass, Field(..., description="класс предмета")]
    item_type: Annotated[GameItemType, Field(..., description="тип предмета")]
    item_parametrs: Annotated[
        GameItemParametr, Field(..., description="Список параметров предмета")
    ]
    item_options: Annotated[
        List[GameItemOption],
        Field(
            default_factory=List[GameItemOption], description="Список опций предмета"
        ),
    ]
    item_description: Annotated[str, Field(..., description="описание предмета")]


class GameItemInterface(Generic[T]):
    """Интерфейс доступа к предметам"""

    def __init__(self) -> None:
        self._item = None

    @property
    def item(self) -> T:
        """Возвращаем предмет"""

        if self._item is None:
            raise TypeError("Item is None")

        return self._item

    @item.setter
    def item(self, value: T):
        """Записывает предмет"""

        if isinstance(value, BaseModel):
            self._item = value
