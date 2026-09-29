"""
应用配置模块
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """系统配置类"""

    app_name: str = "基于Python的电子相册管理系统"
    host: str = "0.0.0.0"
    port: int = 8080
    db_url: str = "mysql+pymysql://root:123456@127.0.0.1:3308/db_photo_album?charset=utf8mb4"
    upload_path: str = "D:/uploads31"
    jwt_secret: str = "SpringBootPhotoAlbumSystemSecretKey2026Java1234"
    jwt_expire_ms: int = 86400000

    class Config:
        env_file = ".env"


settings = Settings()
