"""
用户管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService
from app.utils.user_context import write_oper_log

router = APIRouter(prefix="/api/user", tags=["用户管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 10,
    username: str | None = None,
    db: Session = Depends(get_db),
):
    """分页查询用户"""
    return R.ok(ManageService.page_users(db, pageNum, pageSize, username))


@router.post("")
def add(request: Request, params: dict, db: Session = Depends(get_db)):
    """新增用户"""
    ManageService.add_user(db, params)
    write_oper_log(db, request, "新增用户")
    return R.ok()


@router.put("")
def update(request: Request, params: dict, db: Session = Depends(get_db)):
    """修改用户"""
    ManageService.update_user(db, params)
    write_oper_log(db, request, "修改用户")
    return R.ok()


@router.delete("/{id}")
def delete(id: int, request: Request, db: Session = Depends(get_db)):
    """删除用户"""
    ManageService.delete_user(db, id)
    write_oper_log(db, request, "删除用户")
    return R.ok()
