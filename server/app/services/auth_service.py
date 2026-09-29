"""
认证服务
"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.constants import ROLE_ADMIN, ROLE_USER
from app.common.exceptions import BusinessException
from app.models.entities import Admin, User
from app.utils.jwt_util import JwtUtil
from app.utils.serialize import model_to_camel_dict
from app.utils.user_context import UserContext


class AuthService:
    """认证服务类"""

    @staticmethod
    def admin_login(db: Session, username: str, password: str) -> dict:
        """管理员登录"""
        admin = db.scalar(select(Admin).where(Admin.username == username))
        if not admin or password != admin.password:
            raise BusinessException("用户名或密码错误")
        token = JwtUtil.generate_token(admin.id, admin.username, ROLE_ADMIN)
        return {
            "token": token,
            "role": ROLE_ADMIN,
            "userInfo": model_to_camel_dict(admin),
        }

    @staticmethod
    def user_login(db: Session, username: str, password: str) -> dict:
        """用户登录"""
        user = db.scalar(select(User).where(User.username == username))
        if not user or password != user.password:
            raise BusinessException("用户名或密码错误")
        if user.status is not None and user.status == 0:
            raise BusinessException("账号已被禁用")
        token = JwtUtil.generate_token(user.id, user.username, ROLE_USER)
        return {
            "token": token,
            "role": ROLE_USER,
            "userInfo": model_to_camel_dict(user),
        }

    @staticmethod
    def register(db: Session, user_data: dict) -> None:
        """用户注册"""
        username = user_data.get("username")
        count = db.scalar(select(User).where(User.username == username))
        if count:
            raise BusinessException("用户名已存在")
        user = User(
            username=username,
            password=user_data.get("password"),
            nickname=user_data.get("nickname"),
            phone=user_data.get("phone"),
            status=1,
            gender=1,
            avatar="/uploads31/avatar/default.jpg",
            create_time=datetime.now(),
        )
        db.add(user)
        db.commit()

    @staticmethod
    def get_current_user(db: Session) -> dict:
        """获取当前登录用户信息"""
        ctx = UserContext.get()
        if not ctx:
            raise BusinessException("未登录", 401)
        if ctx.role == ROLE_ADMIN:
            admin = db.get(Admin, ctx.user_id)
            if not admin:
                raise BusinessException("用户不存在")
            return model_to_camel_dict(admin)
        user = db.get(User, ctx.user_id)
        if not user:
            raise BusinessException("用户不存在")
        return model_to_camel_dict(user)

    @staticmethod
    def update_password(db: Session, old_password: str, new_password: str) -> None:
        """修改密码"""
        ctx = UserContext.get()
        if ctx.role == ROLE_ADMIN:
            admin = db.get(Admin, ctx.user_id)
            if not admin or old_password != admin.password:
                raise BusinessException("原密码错误")
            admin.password = new_password
            db.commit()
            return
        user = db.get(User, ctx.user_id)
        if not user or old_password != user.password:
            raise BusinessException("原密码错误")
        user.password = new_password
        db.commit()

    @staticmethod
    def update_admin_profile(db: Session, profile: dict) -> None:
        """修改管理员个人资料"""
        ctx = UserContext.get()
        admin = db.get(Admin, ctx.user_id)
        if not admin:
            raise BusinessException("用户不存在")
        for field in ("nickname", "avatar", "phone", "email"):
            if field in profile and profile[field] is not None:
                setattr(admin, field, profile[field])
        db.commit()

    @staticmethod
    def update_user_profile(db: Session, profile: dict) -> None:
        """修改用户个人资料"""
        ctx = UserContext.get()
        user = db.get(User, ctx.user_id)
        if not user:
            raise BusinessException("用户不存在")
        for field in ("nickname", "avatar", "phone", "email", "gender"):
            if field in profile and profile[field] is not None:
                setattr(user, field, profile[field])
        db.commit()
