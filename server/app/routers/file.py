"""
文件上传路由
"""
from fastapi import APIRouter, Depends, File, UploadFile

from app.common.response import R
from app.utils.file_util import FileUtil

router = APIRouter(prefix="/api/file", tags=["文件上传"])


@router.post("/upload")
async def upload(file: UploadFile = File(...), type: str = "photo"):
    """上传文件"""
    url = await FileUtil.upload(file, type)
    return R.ok(url)
