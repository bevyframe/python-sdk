from bevyframe import *

Base = DeclarativeBase()


class Test(Base):
    __tablename__ = 'test'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    email = DataTypes.Column(DataTypes.String)
    ip = DataTypes.Column(DataTypes.String)
    when = DataTypes.Column(DataTypes.Datetime)