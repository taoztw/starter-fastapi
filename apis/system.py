from fastapi import APIRouter
from exts.responses.json_response import Success
import threading
from exts import logger

router = APIRouter()


@router.get("/health")
async def get():
    logger.info("hello world")
    return Success()


@router.get("/threads")
async def threads():
    num_threads = threading.active_count()
    threads = threading.enumerate()

    thread_list = []
    for thread in threads:
        thread_name = thread.name
        thread_id = thread.ident
        is_alive = thread.is_alive()

        thread_list.append({"name": thread_name, "id": thread_id, "is_alive": is_alive})

    return Success(result={"num_threads": num_threads, "threads": thread_list})
