from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..models import models


def get_user_role_by_id(db_session: Session, user_id: int|None=None, role_id: int|None=None):
    '''根据id查询用户的角色'''
    db_user_role = db_session.query(models.UserRole).filter(
        or_(models.UserRole.user_id == user_id, user_id is None),
        or_(models.UserRole.role_id == role_id, role_id is None)
    ).all()
    return db_user_role


def get_role_by_id(db_session: Session, role_id: int):
    '''根据id查询角色'''
    return db_session.query(models.Role).filter(models.Role.id == role_id).first()


def get_roles(db_session: Session):
    '''查询角色'''
    return db_session.query(models.Role).order_by(models.Role.id.asc()).all()


def create_role(db_session: Session, role_name: str):
    '''新增角色'''
    db_role = models.Role(role_name = role_name)
    db_session.add(db_role)
    db_session.commit()
    db_session.refresh(db_role)
    return db_role


def delete_role(db_session: Session, role_id: int):
    '''删除角色'''
    db_role = db_session.query(models.Role).filter(models.Role.id == role_id).first()
    db_session.delete(db_role)
    db_session.commit()
