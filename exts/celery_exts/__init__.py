from celery import Celery, Task
from exts import logger
from config import settings
from exts.celery_exts import config as celery_config


include_task = [
    "exts.celery_exts.send_email",
]

cele_app = Celery(
    "demo",
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_BROKER_DB}",
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_BACKEND_DB}",
    include=include_task,
)

cele_app.conf.timezone = "Asia/Shanghai"  # 时区
cele_app.conf.enable_utc = False  # 是否使用UTC
cele_app.conf.broker_connection_retry_on_startup = True
cele_app.config_from_object(celery_config)


class BaseTask(Task):

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"任务成功{retval}, {task_id}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info(f"任务失败")
