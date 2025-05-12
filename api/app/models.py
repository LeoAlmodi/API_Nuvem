from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id              = Column(Integer, primary_key=True, index=True)
    nome            = Column(String(100), nullable=False)
    email           = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
