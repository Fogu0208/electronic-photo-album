"""
用户及业务管理服务
"""
from datetime import datetime

from sqlalchemy import func, or_, select, text
from sqlalchemy.orm import Session

from app.common.constants import ROLE_ADMIN
from app.common.exceptions import BusinessException
from app.models.entities import (
    Album,
    Category,
    Comment,
    Favorite,
    Notice,
    OperLog,
    Photo,
    PhotoLike,
    User,
)
from app.utils.serialize import format_value, model_to_camel_dict, page_result
from app.utils.user_context import UserContext


class ManageService:
    """业务管理服务类"""

    # ---------- 用户管理 ----------
    @staticmethod
    def page_users(db: Session, page_num: int, page_size: int, username: str | None) -> dict:
        """分页查询用户"""
        query = select(User)
        if username:
            query = query.where(or_(User.username.like(f"%{username}%"), User.nickname.like(f"%{username}%")))
        query = query.order_by(User.create_time.desc())
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        records = db.scalars(query.offset((page_num - 1) * page_size).limit(page_size)).all()
        return page_result(total or 0, [model_to_camel_dict(r) for r in records])

    @staticmethod
    def add_user(db: Session, data: dict) -> None:
        """新增用户"""
        exists = db.scalar(select(User).where(User.username == data.get("username")))
        if exists:
            raise BusinessException("用户名已存在")
        gender = data.get("gender")
        if gender is None or gender == 0:
            gender = 1
        user = User(
            username=data.get("username"),
            password=data.get("password"),
            nickname=data.get("nickname"),
            phone=data.get("phone"),
            email=data.get("email"),
            gender=gender,
            status=data.get("status", 1),
            create_time=datetime.now(),
        )
        db.add(user)
        db.commit()

    @staticmethod
    def update_user(db: Session, data: dict) -> None:
        """修改用户"""
        user = db.get(User, data.get("id"))
        if not user:
            raise BusinessException("用户不存在")
        for field in ("nickname", "phone", "email", "gender", "status"):
            if field in data and data[field] is not None:
                setattr(user, field, data[field])
        db.commit()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """删除用户"""
        user = db.get(User, user_id)
        if user:
            db.delete(user)
            db.commit()

    # ---------- 分类管理 ----------
    @staticmethod
    def page_categories(db: Session, page_num: int, page_size: int, name: str | None) -> dict:
        """分页查询分类"""
        query = select(Category)
        if name:
            query = query.where(Category.name.like(f"%{name}%"))
        query = query.order_by(Category.sort_num.asc())
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        records = db.scalars(query.offset((page_num - 1) * page_size).limit(page_size)).all()
        return page_result(total or 0, [model_to_camel_dict(r) for r in records])

    @staticmethod
    def list_categories(db: Session) -> list:
        """获取所有分类"""
        records = db.scalars(select(Category).order_by(Category.sort_num.asc())).all()
        return [model_to_camel_dict(r) for r in records]

    @staticmethod
    def add_category(db: Session, data: dict) -> None:
        """新增分类"""
        category = Category(
            name=data.get("name"),
            sort_num=data.get("sortNum", data.get("sort_num", 0)),
            remark=data.get("remark"),
            create_time=datetime.now(),
        )
        db.add(category)
        db.commit()

    @staticmethod
    def update_category(db: Session, data: dict) -> None:
        """修改分类"""
        category = db.get(Category, data.get("id"))
        if not category:
            raise BusinessException("分类不存在")
        for field, attr in (("name", "name"), ("sortNum", "sort_num"), ("sort_num", "sort_num"), ("remark", "remark")):
            if field in data and data[field] is not None:
                setattr(category, attr, data[field])
        db.commit()

    @staticmethod
    def delete_category(db: Session, category_id: int) -> None:
        """删除分类"""
        category = db.get(Category, category_id)
        if category:
            db.delete(category)
            db.commit()

    # ---------- 相册管理 ----------
    @staticmethod
    def _album_row_to_dict(row) -> dict:
        """相册联表行转字典"""
        return {
            "id": row.id,
            "userId": row.user_id,
            "categoryId": row.category_id,
            "name": row.name,
            "cover": row.cover,
            "description": row.description,
            "isPublic": row.is_public,
            "photoCount": row.photo_count,
            "viewCount": row.view_count,
            "createTime": format_value(row.create_time),
            "username": row.username,
            "categoryName": row.category_name,
        }

    @staticmethod
    def page_albums(
        db: Session,
        page_num: int,
        page_size: int,
        name: str | None,
        user_id: int | None,
        is_public: int | None,
    ) -> dict:
        """分页查询相册"""
        conditions = ["1=1"]
        params: dict = {}
        if name:
            conditions.append("a.name LIKE :name")
            params["name"] = f"%{name}%"
        if user_id is not None:
            conditions.append("a.user_id = :user_id")
            params["user_id"] = user_id
        if is_public is not None:
            conditions.append("a.is_public = :is_public")
            params["is_public"] = is_public
        where_sql = " AND ".join(conditions)
        count_sql = text(f"SELECT COUNT(*) FROM t_album a WHERE {where_sql}")
        total = db.scalar(count_sql, params) or 0
        query_sql = text(
            f"SELECT a.*, u.nickname AS username, c.name AS category_name "
            f"FROM t_album a LEFT JOIN t_user u ON a.user_id = u.id "
            f"LEFT JOIN t_category c ON a.category_id = c.id "
            f"WHERE {where_sql} ORDER BY a.create_time DESC "
            f"LIMIT :offset, :limit"
        )
        params["offset"] = (page_num - 1) * page_size
        params["limit"] = page_size
        rows = db.execute(query_sql, params).fetchall()
        records = [ManageService._album_row_to_dict(row) for row in rows]
        return page_result(total, records)

    @staticmethod
    def add_album(db: Session, data: dict) -> None:
        """新增相册"""
        user_id = data.get("userId") or data.get("user_id") or UserContext.get_user_id()
        album = Album(
            user_id=user_id,
            category_id=data.get("categoryId") or data.get("category_id"),
            name=data.get("name"),
            cover=data.get("cover"),
            description=data.get("description"),
            is_public=data.get("isPublic", data.get("is_public", 1)),
            photo_count=0,
            view_count=0,
            create_time=datetime.now(),
        )
        db.add(album)
        db.commit()

    @staticmethod
    def update_album(db: Session, data: dict) -> None:
        """修改相册"""
        album_id = data.get("id")
        if not album_id:
            raise BusinessException("相册ID不能为空")
        existing = db.get(Album, album_id)
        if not existing:
            raise BusinessException("相册不存在")
        current_user_id = UserContext.get_user_id()
        role = UserContext.get_role()
        if role != ROLE_ADMIN and current_user_id != existing.user_id:
            raise BusinessException("无权修改该相册")
        name = data.get("name")
        if name is not None and str(name).strip() == "":
            raise BusinessException("相册名称不能为空")
        for field, attr in (
            ("name", "name"),
            ("cover", "cover"),
            ("description", "description"),
            ("isPublic", "is_public"),
            ("is_public", "is_public"),
            ("categoryId", "category_id"),
            ("category_id", "category_id"),
        ):
            if field in data and data[field] is not None:
                setattr(existing, attr, data[field])
        db.commit()

    @staticmethod
    def delete_album(db: Session, album_id: int) -> None:
        """删除相册"""
        album = db.get(Album, album_id)
        if not album:
            raise BusinessException("相册不存在")
        current_user_id = UserContext.get_user_id()
        role = UserContext.get_role()
        if role != ROLE_ADMIN and current_user_id != album.user_id:
            raise BusinessException("无权删除该相册")
        photo_count = db.scalar(select(func.count()).select_from(Photo).where(Photo.album_id == album_id))
        if photo_count and photo_count > 0:
            raise BusinessException("相册内还有照片，请先删除全部照片后再删除相册")
        db.delete(album)
        db.commit()

    # ---------- 照片管理 ----------
    @staticmethod
    def _photo_row_to_dict(row, liked: bool = False, favorited: bool = False) -> dict:
        """照片联表行转字典"""
        return {
            "id": row.id,
            "albumId": row.album_id,
            "userId": row.user_id,
            "name": row.name,
            "url": row.url,
            "description": row.description,
            "fileSize": row.file_size,
            "viewCount": row.view_count,
            "likeCount": row.like_count,
            "createTime": format_value(row.create_time),
            "username": getattr(row, "username", None),
            "albumName": getattr(row, "album_name", None),
            "liked": liked,
            "favorited": favorited,
        }

    @staticmethod
    def _fill_photo_status(db: Session, photo_id: int, user_id: int | None) -> tuple[bool, bool]:
        """填充照片点赞收藏状态"""
        if not user_id:
            return False, False
        liked = db.scalar(
            select(func.count()).select_from(PhotoLike).where(
                PhotoLike.photo_id == photo_id, PhotoLike.user_id == user_id
            )
        )
        favorited = db.scalar(
            select(func.count()).select_from(Favorite).where(
                Favorite.photo_id == photo_id, Favorite.user_id == user_id
            )
        )
        return (liked or 0) > 0, (favorited or 0) > 0

    @staticmethod
    def page_photos(
        db: Session,
        page_num: int,
        page_size: int,
        name: str | None,
        album_id: int | None,
        user_id: int | None,
    ) -> dict:
        """分页查询照片"""
        conditions = ["1=1"]
        params: dict = {}
        if name:
            conditions.append("p.name LIKE :name")
            params["name"] = f"%{name}%"
        if album_id is not None:
            conditions.append("p.album_id = :album_id")
            params["album_id"] = album_id
        if user_id is not None:
            conditions.append("p.user_id = :user_id")
            params["user_id"] = user_id
        where_sql = " AND ".join(conditions)
        count_sql = text(f"SELECT COUNT(*) FROM t_photo p WHERE {where_sql}")
        total = db.scalar(count_sql, params) or 0
        query_sql = text(
            f"SELECT p.*, u.nickname AS username, a.name AS album_name "
            f"FROM t_photo p LEFT JOIN t_user u ON p.user_id = u.id "
            f"LEFT JOIN t_album a ON p.album_id = a.id "
            f"WHERE {where_sql} ORDER BY p.create_time DESC "
            f"LIMIT :offset, :limit"
        )
        params["offset"] = (page_num - 1) * page_size
        params["limit"] = page_size
        rows = db.execute(query_sql, params).fetchall()
        current_user_id = UserContext.get_user_id()
        records = []
        for row in rows:
            liked, favorited = ManageService._fill_photo_status(db, row.id, current_user_id)
            records.append(ManageService._photo_row_to_dict(row, liked, favorited))
        return page_result(total, records)

    @staticmethod
    def add_photo(db: Session, data: dict) -> None:
        """新增照片"""
        user_id = data.get("userId") or data.get("user_id") or UserContext.get_user_id()
        album_id = data.get("albumId") or data.get("album_id")
        photo = Photo(
            album_id=album_id,
            user_id=user_id,
            name=data.get("name"),
            url=data.get("url"),
            description=data.get("description"),
            file_size=data.get("fileSize") or data.get("file_size", 0),
            view_count=0,
            like_count=0,
            create_time=datetime.now(),
        )
        db.add(photo)
        db.commit()
        ManageService._update_album_photo_count(db, album_id)

    @staticmethod
    def update_photo(db: Session, data: dict) -> None:
        """修改照片"""
        photo = db.get(Photo, data.get("id"))
        if not photo:
            raise BusinessException("照片不存在")
        for field, attr in (("name", "name"), ("description", "description")):
            if field in data and data[field] is not None:
                setattr(photo, attr, data[field])
        db.commit()

    @staticmethod
    def delete_photo(db: Session, photo_id: int) -> None:
        """删除照片"""
        photo = db.get(Photo, photo_id)
        if not photo:
            raise BusinessException("照片不存在")
        current_user_id = UserContext.get_user_id()
        role = UserContext.get_role()
        if role != ROLE_ADMIN and current_user_id != photo.user_id:
            raise BusinessException("无权删除该照片")
        album_id = photo.album_id
        db.query(PhotoLike).filter(PhotoLike.photo_id == photo_id).delete()
        db.query(Favorite).filter(Favorite.photo_id == photo_id).delete()
        db.query(Comment).filter(Comment.photo_id == photo_id).delete()
        db.delete(photo)
        db.commit()
        ManageService._update_album_photo_count(db, album_id)

    @staticmethod
    def _update_album_photo_count(db: Session, album_id: int) -> None:
        """更新相册照片数量"""
        count = db.scalar(select(func.count()).select_from(Photo).where(Photo.album_id == album_id)) or 0
        album = db.get(Album, album_id)
        if album:
            album.photo_count = count
            db.commit()

    # ---------- 评论管理 ----------
    @staticmethod
    def page_comments(
        db: Session,
        page_num: int,
        page_size: int,
        status: int | None,
        photo_id: int | None,
    ) -> dict:
        """分页查询评论"""
        conditions = ["1=1"]
        params: dict = {}
        if status is not None:
            conditions.append("c.status = :status")
            params["status"] = status
        if photo_id is not None:
            conditions.append("c.photo_id = :photo_id")
            params["photo_id"] = photo_id
        where_sql = " AND ".join(conditions)
        count_sql = text(f"SELECT COUNT(*) FROM t_comment c WHERE {where_sql}")
        total = db.scalar(count_sql, params) or 0
        query_sql = text(
            f"SELECT c.*, u.nickname AS username, p.name AS photo_name "
            f"FROM t_comment c LEFT JOIN t_user u ON c.user_id = u.id "
            f"LEFT JOIN t_photo p ON c.photo_id = p.id "
            f"WHERE {where_sql} ORDER BY c.create_time ASC "
            f"LIMIT :offset, :limit"
        )
        params["offset"] = (page_num - 1) * page_size
        params["limit"] = page_size
        rows = db.execute(query_sql, params).fetchall()
        records = []
        for row in rows:
            records.append({
                "id": row.id,
                "photoId": row.photo_id,
                "userId": row.user_id,
                "content": row.content,
                "status": row.status,
                "createTime": format_value(row.create_time),
                "username": row.username,
                "photoName": row.photo_name,
            })
        return page_result(total, records)

    @staticmethod
    def add_comment(db: Session, photo_id: int, content: str) -> None:
        """新增评论"""
        comment = Comment(
            photo_id=photo_id,
            user_id=UserContext.get_user_id(),
            content=content,
            status=0,
            create_time=datetime.now(),
        )
        db.add(comment)
        db.commit()

    @staticmethod
    def audit_comment(db: Session, comment_id: int, status: int) -> None:
        """审核评论"""
        comment = db.get(Comment, comment_id)
        if comment:
            comment.status = status
            db.commit()

    @staticmethod
    def delete_comment(db: Session, comment_id: int) -> None:
        """删除评论"""
        comment = db.get(Comment, comment_id)
        if comment:
            db.delete(comment)
            db.commit()

    # ---------- 互动 ----------
    @staticmethod
    def toggle_like(db: Session, photo_id: int) -> None:
        """点赞/取消点赞"""
        user_id = UserContext.get_user_id()
        existing = db.scalar(
            select(PhotoLike).where(PhotoLike.photo_id == photo_id, PhotoLike.user_id == user_id)
        )
        photo = db.get(Photo, photo_id)
        if existing:
            db.delete(existing)
            if photo:
                photo.like_count = max(0, (photo.like_count or 0) - 1)
        else:
            db.add(PhotoLike(photo_id=photo_id, user_id=user_id, create_time=datetime.now()))
            if photo:
                photo.like_count = (photo.like_count or 0) + 1
        db.commit()

    @staticmethod
    def toggle_favorite(db: Session, photo_id: int) -> None:
        """收藏/取消收藏"""
        user_id = UserContext.get_user_id()
        existing = db.scalar(
            select(Favorite).where(Favorite.photo_id == photo_id, Favorite.user_id == user_id)
        )
        if existing:
            db.delete(existing)
        else:
            db.add(Favorite(photo_id=photo_id, user_id=user_id, create_time=datetime.now()))
        db.commit()

    @staticmethod
    def my_favorites(db: Session, page_num: int, page_size: int) -> dict:
        """我的收藏列表"""
        user_id = UserContext.get_user_id()
        query = select(Favorite).where(Favorite.user_id == user_id).order_by(Favorite.create_time.desc())
        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        favs = db.scalars(query.offset((page_num - 1) * page_size).limit(page_size)).all()
        records = []
        for fav in favs:
            photo = db.get(Photo, fav.photo_id)
            if photo:
                liked, favorited = ManageService._fill_photo_status(db, photo.id, user_id)
                records.append(model_to_camel_dict(photo, {"liked": liked, "favorited": True}))
        return page_result(total, records)

    # ---------- 公告 ----------
    @staticmethod
    def page_notices(db: Session, page_num: int, page_size: int) -> dict:
        """分页查询公告"""
        query = select(Notice).order_by(Notice.create_time.desc())
        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        records = db.scalars(query.offset((page_num - 1) * page_size).limit(page_size)).all()
        return page_result(total, [model_to_camel_dict(r) for r in records])

    @staticmethod
    def add_notice(db: Session, data: dict) -> None:
        """新增公告"""
        notice = Notice(
            title=data.get("title"),
            content=data.get("content"),
            admin_id=UserContext.get_user_id(),
            create_time=datetime.now(),
        )
        db.add(notice)
        db.commit()

    @staticmethod
    def update_notice(db: Session, data: dict) -> None:
        """修改公告"""
        notice = db.get(Notice, data.get("id"))
        if not notice:
            raise BusinessException("公告不存在")
        if data.get("title") is not None:
            notice.title = data.get("title")
        if data.get("content") is not None:
            notice.content = data.get("content")
        db.commit()

    @staticmethod
    def delete_notice(db: Session, notice_id: int) -> None:
        """删除公告"""
        notice = db.get(Notice, notice_id)
        if notice:
            db.delete(notice)
            db.commit()

    # ---------- 日志 ----------
    @staticmethod
    def page_logs(db: Session, page_num: int, page_size: int, username: str | None) -> dict:
        """分页查询日志"""
        query = select(OperLog)
        if username:
            query = query.where(OperLog.username.like(f"%{username}%"))
        query = query.order_by(OperLog.create_time.desc())
        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        records = db.scalars(query.offset((page_num - 1) * page_size).limit(page_size)).all()
        return page_result(total, [model_to_camel_dict(r) for r in records])

    # ---------- 统计 ----------
    @staticmethod
    def admin_statistics(db: Session) -> dict:
        """管理员首页统计"""
        photo_trend = db.execute(text(
            "SELECT DATE(create_time) AS date, COUNT(*) AS count "
            "FROM t_photo WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 6 DAY) "
            "GROUP BY DATE(create_time) ORDER BY date"
        )).fetchall()
        category_ratio = db.execute(text(
            "SELECT c.name AS name, COUNT(a.id) AS value "
            "FROM t_category c LEFT JOIN t_album a ON c.id = a.category_id "
            "GROUP BY c.id, c.name ORDER BY value DESC"
        )).fetchall()
        top_users = db.execute(text(
            "SELECT u.nickname AS name, COUNT(p.id) AS value "
            "FROM t_user u LEFT JOIN t_photo p ON u.id = p.user_id "
            "GROUP BY u.id, u.nickname ORDER BY value DESC LIMIT 5"
        )).fetchall()
        return {
            "userCount": db.scalar(select(func.count()).select_from(User)) or 0,
            "albumCount": db.scalar(select(func.count()).select_from(Album)) or 0,
            "photoCount": db.scalar(select(func.count()).select_from(Photo)) or 0,
            "pendingCommentCount": db.scalar(
                select(func.count()).select_from(Comment).where(Comment.status == 0)
            ) or 0,
            "photoTrend": [{"date": format_value(r.date), "count": r.count} for r in photo_trend],
            "categoryRatio": [{"name": r.name, "value": r.value} for r in category_ratio],
            "topUsers": [{"name": r.name, "value": r.value} for r in top_users],
        }

    @staticmethod
    def user_statistics(db: Session) -> dict:
        """用户首页统计"""
        user_id = UserContext.get_user_id()
        photos = db.scalars(select(Photo).where(Photo.user_id == user_id)).all()
        total_likes = sum(p.like_count or 0 for p in photos)
        photo_trend = db.execute(text(
            "SELECT DATE(create_time) AS date, COUNT(*) AS count "
            "FROM t_photo WHERE user_id = :user_id AND create_time >= DATE_SUB(CURDATE(), INTERVAL 6 DAY) "
            "GROUP BY DATE(create_time) ORDER BY date"
        ), {"user_id": user_id}).fetchall()
        category_ratio = db.execute(text(
            "SELECT c.name AS name, COUNT(a.id) AS value "
            "FROM t_category c LEFT JOIN t_album a ON c.id = a.category_id AND a.user_id = :user_id "
            "GROUP BY c.id, c.name ORDER BY value DESC"
        ), {"user_id": user_id}).fetchall()
        return {
            "albumCount": db.scalar(select(func.count()).select_from(Album).where(Album.user_id == user_id)) or 0,
            "photoCount": db.scalar(select(func.count()).select_from(Photo).where(Photo.user_id == user_id)) or 0,
            "favoriteCount": db.scalar(select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)) or 0,
            "totalLikes": total_likes,
            "photoTrend": [{"date": format_value(r.date), "count": r.count} for r in photo_trend],
            "categoryRatio": [{"name": r.name, "value": r.value} for r in category_ratio],
        }
