@echo off
chcp 65001 >nul
title Python电子相册管理系统

set ROOT=%~dp0
set SRV=%ROOT%server
set CLI=%ROOT%client

echo ============================================
echo   正在启动 Python 电子相册管理系统
echo   后端 http://127.0.0.1:8081  (接口文档 /docs)
echo   前端 http://127.0.0.1:5174/login
echo   管理员账号 python222 / 123456
echo   普通用户   zhangsan  / 123456
echo ============================================
echo.

start "相册-后端 :8081" cmd /k "cd /d "%SRV%" && .venv\Scripts\python.exe main.py"
timeout /t 6 /nobreak >nul
start "相册-前端 :5174" cmd /k "cd /d "%CLI%" && set VITE_BACKEND_PORT=8081&& npm run dev -- --port 5174"

timeout /t 8 /nobreak >nul
start http://127.0.0.1:5174/login

echo 两个服务已在独立窗口启动，关闭对应窗口即可停止服务。
pause
