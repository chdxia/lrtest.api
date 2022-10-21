from datetime import datetime
from pydantic import BaseModel


# 新增任务
class TaskCreate(BaseModel):
    task_type: int
    task_name: str|None=None
    description: str|None=None
    status: int
    start_time: datetime|None=None
    plan_end_time: datetime|None=None
    actual_end_time: datetime|None=None
    users: list

# 修改任务
class UserUpdate(TaskCreate):
    pass

# 任务信息
class Task(BaseModel):
    id: int
    task_type: int
    task_name: str|None=None
    description: str|None=None
    users: list
    status: int
    start_time: datetime|None=None
    plan_end_time: datetime|None=None
    actual_end_time: datetime|None=None
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True

# 返回任务信息
class TaskResponse(BaseModel):
    code: int
    message: str
    data: Task

# 任务数量
class TotalTask(BaseModel):
    total: int
    tasks: list[Task]

# 返回用户信息
class TasksResponse(BaseModel):
    code: int
    message: str
    data: TotalTask
