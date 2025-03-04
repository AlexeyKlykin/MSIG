from pytest import fixture, mark
from game_engine.controllers import GameItemController
from game_engine.game_elements.game_items import (
    GameItem,
    GameItemClass,
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
            "id": 1,
            "title": "Обычное",
            "description": "Не несет не каких дополнительных эффектов",
        }
    )
    item_type = GameItemType(
        **{
            "id": 1,
            "title": "Огнестрельное",
            "description": "Тип огнестрел являеться простым и эффективным",
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
            "id": 1,
            "title": "Стихия огонь",
            "description": "Стихийный эффект ввиде опции на оружии",
            "range_of_numeric_values": (1, 10),
        }
    )
    item = GameItem(
        **{
            "id": 1,
            "title": "Обычное ружье",
            "description": "Обычное ружье - дешевый огнестрел. Работает на близком расстоянии.",
            "item_class": item_class,
            "item_type": item_type,
            "item_parametrs": item_parametr,
            "item_options": [
                item_option,
            ],
        }
    )

    controller = GameItemController()
    controller.item_class = item_class
    controller.item_type = item_type
    controller.item_parametr = item_parametr
    controller.item_option = item_option
    controller.game_item = item

    yield controller


@mark.items_game()
class TestItemsGame:
    """Тест структуры предметов игры"""

    def test_game_item_class(self, setup_items_config):
        """тест: получение класса предмета"""

        assert setup_items_config.item_class.model_dump() == {
            "id": 1,
            "title": "Обычное",
            "description": "Не несет не каких дополнительных эффектов",
        }

    def test_game_item_type(self, setup_items_config):
        """тест: получения структуры типа предмета игры"""

        assert setup_items_config.item_type.model_dump() == {
            "id": 1,
            "title": "Огнестрельное",
            "description": "Тип огнестрел являеться простым и эффективным",
        }

    def test_game_item_option(self, setup_items_config):
        """тест: получение структуры опций предмета игры"""

        assert setup_items_config.item_option.model_dump() == {
            "id": 1,
            "title": "Стихия огонь",
            "description": "Стихийный эффект ввиде опции на оружии",
            "range_of_numeric_values": (1, 10),
        }

    def test_game_item_parametr(self, setup_items_config):
        """тест: получение структуры параметров предмета игры"""

        assert setup_items_config.item_parametr.model_dump() == {
            "item_id": 1,
            "power": 2,
            "distance": 1,
            "over_damage": 0,
            "mass_damage": 0,
        }

    def test_get_item_game(self, setup_items_config):
        """тест: получение предмета"""

        assert setup_items_config.game_item.model_dump() == {
            "item_class": {
                "description": "Не несет не каких дополнительных эффектов",
                "id": 1,
                "title": "Обычное",
            },
            "description": "Обычное ружье - дешевый огнестрел. Работает на близком расстоянии.",
            "id": 1,
            "item_options": [
                {
                    "id": 1,
                    "title": "Стихия огонь",
                    "description": "Стихийный эффект ввиде опции на оружии",
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
            "title": "Обычное ружье",
            "item_type": {
                "description": "Тип огнестрел являеться простым и эффективным",
                "id": 1,
                "title": "Огнестрельное",
            },
        }
