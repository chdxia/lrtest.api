from sqlalchemy.orm import Session
from ..models import models


def get_roles(db_session: Session):
    '''查询角色'''
    return db_session.query(models.Role).all()
