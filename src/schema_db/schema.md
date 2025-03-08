## Game rules

```sql
-- game rules
create table if not exists game_rules.point_game_rule(
	point_game_rule_id bigint generated always as identity primary key,
	title varchar(300) not null,
	description text not null
);

comment on table game_rules.point_game_rule is 'таблица пунктов правил игры';
comment on column game_rules.point_game_rule.point_game_rule_id is 'идентификатор/номер пункта правил игры';
comment on column game_rules.point_game_rule.title is 'название пункта правил игры';
comment on column game_rules.point_game_rule.description is 'описание пункта правил игры';

create table if not exists game_rules.sub_point_game_rule(
  sub_point_game_rule_id bigint generated always as identity primary key,
  point_game_rule_id bigint references game_rules.point_game_rule(point_game_rule_id),
  title varchar(300) not null,
  description text not null
);

comment on table game_rules.sub_point_game_rule is 'таблица под пунктов правил игры';
comment on column game_rules.sub_point_game_rule.sub_point_game_rule_id is 'идентификатор/номер под пунктов правил игры';
comment on column game_rules.sub_point_game_rule.point_game_rule_id is 'идентификатор связи подпунктов с пунктом правил игры';
comment on column game_rules.sub_point_game_rule.title is 'название подпункта правил игры';
comment on column game_rules.sub_point_game_rule.description is 'описание подпункта правил игры';
```

## Game engine

```sql
create table if not exists game_engine.role(
  role_id int generated always as identity primary key,
  title varchar(300) not null,
  description text
);

-- player
create table if not exists game_engine.player(
  player_id bigint generated always as identity primary key,
  role_id int not null references game_engine.role(role_id),
  player_name varchar(300) not null,
  player_ava_link text
);

create table if not exists game_engine.player_inventory(
  player_id bigint generated always as identity primary key
);

-- map
create table if not exists game_engine.map(
  map_id bigint generated always as identity primary key,
  title varchar(300) not null,
  description text not null,
  link_img_for_map text not null
);

comment on table game_engine.map is 'таблица карты игры';
comment on column game_engine.map.map_id is 'идентификатор карты игры';
comment on column game_engine.map.title is 'название карты игры';
comment on column game_engine.map.description is 'описание карты игры';
comment on column game_engine.map.link_img_for_map is 'ссылка на изображение карты игры';

create table if not exists game_engine.natural_zone(
  natural_zone_id bigint generated always as identity primary key,
  map_id bigint not null references game_engine.map(map_id),
  title varchar(300) not null,
  description text not null
);

create table if not exists game_engine.cell_map(
  cell_map_id bigint generated always as identity primary key,
  map_id bigint not null references game_engine.map(map_id),
  natural_zone_id not null references game_engine.natural_zone(natural_zone_id),
  title varchar(300) not null,
  is_active bool default true
);

create table if not exists game_engine.resources(
  resources_id int generated always as identity primary key,
  player_id bigint references game_engine.player_inventory(player_id),
  cell_map_id bigint references game_engine.cell_map(cell_map_id),
  title varchar(300) not null,
  description text
);

create table if not exists game_engine.mage_element(
  mage_element_id bigint generated always as identity primary key,
  title varchar(300) not null,
  description text not null
);

create table if not exists game_engine.physical_effect(
  physical_effect_id bigint generated always as identity primary key,
  title varchar(300) not null,
  description text not null
);

create table if not exists game_engine.effect(
  effect_id bigint generated always as identity primary key,
  cell_map_id bigint references game_engine.cell_map(cell_map_id),
  mage_element_id bigint references game_engine.mage_element(mage_element_id),
  physical_effect_id bigint references game_engine.physical_effect(physical_effect_id),
  player_id bigint references game_engine.player_inventory(player_id),
  title varchar(300) not null,
  description text
);

create table if not exists game_engine.trap(
  trap_id bigint generated always as identity primary key,
  cell_map_id bigint not null references game_engine.cell_map(cell_map_id),
  effect_id bigint references game_engine.effect(effect_id), 
  title varchar(300) not null,
  description text not null
);

create table if not exists game_engine.vacation_spot(
  vacation_spot_id bigint generated always as identity primary key,
  cell_map_id bigint not null references game_engine.cell_map(cell_map_id),
  title varchar(300) not null,
  description text
);

create table if not exists game_engine.game_store(
  game_store_id bigint generated always as identity primary key,
  cell_map_id bigint not null references game_engine.cell_map(cell_map_id),
  title varchar(300) not null,
  description text
);

create table if not exists game_engine.game_item(
  game_item_id bigint generated always as identity primary key,
  game_store_id bigint references game_engine.game_store(game_store_id),
  effect_id bigint references game_engine.effect(effect_id),
  player_id bigint references game_engine.player_inventory(player_id),
  title varchar(300) not null,
  description text not null
);


```
