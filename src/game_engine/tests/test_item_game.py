from pytest import fixture, mark
from game_engine.game_elements.game_items import (
    GameItem,
    GameItemClass,
    GameItemInterface,
    GameItemOption,
    GameItemParametr,
    GameItemType,
)


@fixture(scope="class")
def setup_items_config():
    """подготовка настроек для теста
    структуры предметов в игре"""

    item_class = GameItemClass(
        **{
            "class_item_id": 1,
            "class_item_title": "Обычное",
            "class_item_description": "Не несет не каких дополнительных эффектов",
        }
    )
    item_type = GameItemType(
        **{
            "type_item_id": 1,
            "type_item_title": "Огнестрельное",
            "type_item_description": "Тип огнестрел являеться простым и эффективным",
        }
    )
    item_parametr = GameItemParametr(
        **{
            "item_id": 1,
            "power": 2,
            "distance": 1,
            "over_damage": 0,
            "mass_damage": 0,
        }
    )
    item_option = GameItemOption(
        **{
            "item_option_id": 1,
            "item_option_title": "Стихия огонь",
            "item_option_description": "Стихийный эффект ввиде опции на оружии",
            "range_of_numeric_values": (1, 10),
        }
    )
    item = GameItem(
        **{
            "item_id": 1,
            "item_title": "Обычное ружье",
            "item_description": "Обычное ружье - дешевый огнестрел. Работает на близком расстоянии.",
            "item_class": item_class,
            "item_type": item_type,
            "item_parametrs": item_parametr,
            "item_options": [
                item_option,
            ],
        }
    )
    gii = GameItemInterface()
    gii.item = item

    yield gii


@mark.items_game()
class TestItemsGame:
    """Класс тестирования предметов игры"""

    def test_game_item_class(self, setup_items_config):
        """тест: получение класса предмета"""

        assert setup_items_config.item.item_class.model_dump() == {
            "class_item_id": 1,
            "class_item_title": "Обычное",
            "class_item_description": "Не несет не каких дополнительных эффектов",
        }

    def test_game_item_type(self, setup_items_config):
        """тест: получения структуры типа предмета игры"""

        assert setup_items_config.item.item_type.model_dump() == {
            "type_item_id": 1,
            "type_item_title": "Огнестрельное",
            "type_item_description": "Тип огнестрел являеться простым и эффективным",
        }

    def test_game_item_option(self, setup_items_config):
        """тест: получение структуры опций предмета игры"""

        assert [item.model_dump() for item in setup_items_config.item.item_options] == [
            {
                "item_option_id": 1,
                "item_option_title": "Стихия огонь",
                "item_option_description": "Стихийный эффект ввиде опции на оружии",
                "range_of_numeric_values": (1, 10),
            }
        ]

    def test_get_item_game(self, setup_items_config):
        """тест: получение предмета"""

        assert setup_items_config.item.model_dump() == {
            "item_class": {
                "class_item_description": "Не несет не каких дополнительных эффектов",
                "class_item_id": 1,
                "class_item_title": "Обычное",
            },
            "item_description": "Обычное ружье - дешевый огнестрел. Работает на близком расстоянии.",
            "item_id": 1,
            "item_options": [
                {
                    "item_option_id": 1,
                    "item_option_title": "Стихия огонь",
                    "item_option_description": "Стихийный эффект ввиде опции на оружии",
                    "range_of_numeric_values": (1, 10),
                }
            ],
            "item_parametrs": {
                "distance": 1,
                "item_id": 1,
                "mass_damage": 0,
                "over_damage": 0,
                "power": 2,
            },
            "item_title": "Обычное ружье",
            "item_type": {
                "type_item_description": "Тип огнестрел являеться простым и эффективным",
                "type_item_id": 1,
                "type_item_title": "Огнестрельное",
            },
        }

    def test_item_interface(self):
        """тест: интерфейса создания класса предмета"""

        gic = GameItemClass(
            **{
                "class_item_id": 1,
                "class_item_title": "Ракета м1",
                "class_item_description": "Описание ракеты m1",
            }
        )
        gici = GameItemInterface()
        gici.item = gic

        assert gici.item.model_dump() == {
            "class_item_id": 1,
            "class_item_title": "Ракета м1",
            "class_item_description": "Описание ракеты m1",
        }
