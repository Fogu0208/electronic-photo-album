"""
用户上下文与操作日志
"""
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models.entities import OperLog
from app.utils.ip_util import IpUtil


@dataclass
class UserInfo:
    """当前登录用户信息"""

    user_id: int
    username: str
    role: str


_user_context: ContextVar[UserInfo | None] = ContextVar("user_context", default=None)


class UserContext:
    """用户上下文工具类"""

    @staticmethod
    def set(user: UserInfo) -> None:
        """设置当前用户"""
        _user_context.set(user)

    @staticmethod
    def get() -> UserInfo | None:
        """获取当前用户"""
        return _user_context.get()

    @staticmethod
    def get_user_id() -> int | None:
        """获取当前用户ID"""
        user = _user_context.get()
        return user.user_id if user else None

    @staticmethod
    def get_role() -> str | None:
        """获取当前用户角色"""
        user = _user_context.get()
        return user.role if user else None

    @staticmethod
    def clear() -> None:
        """清除上下文"""
        _user_context.set(None)


def write_oper_log(db: Session, request: Request, operation: str) -> None:
    """写入操作日志"""
    user = UserContext.get()
    if not user:
        return
    try:
        log = OperLog(
            user_type=user.role,
            user_id=user.user_id,
            username=user.username,
            operation=operation,
            ip=IpUtil.get_ip(request),
            create_time=datetime.now(),
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
