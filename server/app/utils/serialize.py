"""
序列化工具 - 将ORM对象转为camelCase字典
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import DeclarativeBase


def to_camel(snake_str: str) -> str:
    """蛇形转驼峰"""
    parts = snake_str.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def format_value(value: Any) -> Any:
    """格式化字段值"""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


def model_to_camel_dict(obj: Any, extra: dict | None = None) -> dict:
    """将ORM对象转为camelCase字典"""
    if obj is None:
        return {}
    result = {}
    if isinstance(obj, DeclarativeBase):
        for column in obj.__table__.columns:
            key = to_camel(column.name)
            value = getattr(obj, column.name)
            if key == "password":
                continue
            result[key] = format_value(value)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            camel_key = to_camel(key) if "_" in key else key
            result[camel_key] = format_value(value)
    if extra:
        for key, value in extra.items():
            result[key] = format_value(value)
    return result


def models_to_camel_list(items: list, extra_list: list[dict] | None = None) -> list:
    """批量转换ORM列表"""
    result = []
    for idx, item in enumerate(items):
        extra = extra_list[idx] if extra_list and idx < len(extra_list) else None
        result.append(model_to_camel_dict(item, extra))
    return result


def page_result(total: int, records: list) -> dict:
    """构建分页结果"""
    return {"total": total, "records": records}
