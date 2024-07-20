from loguru import logger
import os
from config import settings
from sys import stdout

# 定义info_log文件名称
log_file_path = os.path.join(settings.LOG_DIR, "info_{time:YYYYMMDD}.log")
# 定义err_log文件名称
err_log_file_path = os.path.join(settings.LOG_DIR, "error_{time:YYYYMMDD}.log")

def safe_format_record(record):
    request_id = record["extra"].get("request_id", "-")
    record["extra"]["request_id"] = request_id
    return (
        f"<green>{record['time']:%Y-%m-%d %H:%M:%S.%f%z}  request_id:{request_id}</green> | thread_id:{record['thread'].id} thread_name:{record['thread'].name} | {record['level']} | {record['message']}\n"
    )

# 设置 stdout 日志 handler
logger.configure(
    handlers=[
        {"sink": stdout, "format": safe_format_record}
    ]
)

# 添加其他日志 handler
logger.add(
    err_log_file_path,
    format=safe_format_record,
    rotation="00:00",
    encoding="utf-8",
    level="ERROR",
    enqueue=True,
)
logger.add(
    log_file_path,
    format=safe_format_record,
    rotation="00:00",
    encoding="utf-8",
    level="INFO",
    enqueue=True,
)  # Automatically rotate logs