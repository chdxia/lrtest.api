from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import item_schemas


def get_items(db_session:Session, user_id:int|None=None, title:str|None=None, description:str|None=None):
    '''查询物品'''
    return db_session.query(models.Item).filter(
        or_(models.Item.owner_id == user_id, user_id is None),
        or_(models.Item.title.like(f'%{title}%'), title is None),
        or_(models.Item.description.like(f'%{description}%'), description is None)
    ).all()


def get_item_by_id(db_session: Session, item_id= int):
    '''根据id查询物品'''
    return db_session.query(models.Item).filter(models.Item.id == item_id).first()


def create_item_by_user(db_session: Session, item: item_schemas.ItemCreate, user_id: int):
    '''新增商品'''
    db_item = models.Item(**item.dict(), owner_id =user_id)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item


def update_item(db_session: Session, item: item_schemas.ItemUpdate, item_id: int):
    '''修改商品信息'''
    db_item= db_session.query(models.Item).filter(models.Item.id == item_id).first()
    item_dict = item.dict()
    db_item.title = item_dict['title']
    db_item.description = item_dict['description']
    db_item.owner_id = item_dict['owner_id']
    db_session.commit()
    db_session.refresh(db_item)
    return db_item
