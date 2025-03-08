from pytest import mark, fixture

from game_engine.controllers import GameEffectController
from game_engine.game_elements.game_effects import (
    GameEffect,
    GameEffectClass,
    GameEffectOption,
    GameEffectParametr,
    GameEffectType,
)


@fixture(scope="class")
def setup_effect_struct():
    """предустоновка структуры эффектов для теста"""

    effect_type = GameEffectType(
        **{"id": 1, "title": "Временные", "description": "Истекает со временем"}
    )
    effect_class = GameEffectClass(
        **{"id": 1, "title": "Вода", "description": "Водный тип"}
    )
    effect_option = GameEffectOption(
        **{
            "id": 1,
            "title": "Временная",
            "description": "Временная опция объявляет работу со временем",
            "range_of_numeric_values": [1, 10],
        }
    )
    effect_parametr = GameEffectParametr(
        **{
            "id": 1,
            "power": 2,
            "distance": 0,
            "over_damage": 0,
            "mass_damage": 0,
        }
    )
    effect = GameEffect(
        **{
            "id": 1,
            "title": "Поджог",
            "description": "Остовляет на цели ожог который остается не продолжительное время",
            "effect_type": effect_type,
            "effect_class": effect_class,
            "effect_options": effect_option,
            "effect_parametrs": [
                effect_parametr,
            ],
        }
    )

    controler = GameEffectController()
    controler.game_effect = effect

    yield controler


@mark.effect_game()
class TestEffectStructGame:
    """Тест структуры эффектов игры"""

    def test_game_effect(self, setup_effect_struct):
        """тест: сборки структуры эффекта"""

        assert setup_effect_struct.game_effect.model_dump() == {
            "description": "Остовляет на цели ожог который остается не продолжительное "
            "время",
            "effect_class": {"description": "Водный тип", "id": 1, "title": "Вода"},
            "effect_parametrs": [
                {
                    "distance": 0,
                    "effect_id": 0,
                    "mass_damage": 0,
                    "over_damage": 0,
                    "power": 2,
                }
            ],
            "effect_type": {
                "description": "Истекает со временем",
                "id": 1,
                "title": "Временные",
            },
            "id": 1,
            "title": "Поджог",
        }
