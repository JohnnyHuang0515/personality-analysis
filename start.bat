@echo off
chcp 65001 >nul
title 人格特質分析系統 - 啟動器

echo.
echo ========================================
echo   人格特質分析系統 - 啟動器
echo ========================================
echo.

:: 檢查目錄結構
if not exist "backend" (
    echo 錯誤: 找不到 backend 目錄
    echo 請在專案根目錄執行此腳本
    pause
    exit /b 1
)

if not exist "frontend" (
    echo 錯誤: 找不到 frontend 目錄
    echo 請在專案根目錄執行此腳本
    pause
    exit /b 1
)

echo 正在啟動後端服務器...
echo.

:: 啟動後端服務器
cd backend
start "後端服務器" cmd /k "python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: 等待後端啟動
timeout /t 5 /nobreak >nul

echo 正在啟動前端服務器...
echo.

:: 啟動前端服務器
cd ..\frontend
start "前端服務器" cmd /k "npm start"

:: 等待前端啟動
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo           系統啟動完成！
echo ========================================
echo.
echo 前端應用: http://localhost:3000
echo API 文檔: http://127.0.0.1:8000/docs
echo 健康檢查: http://127.0.0.1:8000/health
echo.
echo 按任意鍵打開瀏覽器...
pause >nul

:: 打開瀏覽器
start http://localhost:3000
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000/docs

echo.
echo 瀏覽器已打開！
echo 關閉此視窗不會停止服務器
echo 要停止服務器，請關閉對應的終端視窗
echo.
pause 