from sqlalchemy import create_engine, Column as Col, Integer as Int, String as Str, DateTime as Dt, Boolean as Bool
from sqlalchemy.orm import sessionmaker, query, DeclarativeBase


class DataTypes:
    Integer = Int
    String = Str
    Datetime = Dt
    Bool = Bool
    Column = Col


class Database:
    def __init__(self, app, url: str, base: DeclarativeBase) -> None:
        self.__engine = create_engine(url)
        self.__url = url
        self.__session = sessionmaker(bind=self.__engine)()
        self.__base = base
        app.db = self

    def add(self, data: object) -> None:
        return self.__session.add(data)

    def delete(self, data: object) -> None:
        return self.__session.delete(data)

    def commit(self) -> None:
        return self.__session.commit()

    def query(self, model) -> query.Query[object]:
        return self.__session.query(model)

    @property
    def Model(self) -> DeclarativeBase:
        return self.__base

    def create_all(self) -> None:
        return self.__base.metadata.create_all(self.__engine)
