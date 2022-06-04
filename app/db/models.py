from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


# users表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    email = Column(String(64), unique=True, index=True)
    password = Column(String(64))
    access_token = Column(String(64), default=None)
    role = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    items = relationship("Item", back_populates="owner")


# items表
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    description = Column(String(64), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner = relationship("User", back_populates="items")