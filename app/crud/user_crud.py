import uuid
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import user_schemas
from ..lib import str_to_sha256


def get_user_by_id(db_session: Session, user_id: int):
    '''根据id查询用户'''
    return db_session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_account(db_session: Session, account: str):
    '''根据账号查询用户'''
    return db_session.query(models.User).filter(models.User.account == account).first()


def get_user_by_email(db_session: Session, email: str):
    '''根据邮箱查询用户'''
    return db_session.query(models.User).filter(models.User.email == email).first()


def get_user_by_token(db_session: Session, access_token: str):
    '''根据token查询用户'''
    return db_session.query(models.User).filter(models.User.access_token == access_token).first()


def get_users(
    db_session: Session,
    account: str|None=None,
    user_name: str|None=None,
    email: str|None=None,
    access_token: str|None=None,
    role_id: int|None=None,
    status: bool|None=None,
    sort: str|None = '+create_time'
):
    '''查询用户'''
    return db_session.query(models.User).filter(
        or_(models.User.account.like(f'%{account}%'), account is None),
        or_(models.User.user_name.like(f'%{user_name}%'), user_name is None),
        or_(models.User.email.like(f'%{email}%'), email is None),
        or_(models.User.access_token == access_token, access_token is None),
        or_(models.User.id.in_(list(map(lambda item: item.user_id, db_session.query(models.UserRole).filter(models.UserRole.role_id == role_id).all()))), role_id is None),
        or_(models.User.status == status, status is None)
    ).order_by(
        and_(models.User.create_time.asc(), sort == '+create_time'),
        and_(models.User.create_time.desc(), sort == '-create_time'),
        and_(models.User.update_time.asc(), sort == '+update_time'),
        and_(models.User.update_time.desc(), sort == '-update_time')
    ).all()


def create_user(db_session: Session, user: user_schemas.UserCreate):
    '''新增用户'''
    db_user = models.User(
        account = user.account,
        user_name = user.user_name,
        email = user.email,
        password = str_to_sha256(user.password),
        status = user.status
    )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    if user.roles:
        for item in user.roles:
            db_user_role = models.UserRole(user_id = db_user.id, role_id = item)
            db_session.add(db_user_role)
    db_session.commit()
    return db_user


def update_user(db_session: Session, user:user_schemas.UserUpdate, user_id: int):
    '''修改用户'''
    db_session.query(models.UserRole).filter(models.UserRole.user_id == user_id).delete()
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    db_user.account = user.account
    db_user.user_name = user.user_name  
    db_user.email = user.email
    if user.password:
        db_user.password = str_to_sha256(user.password)
    db_user.status = user.status
    if user.roles:
        for item in user.roles:
            db_user_role = models.UserRole(user_id = user_id, role_id = item)
            db_session.add(db_user_role)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def delete_user(db_session: Session, user_id: int):
    '''删除用户'''
    db_user_role = db_session.query(models.UserRole).filter(models.UserRole.user_id == user_id).all()
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    [db_session.delete(item) for item in db_user_role]
    db_session.delete(db_user)
    db_session.commit()


def update_token(db_session: Session, user_id: int|None=None, access_token: str|None=None):
    '''
    更新token

    传入user_id时，更新该用户的token，返回token值

    没有传入user_id，且传入token时，删除该token值（此处暂未考虑token重复）
    '''
    if user_id:
        db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
        token = uuid.uuid4()
        db_user.access_token = token
        db_session.commit()
        return token
    elif access_token:
        db_user = db_session.query(models.User).filter(models.User.access_token == access_token).first()
        if db_user:
            db_user.access_token = None
            db_session.commit()
