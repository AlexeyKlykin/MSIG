from pytest import mark, fixture


@fixture(scope="class")
def setup_effect_struct():
    """предустоновка структуры эффектов для теста"""

    effect = GameEffect(
        **{
            "id": 1,
            "title": "Поджог",
            "description": "Остовляет на цели ожог который остается не продолжительное время",
            "effect_type": effect_type,
            "effect_class": effect_class,
            "effect_parametrs": [
                effect_parametr,
            ],
        }
    )


class TestEffectStructGame:
    """Тест структуры эффектов игры"""

    def test_game_effect(self, setup_effect_struct):
        """тест: сборки структуры эффекта"""

        assert setup_effect_struct.effect.model_dump() == {}
