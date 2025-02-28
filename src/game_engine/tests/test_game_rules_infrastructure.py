from typing import List, Tuple
from pytest import fixture, mark, raises

from game_engine.api import GameRulesApi
from game_engine.configs import JsonConfig, NotConfig
from game_engine.connection_protocols import JsonConnectionEngine
from game_engine.game_rules_infrastructure import (
    PointGameRules,
    GameRulesInterface,
    DictGameRules,
)


@fixture(scope="class")
def config_infrastructure():
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

    gir = GameRulesInterface()
    gir.game_rules = [
        struct_rule,
    ]

    api = GameRulesApi()
    config = JsonConfig()
    api.settings = config
    api.rules = gir.game_rules

    yield (api, gir)


@mark.api_rules()
class TestGameRulesApiControll:
    """Тест api для доступа к настройкам и правилам игры"""

    def test_api_json_set_rules(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: записываем json файл данными"""

        api, _ = config_infrastructure

        assert api.rules.game_rules == [
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

    def test_api_json_game_rules_get(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: возврат данных их json"""

        api, _ = config_infrastructure

        assert api.rules.game_rules == [
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

    def test_api_not_config_rules_get(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: показ всех данных"""

        api, _ = config_infrastructure
        config = NotConfig()
        api.settings = config

        assert api.rules.game_rules == [
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

    def test_api_get_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: возврат значения по индексу"""

        api, _ = config_infrastructure
        rules_one = api.get_by_idx(0)

        assert rules_one == {
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
        }

    def test_api_set_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: добавляем правило по индексу"""

        rule_one = PointGameRules(
            id=1, title="Правило", description="Описание правила 1"
        )
        rule_two = PointGameRules(
            id=2, title="Правило", description="Описание правила 2"
        )
        rule_thri = PointGameRules(
            id=3, title="Правило", description="Описание правила 3"
        )

        sub_point_list: List[PointGameRules] = [
            rule_one,
            rule_two,
            rule_thri,
        ]

        struct_rule = DictGameRules(
            id=2,
            title="Правило 2",
            description="Описание правила 2",
            sub_point_list=sub_point_list,
        )

        api, _ = config_infrastructure
        api.set_by_idx(1, struct_rule)
        item = api.get_by_idx(1)

        assert item.model_dump() == {
            "description": "Описание правила 2",
            "id": 2,
            "sub_point_list": [
                {
                    "description": "Описание правила 1",
                    "id": 1,
                    "title": "2.1. Правило",
                },
                {
                    "description": "Описание правила 2",
                    "id": 2,
                    "title": "2.2. Правило",
                },
                {
                    "description": "Описание правила 3",
                    "id": 3,
                    "title": "2.3. Правило",
                },
            ],
            "title": "2. Правило 2",
        }

    def test_api_delete_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: удаление правила по индексу"""

        api, _ = config_infrastructure
        first_el = api.get_by_idx(0)
        api.delete_by_idx(0)

        assert api.get_by_idx(0) != first_el

    def test_raise_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: ошибка индекса при попытке доступа к несуществующему правилу"""

        api, _ = config_infrastructure
        api = GameRulesApi()

        with raises(IndexError):
            api.get_by_idx(1)

    def test_api_get_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """получение субправила по индексу"""

        api, _ = config_infrastructure

        assert api.get_subpoint_by_idx((0, 1)).model_dump() == {
            "description": "Описание правила 2",
            "id": 2,
            "title": "2.2. Правило",
        }

    def test_api_set_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """записть субправила"""

        api, _ = config_infrastructure
        value = PointGameRules(id=4, title="Правило", description="Описание правила 4")
        api.set_subpoint_by_idx((0, 1), value)

        assert api.get_subpoint_by_idx((0, 1)).model_dump() == {
            "description": "Описание правила 4",
            "id": 4,
            "title": "Правило",
        }

    def test_api_delete_subpoint_by_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: удаление подправила по индексу"""

        api, _ = config_infrastructure
        first_el = api.get_subpoint_by_idx((0, 0))
        api.delete_subpoint_by_idx((0, 0))

        assert api.get_subpoint_by_idx((0, 0)) != first_el

    def test_raise_subpoint_idx(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: ошибка индексу при попытке доступа к несуществующему подправилу"""

        api, _ = config_infrastructure

        with raises(IndexError):
            api.get_subpoint_by_idx((1, 1))


@mark.connect_db_rules()
class TestConnectDatabase:
    """Тест должен проверять соединение с бд"""

    def test_connect_json_set(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
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
                'Правило","description":"Описание правила 1"},{"id":2,"title":"1.2. '
                'Правило","description":"Описание правила 2"},{"id":3,"title":"1.3. '
                'Правило","description":"Описание правила 3"}]}',
            ]


@mark.interface_rules()
class TestInterfaceGameRules:
    """Тест интерфейса игровых правил"""

    def test_interface_get_data_list(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
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

    def test_interface_get_data_dict(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
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
        }

    def test_interface_set_data_in_list(
        self, config_infrastructure: Tuple[GameRulesApi, GameRulesInterface]
    ):
        """тест: добавление к правилам"""

        rule_one = PointGameRules(
            id=1, title="Правило", description="Описание правила 1"
        )
        rule_two = PointGameRules(
            id=2, title="Правило", description="Описание правила 2"
        )
        rule_thri = PointGameRules(
            id=3, title="Правило", description="Описание правила 3"
        )

        sub_point_list: List[PointGameRules] = [
            rule_one,
            rule_two,
            rule_thri,
        ]

        struct_rule = DictGameRules(
            id=2,
            title="Правило 2",
            description="Описание правила 2",
            sub_point_list=sub_point_list,
        )

        _, setup_struct = config_infrastructure

        lst: List[DictGameRules] = setup_struct.game_rules
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
            {
                "description": "Описание правила 2",
                "id": 2,
                "sub_point_list": [
                    {
                        "description": "Описание правила 1",
                        "id": 1,
                        "title": "2.1. Правило",
                    },
                    {
                        "description": "Описание правила 2",
                        "id": 2,
                        "title": "2.2. Правило",
                    },
                    {
                        "description": "Описание правила 3",
                        "id": 3,
                        "title": "2.3. Правило",
                    },
                ],
                "title": "2. Правило 2",
            },
        ]
