from pytest import fixture
from game_engine.struct_game_rules import GameRulesJsonManager, PointGameRules
#
#
# @fixture(scope="class")
# def setup_manager():
#     value = PointGameRules(id=1, title="1. Правило", description="Описание правила 1")
#
#     with GameRulesJsonManager("game_rules.json") as js:
#         js.save_state(value.model_dump_json())
#         yield js
#
#
# class TestInterfaceGameRules:
#     """Тест интерфейса игровых правил"""
#
#     def test_manager_context_json(self, setup_manager):
#         """тест: менеджер контекста открытие и закрытие"""
#
#         assert isinstance(setup_manager, GameRulesJsonManager)
#
#     def test_manager_interface_json_save_data(self, setup_manager):
#         """тест: менеджер контекста сохранения данных"""
#
#     def test_manager_interface_json_get_by_key(self):
#         """тест: менеджер контекста получение данных по ключу"""
#
#         # with GameRulesJsonManager("game_rules.json") as js:
