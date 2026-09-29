"""
互动路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/interact", tags=["互动"])


@router.post("/like/{photoId}")
def toggle_like(photoId: int, request: Request, db: Session = Depends(get_db)):
    """点赞/取消点赞"""
    ManageService.toggle_like(db, photoId)
    write_oper_log(db, request, "点赞照片")
    return R.ok()


@router.post("/favorite/{photoId}")
def toggle_favorite(photoId: int, request: Request, db: Session = Depends(get_db)):
    """收藏/取消收藏"""
    ManageService.toggle_favorite(db, photoId)
    write_oper_log(db, request, "收藏照片")
    return R.ok()


@router.get("/favorite/page")
def favorite_page(
    pageNum: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    """我的收藏列表"""
    return R.ok(ManageService.my_favorites(db, pageNum, pageSize))
