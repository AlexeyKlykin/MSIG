# точка входа в проект
import os
from dotenv import load_dotenv, dotenv_values
from game_engine.game_rules_interface import (
    JsonConfig,
)

load_dotenv()
config = dotenv_values(".env")

pg_settings = {
    "host": os.getenv("PGDBHOST"),
    "port": os.getenv("PGDBPORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def main():
    conn = JsonConfig().get_db_config()
    print(conn)

    # match config.db_type:
    #     case "json":
    #         with JsonConnectionEngine(self._config.db_host) as js:
    #             connfig = dict(js.read())
    #             print("Подключен json")
    #     # case "postgresql":
    #     #     with PgConnectionEngine(self._config) as conn:
    #     #         self.conn = conn
    #     #         print("Подключен postgres")
    #     case _:
    #         print("Нет действий. conn не назначен")
    #
    # return self._game_rules


if __name__ == "__main__":
    main()
