import traceback

from fastapi import APIRouter, Body, Depends

from dependencies.auth_dep import get_user
from .schemas import UserPost, UserLogin, VerifyEmailCode, SendEmail, ResetPassword
from utils.passlib_hepler import PasslibHelper
from utils.auth_helper import (
    authorize,
    create_access_token,
    create_refresh_token,
)
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db_dep import get_db_context
from .service import UserServices
from exts.responses.json_response import Fail, Success, BadRequestException
from exts.celery_exts import send_email
from exts import logger
from db.redis_client import RedisClient
from itsdangerous import URLSafeTimedSerializer
from config import settings
from dependencies import auth_dep

serializer = URLSafeTimedSerializer(settings.RESET_PASSWORD_SECRET)

router = APIRouter()


@router.post("/register")
async def register(body: UserPost, db_session: AsyncSession = Depends(get_db_context)):
    logger.info(f"register user: {body.model_dump()}")
    body.password_hash = PasslibHelper.hash_password(body.password_hash)
    existing = await UserServices.is_email_exist(db_session, body.email)
    if existing:
        return Fail(message="Email already exists")
    # 创建用户
    user_obj = await UserServices.create_user(db_session, **body.model_dump())
    return Success(
        http_status_code=201, result={"user_id": user_obj.id, "email": user_obj.email}
    )


@router.post("/login")
async def login(body: UserLogin, db_session: AsyncSession = Depends(get_db_context)):
    user = await UserServices.get_user_by_email(db_session, body.email)
    if not user:
        return Fail(message="User not found")
    # 检验是否密码匹配
    if not PasslibHelper.verity_password(body.password, user.password_hash):
        return Fail(message="Invalid Account or Password")
    # 创建jwt access token
    access_token = create_access_token({"email": user.email, "id": user.id})
    # 创建jwt refresh token
    refresh_token = create_refresh_token({"email": user.email, "id": user.id})
    # 存储refresh token
    await UserServices.update_refresh_token(db_session, user.email, refresh_token)
    return Success(
        message="login successful",
        result={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
        },
    )


@router.post("/refresh_token")
async def refresh(token_data: dict = Depends(authorize)):
    return Success(result=token_data)


@router.get("/info")
async def info(user=Depends(get_user)):
    return Success(result={"id": user.id, "email": user.email})


@router.post("/email/send", summary="发送邮箱验证码")
async def send(body: SendEmail):
    send_email.send_email.apply_async(args=(body.email,), retry=False)
    return Success(message="Email verification link sent")


@router.post("/email/verify", summary="验证用户输入的验证码")
async def verify(body: VerifyEmailCode):
    redis_client = await RedisClient.get_redis()
    code = await redis_client.get(f"email_verify:{body.email}")
    logger.info(f"verify email code: {code}")
    if code is None:
        return BadRequestException(
            message="Verification code has expired or does not exist"
        )

    if code != body.code:
        return BadRequestException(message="Invalid verification code")
    return Success(message="Email verified")


@router.post("/email/password/reset", summary="发送重置密码邮件")
async def email_send_reset_password(body: SendEmail):
    # 给用户邮箱发送一条重置密码的邮件
    token = serializer.dumps(body.email, salt=settings.RESET_PASSWORD_SECRET)
    reset_link = f"http://{settings.RESET_PASSWORD_URL}/reset/pwd?token={token}"
    send_email.send_email.apply_async(args=(body.email, reset_link), retry=False)


@router.post("/password/reset", summary="提交重置密码结果")
async def reset_password(
    body: ResetPassword, db_session: AsyncSession = Depends(get_db_context)
):
    # 验证token是否在有效期内
    try:
        email = serializer.loads(
            body.reset_token, salt=settings.RESET_PASSWORD_SECRET, max_age=3600 * 24
        )  # 24小时有效
        logger.info(f"当前重置密码的邮箱: {email}")
        # 从数据库中查看email是否存在，如果存在则更新密码，否则报错
        db_user = await UserServices.get_user_by_email(db_session, email)
        if not db_user:
            return BadRequestException(message="Invalid or expired token")
        # 更新密码
        password_hash = PasslibHelper.hash_password(body.new_password)
        await UserServices.reset_password(db_session, email, password_hash)
        return Success(message="Password reset successfully")
    except Exception as e:
        logger.warning(f"重置密码失败: {str(e)}, {traceback.format_exc()}")
        return BadRequestException(message="Invalid or expired token")
