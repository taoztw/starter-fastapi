from db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, Text


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    refresh_token = Column(Text, nullable=True)
