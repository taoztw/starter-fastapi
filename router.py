from fastapi import APIRouter
from apis import (
    router_system,
    router_user,
    router_hero,
    router_wild_oasis_settings,
    router_wild_oasis_guests,
    router_wild_oasis_cabins,
    router_wild_oasis_bookings,
    router_wild_oasis_file,
)

api_router = APIRouter()


api_router.include_router(router_system, prefix="/system", tags=["系统运行API"])
api_router.include_router(router_user, prefix="/user", tags=["用户API"])
api_router.include_router(router_hero, prefix="/learn", tags=["hero 官网文档API"])

# wil oasis路由
api_router.include_router(
    router_wild_oasis_settings, prefix="/wild_oasis", tags=["Wild Oasis - Setting"]
)
api_router.include_router(
    router_wild_oasis_guests, prefix="/wild_oasis", tags=["Wild Oasis - Guests"]
)
api_router.include_router(
    router_wild_oasis_cabins, prefix="/wild_oasis", tags=["Wild Oasis - Cabins"]
)
api_router.include_router(
    router_wild_oasis_bookings, prefix="/wild_oasis", tags=["Wild Oasis - Bookings"]
)
api_router.include_router(
    router_wild_oasis_file, prefix="/wild_oasis", tags=["Wild Oasis - File"]
)
