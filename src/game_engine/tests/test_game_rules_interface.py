from typing import List
from pytest import fixture, mark

from game_engine.api import Api
from game_engine.game_rules_interface import (
    JsonConfig,
    JsonConnectionEngine,
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

    gir = GameRulesInterface()
    gir.game_rules = [
        struct_rule,
    ]

    api = Api()
    config = JsonConfig()
    api.settings = config
    api.set_rules(gir.game_rules)

    yield gir


@mark.connect_db_rules()
class TestApiControllGameRules:
    """Тест api для доступа к настройкам и правилам игры"""

    def test_api_json_set_rules(self, setup_struct: GameRulesInterface):
        """тест: записываем json файл данными"""

        config = JsonConfig()
        api = Api()
        api.settings = config
        api.set_rules(setup_struct.game_rules)
        game_rules = api.get_rules()

        assert game_rules.game_rules == [
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

    def test_api_json_game_rules_get(self):
        config = JsonConfig()
        api = Api()
        api.settings = config
        game_rules = api.get_rules()

        assert game_rules.game_rules == [
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

    def test_api_not_config_rules_get(self, setup_struct: GameRulesInterface):
        """тест: показ всех данных"""

        config = NotConfig()
        api = Api()
        api.settings = config
        game_rules = api.get_rules()
        game_rules.game_rules = setup_struct.game_rules

        assert [item.model_dump() for item in game_rules.game_rules] == [
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


@mark.connect_db_rules()
class TestConnectDatabase:
    """Тест должен проверять соединение с бд"""

    def test_connect_json_set(self, setup_struct):
        """тест: добавление в json"""

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

    def test_interface_get_data_list(self, setup_struct):
        """тест: менеджер контекста открытие и закрытие"""

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

    def test_interface_get_data_dict(self, setup_struct):
        """тест: менеджер контекста сохранения данных"""

        assert [
            item.model_dump() for item in setup_struct.game_rules if item.id == 1
        ] == [
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

    def test_interface_set_data_in_list(self, setup_struct):
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
