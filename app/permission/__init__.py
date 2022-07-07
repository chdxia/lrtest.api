from .dependencies import RoleDepends


role_depends = RoleDepends()
'''
*roles

参数示例:admin,editor

tips:

=>向参数中的角色开放访问权限

=>默认允许admin，所以admin可以省略

=>参数为空时，默认允许已存在的所有角色访问
'''
