from contextlib import asynccontextmanager
from dotenv import load_dotenv, dotenv_values
from psycopg import AsyncConnection
from psycopg.errors import ConnectionException
from psycopg.pq import PGconn

config = dotenv_values(".env")
load_dotenv()


@asynccontextmanager
async def manager_pg():
    """менеджер для подключения к бд"""

    settings = {}
    pgconn = PGconn()
    conn = AsyncConnection(pgconn=pgconn).connect(**settings, autocommit=True)

    try:
        yield conn

    except ConnectionException as err:
        raise ConnectionException(f"{err}")

    finally:
        conn.close()
