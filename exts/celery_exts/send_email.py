import asyncio
from datetime import timedelta

from celery.app.task import BaseTask
from db.redis_client import RedisClient
from exts.celery_exts import cele_app
from utils.random_helper import generate_num
from exts import logger
from utils.email_send_helper import EmailHelper
from asserts.template.email_tempalte.email_tempalte import (
    verify_email,
    reset_password_email,
)


async def send_email_async(email):
    code = await generate_num()
    html_body = verify_email.format(code=code)
    redis_client = await RedisClient.get_redis()
    logger.info(f"email verify code: {code}, email: {email}")
    await redis_client.set(f"email_verify:{email}", code, ex=timedelta(minutes=5))
    await EmailHelper.main_async(
        to_address=email, html_body=html_body, subject="Email Verification"
    )


async def send_email_reset_password(email, reset_link):
    html_body = reset_password_email.format(href=reset_link)
    logger.info(f"email reset password: {email}, reset_link: {reset_link}")
    await EmailHelper.main_async(
        to_address=email, html_body=html_body, subject="Reset Your Password"
    )


@cele_app.task(bind=True, base=BaseTask)
def send_email(self, email, reset_link=""):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            logger.info("event loop is closed, create new")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if reset_link:
            loop.run_until_complete(send_email_reset_password(email, reset_link))
        else:
            loop.run_until_complete(send_email_async(email))
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
    return "send email success"
