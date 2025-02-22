"""
Правила игры формируются в виде пронумерованых списков
структура состоит из номера, названия и описания
"""

from typing import List
from pydantic import BaseModel, Field
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
