from fastapi import Header, Depends
from sqlalchemy.orm import Session
from ..exception import ApiException
from ..crud import user_crud, role_crud
from ..database.mysql import get_mysql_db


class RoleDepends:
    def __init__(self):
        self.db_roles = {}
        self.roles_key = []


    def __call__(self, *roles):
        self.roles_key = roles
        async def get_token_header(X_Token: str = Header(...), db_session: Session=Depends(get_mysql_db)):
            for item in role_crud.get_roles(db_session):
                self.db_roles[item.role_name] = item.id
            roles_value = [self.db_roles[item] for item in self.roles_key]
            db_user = user_crud.get_users(db_session, access_token=X_Token)
            if len(db_user) == 0: # X-Token无效
                raise ApiException(status_code=400, content={"code": 40000, "message": "X-Token header invalid"})
            elif len(self.roles_key) == 0: # roles参数为空时默认允许所有角色访问
                pass
            elif [item.role for item in db_user] in roles_value: # 允许roles参数中的角色访问
                pass
            elif self.db_roles['admin'] in [item.role for item in db_user]: # 默认允许admin访问（roles参数中可以省略admin）
                pass
            else:
                raise ApiException(status_code=400, content={"code": 40000, "message": "permission denied"})
        return get_token_header
