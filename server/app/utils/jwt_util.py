"""
JWT工具类
"""
from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


class JwtUtil:
    """JWT令牌工具"""

    @staticmethod
    def generate_token(user_id: int, username: str, role: str) -> str:
        """生成Token"""
        payload = {
            "userId": user_id,
            "username": username,
            "role": role,
            "sub": username,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(milliseconds=settings.jwt_expire_ms),
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    @staticmethod
    def parse_token(token: str) -> dict:
        """解析Token"""
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])

    @staticmethod
    def validate_token(token: str) -> bool:
        """验证Token是否有效"""
        try:
            payload = JwtUtil.parse_token(token)
            exp = payload.get("exp")
            if exp is None:
                return False
            if isinstance(exp, (int, float)):
                return datetime.fromtimestamp(exp, tz=timezone.utc) > datetime.now(timezone.utc)
            return True
        except Exception:
            return False
