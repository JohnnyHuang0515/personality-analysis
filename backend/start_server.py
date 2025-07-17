#!/usr/bin/env python3
"""
自動啟動 FastAPI 服務器腳本
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def check_server_running(host="127.0.0.1", port=8000):
    """檢查服務器是否已經運行"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_server():
    """啟動 FastAPI 服務器"""
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    print("🚀 正在啟動綜合人格特質分析平台服務器...")
    print(f"📁 工作目錄: {current_dir}")

    # 檢查服務器是否已經運行
    if check_server_running():
        print("✅ 服務器已經在運行中 (http://127.0.0.1:8000)")
        print("📊 API 文檔: http://127.0.0.1:8000/docs")
        return

    # 檢查 main.py 是否存在
    main_file = current_dir / "main.py"
    if not main_file.exists():
        print("❌ 錯誤: main.py 文件不存在")
        print(f"預期位置: {main_file}")
        return

    try:
        # 啟動服務器 (使用 poetry 執行 uvicorn)
        print("🔄 正在啟動服務器...")
        process = subprocess.Popen([
            "poetry", "run", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=current_dir)

        # 等待服務器啟動
        print("⏳ 等待服務器啟動...")
        for i in range(30):  # 最多等待30秒
            time.sleep(1)
            if check_server_running():
                print("✅ 服務器啟動成功!")
                print("🌐 服務器地址: http://127.0.0.1:8000")
                print("📊 API 文檔: http://127.0.0.1:8000/docs")
                print("🔧 重新載入模式: 已啟用")
                print("\n按 Ctrl+C 停止服務器")
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 正在停止服務器...")
                    process.terminate()
                    process.wait()
                    print("✅ 服務器已停止")
                return
        print("❌ 服務器啟動超時")
        process.terminate()
    except FileNotFoundError:
        print("❌ 錯誤: 找不到 poetry 或 uvicorn")
        print("請確保已安裝依賴: poetry install")
    except Exception as e:
        print(f"❌ 啟動服務器時發生錯誤: {e}")

if __name__ == "__main__":
    start_server() 