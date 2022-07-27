from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True, index=True, description='用户id')
    account = fields.CharField(64, unique=True, description='账号')
    user_name = fields.CharField(64, null=True, description='用户名')
    email = fields.CharField(64, unique=True, description='用户邮箱')
    password = fields.CharField(64, null=True, description='用户密码')
    access_token = fields.CharField(64, null=True, description='账号token')
    status = fields.BooleanField(default=True, description='账号状态 True:启用 False:停用')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')
    user_role: fields.ReverseRelation['UserRole']
    user_task: fields.ReverseRelation['UserTask']
    class Meta:
        table = 'user'
        table_description = '用户表'
        

class Role(Model):
    id = fields.IntField(pk=True, index=True, description='角色id')
    role_name = fields.CharField(64, unique=True, description='角色名')
    user_role: fields.ReverseRelation['UserRole']
    class Meta:
        table = 'role'
        table_description = '角色表'


class UserRole(Model):
    id = fields.IntField(pk=True, index=True, description='id')
    user = fields.ForeignKeyField(model_name='models.User', related_name='user_role', on_delete=fields.CASCADE, to_field='id')
    role = fields.ForeignKeyField(model_name='models.Role', related_name='user_role', on_delete=fields.RESTRICT, to_field='id')
    class Meta:
        table = 'user_role'
        table_description = '用户角色关系表'


class Task(Model):
    id = fields.IntField(pk=True, index=True, description='任务id')
    task_type = fields.IntField(description='任务类型 1:项目任务 2:非项目任务')
    task_name = fields.CharField(64, null=True, description='任务名')
    description = fields.CharField(128, null=True, description='任务描述')
    status = fields.IntField(description='任务状态')
    plan_end_time = fields.DateField(description='预计结束时间')
    actual_end_time = fields.DatetimeField(null=True, description='实际结束时间')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')
    user_task: fields.ReverseRelation['UserTask']
    class Meta:
        table = 'task'
        table_description = '任务表'


class UserTask(Model):
    id = fields.IntField(pk=True, index=True, description='id')
    user = fields.ForeignKeyField(model_name='models.User', related_name='user_task', on_delete=fields.CASCADE, to_field='id')
    task = fields.ForeignKeyField(model_name='models.Task', related_name='user_task', on_delete=fields.CASCADE, to_field='id')
    class Meta:
        table = 'user_task'
        table_description = '用户任务关系表'
