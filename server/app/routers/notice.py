"""
公告管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/notice", tags=["公告管理"])


@router.get("/page")
def page(pageNum: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    """分页查询公告"""
    return R.ok(ManageService.page_notices(db, pageNum, pageSize))


@router.get("/list")
def list_notice(db: Session = Depends(get_db)):
    """公告列表(无需登录)"""
    return R.ok(ManageService.page_notices(db, 1, 20))


@router.post("")
def add(request: Request, params: dict, db: Session = Depends(get_db)):
    """新增公告"""
    ManageService.add_notice(db, params)
    write_oper_log(db, request, "发布公告")
    return R.ok()


@router.put("")
def update(params: dict, db: Session = Depends(get_db)):
    """修改公告"""
    ManageService.update_notice(db, params)
    return R.ok()


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    """删除公告"""
    ManageService.delete_notice(db, id)
    return R.ok()
