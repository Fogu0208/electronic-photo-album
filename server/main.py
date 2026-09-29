"""
基于Python的电子相册管理系统 - 启动入口
"""
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.common.constants import TOKEN_PREFIX
from app.common.exceptions import BusinessException
from app.common.response import R
from app.config import settings
from app.routers import (
    album,
    auth,
    category,
    comment,
    file,
    interact,
    log,
    notice,
    photo,
    statistic,
    user,
)
from app.utils.jwt_util import JwtUtil
from app.utils.user_context import UserContext, UserInfo

app = FastAPI(title=settings.app_name)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 静态资源映射
os.makedirs(settings.upload_path, exist_ok=True)
app.mount("/uploads31", StaticFiles(directory=settings.upload_path), name="uploads31")

# 公开路径白名单
PUBLIC_EXACT = {
    "/api/auth/login",
    "/api/auth/register",
    "/api/notice/list",
}
PUBLIC_PREFIXES = (
    "/api/album/public/",
    "/api/photo/public/",
    "/uploads31/",
)


def is_public_path(path: str) -> bool:
    """判断是否公开路径"""
    if path in PUBLIC_EXACT:
        return True
    return any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """JWT认证中间件"""
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    if is_public_path(path):
        return await call_next(request)

    if not path.startswith("/api/"):
        return await call_next(request)

    header = request.headers.get("Authorization")
    if not header or not header.startswith(TOKEN_PREFIX):
        return JSONResponse(status_code=200, content=R.fail("未登录或Token无效", 401))

    token = header[len(TOKEN_PREFIX):]
    if not JwtUtil.validate_token(token):
        return JSONResponse(status_code=200, content=R.fail("Token已过期，请重新登录", 401))

    try:
        claims = JwtUtil.parse_token(token)
        user_id = claims.get("userId")
        if isinstance(user_id, str):
            user_id = int(user_id)
        UserContext.set(UserInfo(
            user_id=int(user_id),
            username=claims.get("username"),
            role=claims.get("role"),
        ))
        response = await call_next(request)
        return response
    finally:
        UserContext.clear()


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """业务异常处理"""
    return JSONResponse(status_code=200, content=R.fail(exc.message, exc.code))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    import traceback
    traceback.print_exc()
    return JSONResponse(status_code=200, content=R.fail(f"系统异常: {str(exc)}"))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """参数校验异常处理"""
    return JSONResponse(status_code=200, content=R.fail("参数错误"))


# 注册路由
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(album.router)
app.include_router(photo.router)
app.include_router(comment.router)
app.include_router(interact.router)
app.include_router(notice.router)
app.include_router(log.router)
app.include_router(statistic.router)
app.include_router(file.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
