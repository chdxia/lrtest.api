import uuid
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from . import schemas, models
from ..utils.common import str_to_sha256


def get_user_by_id(db_session: Session, user_id: int):
    '''根据id查询用户'''
    return db_session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db_session: Session, email: str):
    '''根据邮箱查询用户（验证邮箱是否已存在）'''
    return db_session.query(models.User).filter(models.User.email == email).first()


def get_users(
    db_session: Session,
    name: str|None=None,
    email: str|None=None,
    access_token: str|None=None,
    role: int|None=None,
    status: bool|None=None,
    sort: str|None = '+create_time'
):
    '''查询用户'''
    return db_session.query(models.User).filter(
        or_(models.User.name.like(f'%{name}%'), name is None),
        or_(models.User.email.like(f'%{email}%'), email is None),
        or_(models.User.access_token == access_token, access_token is None),
        or_(models.User.role == role, role is None),
        or_(models.User.status == status, status is None)
    ).order_by(
        and_(models.User.create_time.asc(), sort == '+create_time'),
        and_(models.User.create_time.desc(), sort == '-create_time'),
        and_(models.User.update_time.asc(), sort == '+update_time'),
        and_(models.User.update_time.desc(), sort == '-update_time')
    ).all()


def create_user(db_session: Session, user: schemas.UserCreate):
    '''新增用户'''
    db_user = models.User(name=user.name, email=user.email, password=str_to_sha256(user.password), role=user.role, status=user.status)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def update_user(db_session: Session, user:schemas.UserUpdate, user_id):
    '''修改用户'''
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    user_dict = user.dict()
    db_user.name = user_dict['name']
    db_user.email = user_dict['email']
    if user_dict['password'] :
        db_user.password = str_to_sha256(user_dict['password'])
    db_user.role = user_dict['role']
    db_user.status = user_dict['status']
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def delete_user(db_session: Session, user_id):
    '''删除用户'''
    db_session.query(models.User).filter(models.User.id == user_id).delete()
    db_session.commit()


def update_token(db_session: Session, user_id: int|None=None, access_token: str|None=None):
    '''更新token'''
    # 传入user_id时，更新该用户的token
    if user_id:
        db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
        token = uuid.uuid4()
        db_user.access_token = token
        db_session.commit()
        db_session.refresh(db_user)
        return token
    # 没有传入user_id，且传入token时，删除该token值（此处暂未考虑token重复）
    elif access_token:
        db_user = db_session.query(models.User).filter(models.User.access_token == access_token).first()
        if db_user:
            db_user.access_token = None
            db_session.commit()
            db_session.refresh(db_user)


def get_items(db_session:Session, user_id:int|None=None, title:str|None=None, description:str|None=None, skip:int =0, limit:int =10):
    '''查询物品'''
    return db_session.query(models.Item).filter(
        or_(models.Item.owner_id == user_id, user_id is None),
        or_(models.Item.title.like(f'%{title}%'), title is None),
        or_(models.Item.description.like(f'%{description}%'), description is None)
    ).offset(skip).limit(limit).all()


def get_item_by_id(db_session: Session, item_id= int):
    '''根据id查询物品'''
    return db_session.query(models.Item).filter(models.Item.id == item_id).first()


def create_user_item(db_session: Session, item: schemas.ItemCreate, user_id: int):
    '''新增商品'''
    db_item = models.Item(**item.dict(), owner_id =user_id)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item


def update_item(db_session: Session, item: schemas.ItemUpdate, item_id: int):
    '''修改商品信息'''
    db_item= db_session.query(models.Item).filter(models.Item.id == item_id).first()
    item_dict = item.dict()
    db_item.title = item_dict['title']
    db_item.description = item_dict['description']
    db_item.owner_id = item_dict['owner_id']
    db_session.commit()
    db_session.refresh(db_item)
    return db_item


def get_files(db_session: Session):
    '''查询文件外链'''
    return db_session.query(models.File).order_by(models.File.id.desc()).all()


def create_file(db_session: Session, url: str):
    '''新增文件外链'''
    db_file = db_session.query(models.File).filter(models.File.url == url).first()
    if not db_file:
        new_file = models.File(url = url)
        db_session.add(new_file)
        db_session.commit()
        db_session.refresh(new_file)
    return new_file
