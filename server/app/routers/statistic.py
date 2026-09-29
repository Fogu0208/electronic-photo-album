"""
统计路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService

router = APIRouter(prefix="/api/statistic", tags=["统计"])


@router.get("/admin")
def admin_statistics(db: Session = Depends(get_db)):
    """管理员首页统计"""
    return R.ok(ManageService.admin_statistics(db))


@router.get("/user")
def user_statistics(db: Session = Depends(get_db)):
    """用户首页统计"""
    return R.ok(ManageService.user_statistics(db))
