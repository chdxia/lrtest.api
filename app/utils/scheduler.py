from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ProcessPoolExecutor


# 任务配置
interval_task = {
    "jobstores": {
        'default': MemoryJobStore()
    },
    "executors": {
        'default': ProcessPoolExecutor(10)
    },
    "job_defaults": {
        'coalesce': False,
        'max_instances': 3
    }
}

scheduler = AsyncIOScheduler(**interval_task)


async def register_scheduler(app: FastAPI):
    scheduler.start()
