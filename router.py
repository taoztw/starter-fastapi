from fastapi import APIRouter
from apis import router_system

api_router = APIRouter()


api_router.include_router(router_system, prefix="/system", tags=["系统运行API"])
