from typing import Any
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # 通用的字段
    id: Any
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    is_delete = Column(Boolean, default=False, comment="逻辑删除:0=未删除,1=删除")
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        import re
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()