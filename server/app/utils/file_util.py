"""
文件上传工具类
"""
import os
import uuid

from fastapi import UploadFile

from app.config import settings


class FileUtil:
    """文件上传工具"""

    @staticmethod
    async def upload(file: UploadFile, sub_dir: str) -> str:
        """上传文件并返回访问URL"""
        if file is None or not file.filename:
            raise RuntimeError("上传文件不能为空")

        original_name = file.filename
        ext = original_name[original_name.rfind("."):] if "." in original_name else ".jpg"
        file_name = uuid.uuid4().hex + ext
        dir_path = os.path.join(settings.upload_path, sub_dir)
        os.makedirs(dir_path, exist_ok=True)
        dest_path = os.path.join(dir_path, file_name)

        content = await file.read()
        with open(dest_path, "wb") as f:
            f.write(content)

        return f"/uploads31/{sub_dir}/{file_name}"
