class TestBuildControllGameRules: ...


#
# @fixture(scope="class")
# def setup_struct():
#     rule_one = PointGameRules(id=1, title="Правило", description="Описание правила 1")
#     rule_two = PointGameRules(id=2, title="Правило", description="Описание правила 2")
#     rule_thri = PointGameRules(id=3, title="Правило", description="Описание правила 3")
#
#     sub_point_list: List[PointGameRules] = [
#         rule_one,
#         rule_two,
#         rule_thri,
#     ]
#
#     struct_rule = DictGameRules(
#         id=1,
#         title="Правило 1",
#         description="Описание правила 1",
#         sub_point_list=sub_point_list,
#     )
#
#     gir = GameRulesInterface()
#     gir.game_rules = [
#         struct_rule,
#     ]
#     yield gir


# ручки для записи игровых правил в Json
# интерфеис максимально простой
# чтение м запись
