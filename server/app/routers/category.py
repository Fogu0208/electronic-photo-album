"""
分类管理路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import R
from app.database import get_db
from app.services.manage_service import ManageService

router = APIRouter(prefix="/api/category", tags=["分类管理"])


@router.get("/page")
def page(
    pageNum: int = 1,
    pageSize: int = 10,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    """分页查询分类"""
    return R.ok(ManageService.page_categories(db, pageNum, pageSize, name))


@router.get("/list")
def list_all(db: Session = Depends(get_db)):
    """获取所有分类"""
    return R.ok(ManageService.list_categories(db))


@router.post("")
def add(params: dict, db: Session = Depends(get_db)):
    """新增分类"""
    ManageService.add_category(db, params)
    return R.ok()


@router.put("")
def update(params: dict, db: Session = Depends(get_db)):
    """修改分类"""
    ManageService.update_category(db, params)
    return R.ok()


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    """删除分类"""
    ManageService.delete_category(db, id)
    return R.ok()
