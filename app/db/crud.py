from sqlalchemy.orm import Session
from . import models, schemas
from urllib import parse


# 根据id查询用户信息
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 根据邮箱查询用户信息
def get_user_by_email(db: Session, email: str, skip: int= 0, limit: int= 10):
    return db.query(models.User).filter(models.User.email == email).offset(skip).limit(limit).all()


# 获取用户信息
def get_users(db: Session, skip: int= 0, limit: int= 10):
    return db.query(models.User).offset(skip).limit(limit).all()


# 新增用户
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email= user.email, password= fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 修改用户
def update_user(db: Session, user:schemas.UserUpdate, user_id):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    user_dict = user.dict()
    db_user.email = user_dict['email']
    db_user.password = user_dict['password']
    db_user.is_active = user_dict['is_active']
    db.commit()
    db.refresh(db_user)
    return db_user


# 获取商品信息
def get_items(db: Session, skip: int =0, limit: int =10):
    return db.query(models.Item).offset(skip).limit(limit).all()


# 根据id查询商品信息
def get_item_by_id(db: Session, item_id= int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# 根据用户id查询商品信息
def get_items_by_userid(db: Session, user_id= int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


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