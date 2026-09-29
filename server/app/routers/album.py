"""
相册管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.models.entities import Album
from app.services.manage_service import ManageService
from app.utils.serialize import model_to_camel_dict
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/album", tags=["相册管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 10,
    name: str | None = None,
    userId: int | None = None,
    isPublic: int | None = None,
    db: Session = Depends(get_db),
):
    """分页查询相册"""
    return R.ok(ManageService.page_albums(db, pageNum, pageSize, name, userId, isPublic))


@router.get("/public/page")
def public_page(
    pageNum: int = 1,
    pageSize: int = 12,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    """公开相册列表"""
    return R.ok(ManageService.page_albums(db, pageNum, pageSize, name, None, 1))


@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    """获取相册详情"""
    album = db.get(Album, id)
    return R.ok(model_to_camel_dict(album))


@router.post("")
def add(request: Request, params: dict, db: Session = Depends(get_db)):
    """新增相册"""
    ManageService.add_album(db, params)
    write_oper_log(db, request, "创建相册")
    return R.ok()


@router.put("")
def update(request: Request, params: dict, db: Session = Depends(get_db)):
    """修改相册"""
    ManageService.update_album(db, params)
    write_oper_log(db, request, "修改相册")
    return R.ok()


@router.delete("/{id}")
def delete(id: int, request: Request, db: Session = Depends(get_db)):
    """删除相册"""
    ManageService.delete_album(db, id)
    write_oper_log(db, request, "删除相册")
    return R.ok()
