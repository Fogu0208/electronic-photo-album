"""
日志管理路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService

router = APIRouter(prefix="/api/log", tags=["日志管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 10,
    username: str | None = None,
    db: Session = Depends(get_db),
):
    """分页查询日志"""
    return R.ok(ManageService.page_logs(db, pageNum, pageSize, username))
