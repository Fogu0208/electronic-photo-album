"""
IP地址工具类
"""
from starlette.requests import Request


class IpUtil:
    """IP工具"""

    @staticmethod
    def get_ip(request: Request) -> str:
        """获取客户端IP地址"""
        ip = request.headers.get("X-Forwarded-For")
        if not ip or ip.lower() == "unknown":
            ip = request.headers.get("Proxy-Client-IP")
        if not ip or ip.lower() == "unknown":
            ip = request.headers.get("WL-Proxy-Client-IP")
        if not ip or ip.lower() == "unknown":
            ip = request.client.host if request.client else "127.0.0.1"
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()
        return ip or "127.0.0.1"
