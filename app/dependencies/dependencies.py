from fastapi import HTTPException, Header
from ..models.models import User, Role, UserRole


class RoleDepends:
    def __init__(self):
        self.db_roles = {}
        self.roles_key = []


    def __call__(self, *roles):
        async def get_token_header(X_Token: str = Header(...)):
            self.roles_key = roles
            for item in await Role.all().values():
                self.db_roles[item['role_name']] = item['id']
            roles_value = [self.db_roles[item] for item in self.roles_key]
            db_user = await User.filter(access_token=X_Token).first()
            if X_Token == '233456': # 万能token，只在dev使用
                pass
            elif not db_user: # X-Token无效
                raise HTTPException(status_code=400, detail='X-Token header invalid')
            elif not db_user.status: # 账号已停用
                raise HTTPException(status_code=400, detail='账号已被禁用')
            elif len(self.roles_key) == 0: # roles参数为空时默认允许所有角色访问
                pass
            elif [item for item in list(map(lambda item: item['role_id'], await UserRole.filter(user_id=db_user.id).values())) if item in roles_value]: # 允许roles参数中的角色访问（当前用户的角色与roles存在交集，则可以访问）
                pass
            elif self.db_roles['admin'] in list(map(lambda item: item['role_id'], await UserRole.filter(user_id=db_user.id).values())): # 默认允许admin访问（roles参数中可以省略admin）
                pass
            else:
                raise HTTPException(status_code=401, detail='抱歉，权限不足')
        return get_token_header
