from typing import List
from pydantic import BaseConfig
from pytest import fixture

from game_engine.game_rules_interface import (
    DataBaseConfig,
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

    write_data = [
        struct_rule,
    ]

    config: DataBaseConfig = NotConfig(
        db_type="not config",
        db_host="local",
        db_port=1,
        db_username="neon",
        db_name="msig",
        db_password="vbnzq",
    )
    cli = GameRulesInterface(config=config)
    cli.game_rules = write_data

    # config_json: JsonConfig = JsonConfig(db_name="config.json")

    # with JsonConnectionEngine(config_json) as conn:
    #     conn.write(config_json.model_dump_json())

    yield cli

    cli.game_rules = []


# class TestConnectDatabase:
#     """Тест должен проверять соединение с бд"""
#
#     def test_connect_json(self):
#         """тест: проверки соединения с json"""
#
#     def test_connect_pg(self):
#         """тест: проверки соединения с postgres"""
#
#     def test_connect_not_config(self):
#         """тест: проверки соединения без конфигурации"""
#


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

    def test_json_get_config(self):
        """тест: управления взаимодействия с json"""

        config = JsonConfig()
        json_setup = GameRulesInterface(config=config)

        assert json_setup.config == {
            "db_host": "w+",
            "db_name": "msig",
            "db_password": "vbnzq",
            "db_port": 1,
            "db_type": "json",
            "db_username": "neon",
        }

    def test_json_set_config(self):
        """тест: добавление своего конфига"""

        config = JsonConfig(db_name="config.json")
        json_setup = GameRulesInterface(config=config)
        json_setup.config = config

        assert json_setup.config == {
            "db_host": "w+",
            "db_name": "config.json",
            "db_password": "vbnzq",
            "db_port": 1,
            "db_type": "json",
            "db_username": "neon",
        }
