from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from tortoise.expressions import Q
from ..models.models import Task, UserTask, User
from ..schemas import task_schemas
from ..dependencies import role_depends
from ..utils import ignore_none


router = APIRouter(prefix='/tasks', tags=['任务'])


@router.get('', response_model=task_schemas.TasksResponse, summary='查询任务', dependencies=[Depends(role_depends())])
async def get_tasks(
    task_type: int|None=None,
    task_name: str|None=None,
    status: int|None=None,
    user_name: str|None=None,
    sort: str|None='-create_time',
    page: int|None=1,
    limit: int|None=10
):
    db_task = Task.filter(**ignore_none(
        task_type = task_type,
        task_name__contains = task_name,
        status = status,
        id__in = list(map(lambda item: item['task_id'], await UserTask.filter(user_id__in = list(map(lambda item: item['id'], await User.filter(user_name__contains = user_name)))).values())) if user_name else None
    )).order_by(sort)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": await db_task.count(),
            "tasks": await db_task.offset((page-1)*limit).limit(limit).prefetch_related('_users')
        }
    }


@router.post('', response_model=task_schemas.TaskResponse, summary='新增任务', dependencies=[Depends(role_depends())])
async def create_task(task: task_schemas.TaskCreate):
    # 创建任务
    db_task = await Task.create(
        task_type = task.task_type,
        task_name = task.task_name,
        description = task.description,
        status = task.status,
        start_time = task.start_time,
        plan_end_time = task.plan_end_time,
        actual_end_time = task.actual_end_time,
        create_time = datetime.now(),
        update_time = datetime.now()
    )
    # 任务、用户之间的绑定
    [await UserTask.create(task_id=db_task.id, user_id=item) for item in task.users if task.users]
    return {"code": 200, "message": "success", "data": await Task.filter(id=db_task.id).first().prefetch_related('_users')}
