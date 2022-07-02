from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database.mysql import Base


class Role(Base):
    '''roles表'''
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, unique=True, nullable=False)
    role_name = Column(String(64), nullable=False)
    role_base = relationship("User", back_populates="roles")


class User(Base):
    '''users表'''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    email = Column(String(64), unique=True, nullable=False)
    password = Column(String(64))
    access_token = Column(String(64), default=None)
    role = Column(Integer, ForeignKey("roles.role_id"))
    status = Column(Boolean, default=True, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    items = relationship("Item", back_populates="owner")
    roles = relationship("Role", back_populates="role_base")


class Item(Base):
    '''items表'''
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64))
    description = Column(String(64))
    owner_id = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner = relationship("User", back_populates="items")
