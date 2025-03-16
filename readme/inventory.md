
#inventory
Выбрав карту и персонажа, игрок получает доступ к выбору аватара и своему инвентарю. В инвентаре находится:
- описание 
- количество очков
- ресурсы
- эффекты
- доступные испытания
- предметы 
- т.д. 
При наведении курсора на элемент инвентаря выпадает плавающее окошко с описанием этого элемента и ссылкой на элемент в правилах.

### inventory_player

`player_bag` - таблица инвентаря для хранения 

player_bag - resource:(1:N)
player_bag - user_role:(1:1) - инвентарь привязан к игроку
player_bag - effects:(1:N)
player_bag - events:(1:N)
player_bag - game_item:(1:N)

```sql
create table if not exists game_engine.player_bag(
	user_role_id int references game_engine.user_role(user_role_id),
	resource_id int references game_engine.resource(resource_id)	
	...
);
```