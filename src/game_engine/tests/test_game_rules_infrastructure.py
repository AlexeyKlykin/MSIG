from typing import List, Tuple
from pytest import fixture, mark, raises

from game_engine.controllers import GameRulesController
from game_engine.configs import JsonConfig, NotConfig
from game_engine.connection_protocols import JsonConnectionEngine
from game_engine.game_rules_infrastructure import (
    PointGameRules,
    GameRulesInterface,
    SubPointGameRules,
)


@fixture(scope="class")
def config_infrastructure():
    rule_one = SubPointGameRules(
        point_game_rules_id=1, id=1, title="Правило", description="Описание правила 1"
    )
    rule_two = SubPointGameRules(
        point_game_rules_id=1, id=2, title="Правило", description="Описание правила 2"
    )
    rule_thri = SubPointGameRules(
        point_game_rules_id=1, id=3, title="Правило", description="Описание правила 3"
    )

    sub_point_list: List[SubPointGameRules] = [
        rule_one,
        rule_two,
        rule_thri,
    ]

    struct_rule = PointGameRules(
        id=1,
        title="Правило 1",
        description="Описание правила 1",
        sub_point_list=sub_point_list,
    )

    gir = GameRulesInterface()
    gir.game_rules = [
        struct_rule,
    ]

    controller = GameRulesController()
    config = JsonConfig()
    controller.settings = config
    controller.rules = gir.game_rules

    yield (controller, gir)


