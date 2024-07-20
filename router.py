from fastapi import APIRouter
from apis import router_system, router_user

api_router = APIRouter()


api_router.include_router(router_system, prefix="/system", tags=["系统运行API"])
api_router.include_router(router_user, prefix="/user", tags=["用户API"])
