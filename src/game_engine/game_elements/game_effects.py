from typing import Annotated, List, Tuple
from pydantic import Field, BaseModel


class GameEffectMixin(BaseModel):
    """Примесь для эффектов модели"""

    id: Annotated[int, Field(default=0, description="Идентификатор эффекта")]
    title: Annotated[str, Field(..., description="Название эффекта")]
    description: Annotated[str, Field(..., description="Описание эффекта")]


class GameEffectType(GameEffectMixin):
    """Модель типа эффектов"""


class GameEffectClass(GameEffectMixin):
    """Модель класса эффектов"""


class GameEffectOption(GameEffectMixin):
    """Опции игровых эффектов"""

    range_of_numeric_values: Annotated[
        Tuple[int, int], Field(..., description="Числовой диапазон от min до max")
    ]


class GameEffectParametr(BaseModel):
    """Модель парметров эффектов"""

    effect_id: Annotated[
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


class GameEffect(GameEffectMixin):
    """Основная модель эффекта"""

    effect_type: Annotated[
        GameEffectType, Field(..., description="Тип игровых эффектов")
    ]
    effect_class: Annotated[
        GameEffectClass, Field(..., description="Класс игровых эффектов")
    ]
    effect_parametrs: Annotated[
        List[GameEffectParametr], Field(..., description="Параметры игровых эффектов")
    ]
