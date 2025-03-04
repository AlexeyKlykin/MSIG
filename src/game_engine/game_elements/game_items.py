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

from typing import List, Annotated, Tuple
from pydantic import BaseModel, Field


class GameItemMixin(BaseModel):
    """Миксин для id, title, description"""

    id: Annotated[int, Field(default=0, description="Идентификатор")]
    title: Annotated[str, Field(..., description="Название")]
    description: Annotated[str, Field(..., description="Описание")]


class GameItemClass(GameItemMixin):
    """Класс предметов игры"""


class GameItemType(GameItemMixin):
    """Тип предметов игры"""


class GameItemOption(GameItemMixin):
    """Опции предмета игры"""

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


class GameItem(GameItemMixin):
    """Класс предмета игры"""

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
