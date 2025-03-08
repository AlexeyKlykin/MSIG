# точка входа в проект
import os
from dotenv import load_dotenv, dotenv_values

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
    pass


if __name__ == "__main__":

    class Coordinate:
        def __set_name__(self, owner, name):
            self._name = name

        def __get__(self, instance, owner):
            print(dir(instance))
            print(dir(owner))
            return instance.__dict__[self._name]

        def __set__(self, instance, value):
            try:
                instance.__dict__[self._name] = float(value)
                print("Validated!")
            except ValueError:
                raise ValueError(f'"{self._name}" must be a number') from None

    class Point:
        x = Coordinate()
        y = Coordinate()

        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Point(1, 2)
    p.x
