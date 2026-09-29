"""
数据库实体模型
"""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Admin(Base):
    """管理员表"""

    __tablename__ = "t_admin"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50))
    avatar: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class User(Base):
    """用户表"""

    __tablename__ = "t_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50))
    avatar: Mapped[str | None] = mapped_column(String(255))
    gender: Mapped[int | None] = mapped_column(Integer, default=1)
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[int | None] = mapped_column(Integer, default=1)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Category(Base):
    """相册分类表"""

    __tablename__ = "t_category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sort_num: Mapped[int | None] = mapped_column(Integer, default=0)
    remark: Mapped[str | None] = mapped_column(String(255))
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Album(Base):
    """相册表"""

    __tablename__ = "t_album"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category_id: Mapped[int | None] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cover: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(500))
    is_public: Mapped[int | None] = mapped_column(Integer, default=1)
    photo_count: Mapped[int | None] = mapped_column(Integer, default=0)
    view_count: Mapped[int | None] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Photo(Base):
    """照片表"""

    __tablename__ = "t_photo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    album_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str | None] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(BigInteger, default=0)
    view_count: Mapped[int | None] = mapped_column(Integer, default=0)
    like_count: Mapped[int | None] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Comment(Base):
    """评论表"""

    __tablename__ = "t_comment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    photo_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[int | None] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class PhotoLike(Base):
    """点赞表"""

    __tablename__ = "t_like"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    photo_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Favorite(Base):
    """收藏表"""

    __tablename__ = "t_favorite"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    photo_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class Notice(Base):
    """公告表"""

    __tablename__ = "t_notice"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    admin_id: Mapped[int | None] = mapped_column(BigInteger)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class OperLog(Base):
    """操作日志表"""

    __tablename__ = "t_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_type: Mapped[str | None] = mapped_column(String(20))
    user_id: Mapped[int | None] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(50))
    operation: Mapped[str | None] = mapped_column(String(200))
    ip: Mapped[str | None] = mapped_column(String(50))
    create_time: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())
