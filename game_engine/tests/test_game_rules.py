"""
Тесты создания класса и интерфейса правил игры.
"""

from pytest import raises

from game_engine.game_rules import (
    GameRulesInterface,
    GameRulesStruct,
    PointRulesInterface,
    SubPointRulesInterface,
    SubPointRules,
    PointRules,
)


class TestPointRules:
    """Тест структуры подзаголовка правил"""

    def test_invalid_point_number(self):
        """тест: ошибка валидации номера заголовка"""

        with raises(ValueError):
            PointRules(
                sub_point_number="sd",  # type: ignore
                title="пункт",
            )

    def test_valid_point_number_as_float(self):
        """тест: валидация номера когда передается число с плавающей точкой"""

        pr = PointRules(
            point_number=1.1,  # type: ignore
            title="пункт",
        )

        assert isinstance(pr.point_number, int)

    def test_valid_point_number_as_str(self):
        """тест: валидация подпункта когда передается строка"""

        pr = PointRules(
            point_number="1",  # type: ignore
            title="пункт",
        )

        assert isinstance(pr.point_number, int)


class TestSubPointRules:
    """Тест структуры подзаголовка правил"""

    def test_invalid_sub_point_number(self):
        """тест: ошибка валидации номера подзаголовка"""

        with raises(ValueError):
            SubPointRules(
                sub_point_number="sd",  # type: ignore
                title="Подпункт",
                description="Описание",
            )

    def test_valid_sub_point_number_as_int(self):
        """тест: валидация номера когда передается число"""

        spr = SubPointRules(
            sub_point_number=1,  # type: ignore
            title="Подпункт",
            description="Описание",
        )

        assert isinstance(spr.sub_point_number, float)

    def test_valid_sub_point_number_as_str(self):
        """тест: валидация подпункта когда передается строка"""

        spr = SubPointRules(
            sub_point_number="1",  # type: ignore
            title="Подпункт",
            description="Описание",
        )

        assert isinstance(spr.sub_point_number, float)


class TestGameRulesInterface:
    """Тест игровых правил"""

    def test_point_rules_interface(self):
        """тест: интерфейса использования заголовка списков правил"""

        value = (1, "Заголовок правил")
        point_interface = PointRulesInterface()
        point_interface.set_rules(value)
        assert dict(point_interface.get_rules()) == {  # type: ignore
            "point_number": 1,
            "title": "Заголовок правил",
        }

    def test_subpoint_rules_interface(self):
        """тест: интерфейс использования списка правил"""

        value = (1.1, "Правило 1.1", "Описание правил")
        sub_point_interface = SubPointRulesInterface()
        sub_point_interface.set_rules(value)
        assert dict(sub_point_interface.get_rules()) == {  # type: ignore
            "sub_point_number": 1.1,
            "title": "Правило 1.1",
            "description": "Описание правил",
        }

    def test_game_rules_interface(self):
        """тест: интерфейс управления игровыми правилами"""

        value_pri = (1, "Заголовок правил")
        point = PointRulesInterface()
        point.set_rules(value_pri)
        get_point = point.get_rules()
        value_spri = (1.1, "Правило 1.1", "Описание правил")
        sub_point_interface = SubPointRulesInterface()
        sub_point_interface.set_rules(value_spri)
        get_sub_point = sub_point_interface.get_rules()
        if get_point is not None:
            game_rules = GameRulesInterface(point=get_point)
            if get_sub_point is not None:
                game_rules.set_rules(get_sub_point)

                assert dict(game_rules.get_rules()) == {
                    "header": PointRules(
                        point_number=1,
                        title="Заголовок правил",
                        computed_title="1 Заголовок правил",  # type: ignore
                    ),
                    "rules_list": [
                        SubPointRules(
                            sub_point_number=1.1,
                            title="Правило 1.1",
                            description="Описание правил",
                            computed_title="1.1 Правило 1.1",  # type: ignore
                        )
                    ],
                }
