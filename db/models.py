from .session import Base
from sqlalchemy import Column, Integer, String, Integer, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, index=True)


# Purchase model
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))


# Report model
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
