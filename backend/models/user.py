from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.clients.postgres_client import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    