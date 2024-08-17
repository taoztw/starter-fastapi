from fastapi import APIRouter
from apis import router_system, router_user, router_hero

api_router = APIRouter()


api_router.include_router(router_system, prefix="/system", tags=["系统运行API"])
api_router.include_router(router_user, prefix="/user", tags=["用户API"])
api_router.include_router(router_hero, prefix="/learn", tags=["hero 官网文档API"])
