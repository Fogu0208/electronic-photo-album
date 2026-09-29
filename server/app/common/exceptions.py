"""
业务异常定义
"""


class BusinessException(Exception):
    """业务异常类"""

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(message)
