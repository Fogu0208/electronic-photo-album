"""
评论管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/comment", tags=["评论管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 10,
    status: int | None = None,
    photoId: int | None = None,
    db: Session = Depends(get_db),
):
    """分页查询评论"""
    return R.ok(ManageService.page_comments(db, pageNum, pageSize, status, photoId))


@router.post("")
def add(request: Request, params: dict, db: Session = Depends(get_db)):
    """发表评论"""
    ManageService.add_comment(db, params.get("photoId"), params.get("content"))
    write_oper_log(db, request, "发表评论")
    return R.ok()


@router.put("/audit")
def audit(request: Request, params: dict, db: Session = Depends(get_db)):
    """审核评论"""
    ManageService.audit_comment(db, params.get("id"), params.get("status"))
    write_oper_log(db, request, "审核评论")
    return R.ok()


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    """删除评论"""
    ManageService.delete_comment(db, id)
    return R.ok()
