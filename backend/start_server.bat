@echo off
echo 啟動人格特質分析系統後端服務...
echo 使用現有 Poetry 環境: personality-analysis-system-BLgXGcbj-py3.12

cd /d "%~dp0"
echo 當前目錄: %CD%
echo 啟動服務...

"C:\Users\User\AppData\Local\pypoetry\Cache\virtualenvs\personality-analysis-system-BLgXGcbj-py3.12\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause 