# 🚀 綜合人格特質分析系統 - 一鍵啟動

## 📋 快速啟動

### 方法一：一鍵啟動 (推薦)
```cmd
# 雙擊執行或在命令提示字元中執行
.\start.bat
```

### 方法二：手動啟動

#### 啟動後端服務器
```cmd
cd backend
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### 啟動前端服務器
```cmd
cd frontend
npm start
```

## 🌐 訪問地址

- **前端應用**: http://localhost:3000
- **API 文檔**: http://127.0.0.1:8000/docs
- **健康檢查**: http://127.0.0.1:8000/health

## 📁 檔案說明

- `start.bat` - 一鍵啟動腳本 (推薦使用)
- `README_啟動說明.md` - 本說明文件

## ⚠️ 注意事項

1. **執行位置**: 確保在專案根目錄執行腳本
2. **首次運行**: 會自動安裝依賴和初始化資料庫
3. **服務器運行**: 前後端服務器會在獨立視窗中運行
4. **停止服務**: 關閉對應的終端視窗即可停止服務

## 🛠️ 系統要求

- **Python 3.10+** 和 **Poetry**
- **Node.js 16+** 和 **npm**
- **Windows 作業系統**

## 🔧 故障排除

### 1. PowerShell 執行政策錯誤
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. 端口被佔用
```cmd
# 檢查端口佔用
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 終止佔用進程
taskkill /PID <進程ID> /F
```

### 3. 依賴安裝失敗
```cmd
# 後端依賴
cd backend
poetry install

# 前端依賴
cd frontend
npm install
```

## 📊 系統狀態檢查

### 檢查服務器狀態
```cmd
# 檢查後端
curl http://127.0.0.1:8000/health

# 檢查前端
curl http://localhost:3000
```

## 🚪 停止服務

### 方法一：關閉終端視窗
- 關閉對應的終端視窗即可停止服務

### 方法二：使用 Ctrl+C
- 在運行服務的終端中按 `Ctrl+C`

### 方法三：終止進程
```cmd
# 終止所有相關進程
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

---

**版本**: 1.0.0  
**最後更新**: 2025-07-19  
**作者**: AI Assistant 