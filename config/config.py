from functools import lru_cache
import os
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, dotenv_values
from datetime import timedelta

env_path = find_dotenv()
env_config = dotenv_values()


class Settings(BaseSettings):

    # 项目相关配置
    PROJECT_NAME: str = env_config.get("PROJECT_NAME", "FastAPI Template")
    PROJECT_ENV: str = env_config.get("PROJECT_ENV", "LOCAL")
    DEBUG: bool = env_config.get("DEBUG", True)
    PROJECT_PORT: int = env_config.get("PROJECT_PORT", 5571)
    PROJECT_ROOT_NAME: str = env_config.get("PROJECT_ROOT_NAME", "test")

    # 定义连接异步引擎数据库的URL地址
    ASYNC_DB_DRIVER: str = "mysql+aiomysql"
    DB_USER: str = env_config.get("MYSQL_USER", "root")
    DB_HOST: str = env_config.get("MYSQL_HOST", "localhost")
    DB_PORT: int = env_config.get("MYSQL_PORT", 3306)
    DB_PASSWORD: str = env_config.get("MYSQL_PASSWORD", "123456")
    DB_DATABASE: str = env_config.get("MYSQL_DATABASE", "test")
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 60
    DB_MAX_OVERFLOW: int = 10
    DATABASE_URI: str = (
        f"{ASYNC_DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8"
    )
    # 定义TOEKN的签名信息值
    TOKEN_SIGN_SECRET: str = "ZcjT6Rcp1yIFQoS7"

    # openssl rand -hex 32
    SECRET: str = "66e47086b1b9f15aa02001f86a3e732ee14ff6a59e389ebb5040e01eed7627d9"
    ALGORITHM: str = "HS256"
    JWT_ACCESS_EXP: timedelta = timedelta(days=1)
    JWT_REFRESH_EXP: timedelta = timedelta(days=36)

    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")
    CABIN_STATIC_DIR: str = os.path.join(BASE_DIR, "static/cabin_static")

    if os.path.exists(CABIN_STATIC_DIR) is False:
        os.makedirs(CABIN_STATIC_DIR)

    # Sqlite 配置
    # sqllite数据库地址
    SQLITE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/{PROJECT_ROOT_NAME}.db"
    # redis配置
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD", "")
    REDIS_DB: int = os.environ.get("REDIS_DB", 0)
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)
    REDIS_URL: str = (
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    )
    REDIS_TIMEOUT: int = 5  # redis连接超时时间

    # 重置密码
    RESET_PASSWORD_SECRET: str = os.environ.get("RESET_PASSWORD_SECRET", "")
    RESET_PASSWORD_URL: str = "127.0.0.1:3000"

    ## CELERY 配置
    CELERY_BACKEND_DB: str = env_config.get("CELERY_BACKEND_DB", 6)
    CELERY_BROKER_DB: str = env_config.get("CELERY_BROKER_DB", 5)

    # EMAIL
    EMAIL_SENDER: str = ""
    ALIBABA_CLOUD_ACCESS_KEY_ID: str = env_config.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    ALIBABA_CLOUD_ACCESS_KEY_SECRET: str = env_config.get(
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET", ""
    )


class LocalTzSetting(Settings):
    DB_DATABASE: str = "test"


@lru_cache()
def get_settings():
    if os.environ.get("PROJECT_ENV") == "LOCAL":
        print("当前环境为LOCAL")
        return LocalTzSetting()
    elif os.environ.get("PROJECT_ENV") == "ONLINE":
        print("env: ONLINE")
        return Settings()
    return Settings()


if __name__ == "__main__":
    print(get_settings().BASE_DIR)
    print(get_settings().LOG_DIR)
