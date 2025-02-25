from typing import List
from pytest import fixture

from game_engine.game_rules_interface import (
    NotConfig,
    PointGameRules,
    GameRulesInterface,
    DictGameRules,
)


@fixture(scope="class")
def setup_struct():
    rule_one = PointGameRules(id=1, title="Правило", description="Описание правила 1")
    rule_two = PointGameRules(id=2, title="Правило", description="Описание правила 2")
    rule_thri = PointGameRules(id=3, title="Правило", description="Описание правила 3")

    sub_point_list: List[PointGameRules] = [
        rule_one,
        rule_two,
        rule_thri,
    ]

    struct_rule = DictGameRules(
        id=1,
        title="Правило 1",
        description="Описание правила 1",
        sub_point_list=sub_point_list,
    )

    write_data = [
        struct_rule,
    ]

    config = NotConfig(db_type="", db_name="")
    gri = GameRulesInterface(config)
    gri.game_rules = write_data
    yield gri.game_rules


class TestInterfaceGameRules:
    """Тест интерфейса игровых правил"""

    def test_interface_get_data_list(self, setup_struct):
        """тест: менеджер контекста открытие и закрытие"""

        assert [item.model_dump() for item in setup_struct] == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]

    def test_interface_get_data_dict(self, setup_struct):
        """тест: менеджер контекста сохранения данных"""

        assert [item.model_dump() for item in setup_struct if item.id == 1] == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]
