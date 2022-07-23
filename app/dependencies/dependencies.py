from fastapi import HTTPException, Header
from ..crud import user_crud, role_crud


class RoleDepends:
    def __init__(self):
        self.db_roles = {}
        self.roles_key = []


    def __call__(self, *roles):
        async def get_token_header(X_Token: str = Header(...)):
            self.roles_key = roles
            for item in role_crud.get_roles():
                self.db_roles[item.role_name] = item.id
            roles_value = [self.db_roles[item] for item in self.roles_key]
            db_user = user_crud.get_user(access_token=X_Token)
            if X_Token == '233456': # 万能token，正式环境请删除
                pass
            elif db_user is None: # X-Token无效
                raise HTTPException(status_code=400, detail='X-Token header invalid')
            elif not db_user.status: # 账号已停用
                raise HTTPException(status_code=400, detail='Account is disabled')
            elif len(self.roles_key) == 0: # roles参数为空时默认允许所有角色访问
                pass
            elif [item for item in list(map(lambda item: item.role_id, role_crud.get_user(user_id=db_user.id))) if item in roles_value]: # 允许roles参数中的角色访问（当前用户的角色与roles存在交集，则可以访问）
                pass
            elif self.db_roles['admin'] in list(map(lambda item: item.role_id, role_crud.get_user_role(user_id=db_user.id))): # 默认允许admin访问（roles参数中可以省略admin）
                pass
            else:
                raise HTTPException(status_code=401, detail='Permission denied')
        return get_token_header
