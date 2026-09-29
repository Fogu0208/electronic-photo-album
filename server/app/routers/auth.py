"""
认证路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.constants import ROLE_ADMIN
from app.common.response import R
from app.database import get_db
from app.services.auth_service import AuthService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login")
def login(request: Request, params: dict, db: Session = Depends(get_db)):
    """登录接口"""
    username = params.get("username")
    password = params.get("password")
    role = params.get("role")
    if role == ROLE_ADMIN:
        data = AuthService.admin_login(db, username, password)
    else:
        data = AuthService.user_login(db, username, password)
    write_oper_log(db, request, "用户登录")
    return R.ok(data)


@router.post("/register")
def register(params: dict, db: Session = Depends(get_db)):
    """用户注册"""
    AuthService.register(db, params)
    return R.ok()


@router.get("/info")
def info(db: Session = Depends(get_db)):
    """获取当前用户信息"""
    return R.ok(AuthService.get_current_user(db))


@router.put("/password")
def update_password(params: dict, db: Session = Depends(get_db)):
    """修改密码"""
    AuthService.update_password(db, params.get("oldPassword"), params.get("newPassword"))
    return R.ok()


@router.put("/profile/admin")
def update_admin_profile(params: dict, db: Session = Depends(get_db)):
    """修改管理员个人资料"""
    AuthService.update_admin_profile(db, params)
    return R.ok()


@router.put("/profile/user")
def update_user_profile(params: dict, db: Session = Depends(get_db)):
    """修改用户个人资料"""
    AuthService.update_user_profile(db, params)
    return R.ok()
