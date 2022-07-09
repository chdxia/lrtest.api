from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database.mysql import Base


class Role(Base):
    '''roles表'''
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(64), unique=True, nullable=False)
    users = relationship("User", back_populates="roles")


class User(Base):
    '''users表'''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(64), unique=True, nullable=False)
    user_name = Column(String(64))
    email = Column(String(64), unique=True, nullable=False)
    password = Column(String(64))
    access_token = Column(String(64), default=None)
    role_id = Column(Integer, ForeignKey("roles.id"))
    status = Column(Boolean, default=True, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    roles = relationship("Role", back_populates="users")
