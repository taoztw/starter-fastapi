from functools import lru_cache
import os
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, dotenv_values
from datetime import timedelta

env_path = find_dotenv()
env_config = dotenv_values()


class Settings(BaseSettings):

    # 项目相关配置

    # 项目名称
    PROJECT_NAME: str = env_config.get("PROJECT_NAME", "FastAPI Template")
    # 项目环境，不同环境有不同的启动方式
    PROJECT_ENV: str = env_config.get("PROJECT_ENV", "LOCAL")
    DEBUG: bool = env_config.get("DEBUG", True)
    # 端口号
    PROJECT_PORT: int = env_config.get("PROJECT_PORT", 5571)
    # 项目根API路径
    PROJECT_ROOT_NAME: str = env_config.get("PROJECT_ROOT_NAME", "test")

    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")


@lru_cache()
def get_settings():
    return Settings()
