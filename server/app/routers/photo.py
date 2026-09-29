"""
照片管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/photo", tags=["照片管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 12,
    name: str | None = None,
    albumId: int | None = None,
    userId: int | None = None,
    db: Session = Depends(get_db),
):
    """分页查询照片"""
    return R.ok(ManageService.page_photos(db, pageNum, pageSize, name, albumId, userId))


@router.post("")
def add(request: Request, params: dict, db: Session = Depends(get_db)):
    """新增照片"""
    ManageService.add_photo(db, params)
    write_oper_log(db, request, "上传照片")
    return R.ok()


@router.put("")
def update(params: dict, db: Session = Depends(get_db)):
    """修改照片"""
    ManageService.update_photo(db, params)
    return R.ok()


@router.delete("/{id}")
def delete(id: int, request: Request, db: Session = Depends(get_db)):
    """删除照片"""
    ManageService.delete_photo(db, id)
    write_oper_log(db, request, "删除照片")
    return R.ok()
