from datetime import datetime


class Test:
    __tablename__ = 'test'
    __primary_key__ = 'id'
    id: int
    email: str
    ip: str
    when: datetime
