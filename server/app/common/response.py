"""
统一响应封装
"""
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageResult(BaseModel):
    """分页结果"""

    total: int
    records: List[Any]


class R(BaseModel, Generic[T]):
    """统一返回结果"""

    code: int = 200
    msg: str = "操作成功"
    data: Optional[T] = None

    @staticmethod
    def ok(data: Any = None) -> dict:
        """成功返回"""
        return {"code": 200, "msg": "操作成功", "data": data}

    @staticmethod
    def fail(msg: str, code: int = 500) -> dict:
        """失败返回"""
        return {"code": code, "msg": msg, "data": None}
