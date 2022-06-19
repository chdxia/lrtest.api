from urllib.request import url2pathname
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import uuid
from . import models, schemas
from ..utils.common import Common


# 根据id查询用户
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 根据邮箱查询用户（验证邮箱是否已存在）
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 查询用户
def get_users(
    db: Session,
    name: str|None=None,
    email: str|None=None,
    access_token: str|None=None,
    role: int|None=None,
    status: bool|None=None,
    sort: str|None = '+create_time'
):
    return db.query(models.User).filter(
        or_(models.User.name.like(f'%{name}%'), name == None),
        or_(models.User.email.like(f'%{email}%'), email == None),
        or_(models.User.access_token == access_token, access_token == None),
        or_(models.User.role == role, role == None),
        or_(models.User.status == status, status == None)
    ).order_by(
        and_(models.User.create_time.asc(), sort == '+create_time'),
        and_(models.User.create_time.desc(), sort == '-create_time'),
        and_(models.User.update_time.asc(), sort == '+update_time'),
        and_(models.User.update_time.desc(), sort == '-update_time')
    ).all()


# 新增用户
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name= user.name,
        email= user.email,
        password= Common.str_to_sha256(user.password),
        role=user.role,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 修改用户
def update_user(db: Session, user:schemas.UserUpdate, user_id):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    user_dict = user.dict()
    db_user.name = user_dict['name']
    db_user.email = user_dict['email']
    if user_dict['password'] :
        db_user.password = Common.str_to_sha256(user_dict['password'])
    db_user.role = user_dict['role']
    db_user.status = user_dict['status']
    db.commit()
    db.refresh(db_user)
    return db_user


# 删除用户
def delete_user(db: Session, user_id):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


# 更新token
def update_token(db: Session, user_id: int|None=None, access_token: str|None=None):
    # 传入user_id时，更新该用户的token
    if user_id:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        token = uuid.uuid4()
        db_user.access_token = token
        db.commit()
        db.refresh(db_user)
        return token
    # 没有传入user_id，且传入token时，删除该token值（此处暂未考虑token重复）
    elif access_token:
        db_user = db.query(models.User).filter(models.User.access_token == access_token).first()
        if db_user:
            db_user.access_token = None
            db.commit()
            db.refresh(db_user)


# 查询物品
def get_items(db: Session, user_id: int|None=None, title: str|None=None, description: str|None=None, skip: int =0, limit: int =10):
    return db.query(models.Item).filter(
        or_(models.Item.owner_id == user_id, user_id == None),
        or_(models.Item.title.like(f'%{title}%'), title == None),
        or_(models.Item.description.like(f'%{description}%'), description == None)
    ).offset(skip).limit(limit).all()


# 根据id查询物品
def get_item_by_id(db: Session, item_id= int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# 新增商品
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id =user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 修改商品信息
def update_item(db: Session, item: schemas.ItemUpdate, item_id: int):
    db_item= db.query(models.Item).filter(models.Item.id == item_id).first()
    item_dict = item.dict()
    db_item.title = item_dict['title']
    db_item.description = item_dict['description']
    db_item.owner_id = item_dict['owner_id']
    db.commit()
    db.refresh(db_item)
    return db_item


# 查询文件外链
def get_files(db: Session):
    return db.query(models.File).order_by(models.File.id.desc()).all()


# 新增文件外链
def create_file(db: Session, url: str):
    db_file = db.query(models.File).filter(models.File.url == url).first()
    if not db_file:
        new_file = models.File(url = url)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        return new_file