@mark.controller_rules()
class TestGameRulesControler:
    """Тест controller для доступа к настройкам и правилам игры"""

    def test_controller_json_set_rules(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: записываем json файл данными"""

        controller, _ = config_infrastructure

        assert controller.rules.game_rules == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 1,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 1,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]

    def test_controller_json_game_rules_get(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: возврат данных их json"""

        controller, _ = config_infrastructure

        assert controller.rules.game_rules == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 1,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 1,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]

    def test_controller_not_config_rules_get(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: показ всех данных при настройках по умолчанию.
        default_settings без доступа к каким либо базам данных"""

        controller, _ = config_infrastructure
        config = NotConfig()
        controller.settings = config

        assert controller.rules.game_rules == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 1,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 1,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]

    def test_controller_get_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: возврат значения по индексу"""

        controller, _ = config_infrastructure
        rules_one = controller.get_by_idx(0)

        assert rules_one == {
            "description": "Описание правила 1",
            "id": 1,
            "sub_point_list": [
                {
                    "description": "Описание правила 1",
                    "id": 1,
                    "point_game_rules_id": 1,
                    "title": "1.1. Правило",
                },
                {
                    "description": "Описание правила 2",
                    "id": 2,
                    "point_game_rules_id": 1,
                    "title": "1.2. Правило",
                },
                {
                    "description": "Описание правила 3",
                    "id": 3,
                    "point_game_rules_id": 1,
                    "title": "1.3. Правило",
                },
            ],
            "title": "1. Правило 1",
        }

    def test_controller_set_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: добавляем правило по индексу"""

        rule_one = SubPointGameRules(
            point_game_rules_id=1,
            id=1,
            title="Правило",
            description="Описание правила 1",
        )
        rule_two = SubPointGameRules(
            point_game_rules_id=1,
            id=2,
            title="Правило",
            description="Описание правила 2",
        )
        rule_thri = SubPointGameRules(
            point_game_rules_id=1,
            id=3,
            title="Правило",
            description="Описание правила 3",
        )

        sub_point_list: List[SubPointGameRules] = [
            rule_one,
            rule_two,
            rule_thri,
        ]

        struct_rule = PointGameRules(
            id=2,
            title="Правило 2",
            description="Описание правила 2",
            sub_point_list=sub_point_list,
        )

        controller, _ = config_infrastructure
        controller.set_by_idx(1, struct_rule)
        item = controller.get_by_idx(1)

        assert item.model_dump() == {
            "description": "Описание правила 2",
            "id": 2,
            "sub_point_list": [
                {
                    "description": "Описание правила 1",
                    "id": 1,
                    "point_game_rules_id": 1,
                    "title": "2.1. Правило",
                },
                {
                    "description": "Описание правила 2",
                    "id": 2,
                    "point_game_rules_id": 1,
                    "title": "2.2. Правило",
                },
                {
                    "description": "Описание правила 3",
                    "id": 3,
                    "point_game_rules_id": 1,
                    "title": "2.3. Правило",
                },
            ],
            "title": "2. Правило 2",
        }

    def test_controller_delete_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: удаление правила по индексу"""

        controller, _ = config_infrastructure
        first_el = controller.get_by_idx(0)
        controller.delete_by_idx(0)

        assert controller.get_by_idx(0) != first_el

    def test_raise_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: ошибка индекса при попытке доступа к несуществующему правилу"""

        controller, _ = config_infrastructure
        controller = GameRulesController()

        with raises(IndexError):
            controller.get_by_idx(1)

    def test_controller_get_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """получение субправила по индексу"""

        controller, _ = config_infrastructure

        assert controller.get_subpoint_by_idx((0, 1)).model_dump() == {
            "description": "Описание правила 2",
            "id": 2,
            "point_game_rules_id": 1,
            "title": "2.2. Правило",
        }

    def test_controller_set_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """записть субправила"""

        controller, _ = config_infrastructure
        value = SubPointGameRules(
            point_game_rules_id=1,
            id=4,
            title="Правило",
            description="Описание правила 4",
        )
        controller.set_subpoint_by_idx((0, 1), value)

        assert controller.get_subpoint_by_idx((0, 1)).model_dump() == {
            "description": "Описание правила 4",
            "id": 4,
            "point_game_rules_id": 1,
            "title": "Правило",
        }

    def test_controller_delete_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: удаление подправила по индексу"""

        controller, _ = config_infrastructure
        first_el = controller.get_subpoint_by_idx((0, 0))
        controller.delete_subpoint_by_idx((0, 0))

        assert controller.get_subpoint_by_idx((0, 0)) != first_el

    def test_raise_subpoint_idx(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: ошибка индексу при попытке доступа к несуществующему подправилу"""

        controller, _ = config_infrastructure

        with raises(IndexError):
            controller.get_subpoint_by_idx((1, 1))


@mark.connect_db_rules()
class TestConnectDatabase:
    """Тест должен проверять соединение с бд"""

    def test_connect_json_set(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: добавление в json"""

        _, setup_struct = config_infrastructure
        config_json: JsonConfig = JsonConfig(db_name="config.json", db_host="w")

        with JsonConnectionEngine(config_json) as conn:
            conn.write(setup_struct.game_rules[0].model_dump_json())

    def test_connect_json(self):
        """тест: проверки соединения с json"""

        config_json: JsonConfig = JsonConfig(db_name="config.json", db_host="r")
        with JsonConnectionEngine(config_json) as js:
            read_js = js.readlines()

            assert read_js == [
                '{"id":1,"title":"1. Правило 1","description":"Описание правила '
                '1","sub_point_list":[{"id":1,"title":"1.1. '
                'Правило","description":"Описание правила '
                '1","point_game_rules_id":1},{"id":2,"title":"1.2. '
                'Правило","description":"Описание правила '
                '2","point_game_rules_id":1},{"id":3,"title":"1.3. '
                'Правило","description":"Описание правила 3","point_game_rules_id":1}]}',
            ]


@mark.interface_rules()
class TestInterfaceGameRules:
    """Тест интерфейса игровых правил"""

    def test_interface_get_data_list(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: менеджер контекста открытие и закрытие"""

        _, setup_struct = config_infrastructure

        assert [item.model_dump() for item in setup_struct.game_rules] == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 1,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 1,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
        ]

    def test_interface_get_data_dict(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: менеджер контекста сохранения данных"""

        _, setup_struct = config_infrastructure

        assert setup_struct.game_rules[0].model_dump() == {
            "description": "Описание правила 1",
            "id": 1,
            "sub_point_list": [
                {
                    "description": "Описание правила 1",
                    "id": 1,
                    "point_game_rules_id": 1,
                    "title": "1.1. Правило",
                },
                {
                    "description": "Описание правила 2",
                    "id": 2,
                    "point_game_rules_id": 1,
                    "title": "1.2. Правило",
                },
                {
                    "description": "Описание правила 3",
                    "id": 3,
                    "point_game_rules_id": 1,
                    "title": "1.3. Правило",
                },
            ],
            "title": "1. Правило 1",
        }

    def test_interface_set_data_in_list(
        self, config_infrastructure: Tuple[GameRulesController, GameRulesInterface]
    ):
        """тест: добавление к правилам"""

        rule_one = SubPointGameRules(
            point_game_rules_id=2,
            id=1,
            title="Правило",
            description="Описание правила 1",
        )
        rule_two = SubPointGameRules(
            point_game_rules_id=2,
            id=2,
            title="Правило",
            description="Описание правила 2",
        )
        rule_thri = SubPointGameRules(
            point_game_rules_id=2,
            id=3,
            title="Правило",
            description="Описание правила 3",
        )

        sub_point_list: List[SubPointGameRules] = [
            rule_one,
            rule_two,
            rule_thri,
        ]

        struct_rule = PointGameRules(
            id=2,
            title="Правило 2",
            description="Описание правила 2",
            sub_point_list=sub_point_list,
        )

        _, setup_struct = config_infrastructure

        lst: List[PointGameRules] = setup_struct.game_rules
        lst.append(struct_rule)
        setup_struct.game_rules = lst

        assert [item.model_dump() for item in setup_struct.game_rules] == [
            {
                "description": "Описание правила 1",
                "id": 1,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 1,
                        "title": "1.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 1,
                        "title": "1.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 1,
                        "title": "1.3. Правило",
                    },
                ],
                "title": "1. Правило 1",
            },
            {
                "description": "Описание правила 2",
                "id": 2,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "point_game_rules_id": 2,
                        "title": "2.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "point_game_rules_id": 2,
                        "title": "2.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "point_game_rules_id": 2,
                        "title": "2.3. Правило",
                    },
                ],
                "title": "2. Правило 2",
            },
        ]
