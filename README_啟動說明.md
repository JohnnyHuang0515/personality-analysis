# 🚀 人格特質分析系統 - 啟動說明

## 📋 快速啟動

### 方法一：手動啟動 (推薦)

#### 1. 啟動後端服務器
```cmd
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. 啟動前端服務器 (新開終端)
```cmd
cd frontend
npm start
```

### 方法二：使用啟動腳本
```cmd
# 雙擊執行或在命令提示字元中執行
.\start.bat
```

## 🌐 訪問地址

- **前端應用**: http://localhost:3000
- **API 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

## 📊 系統功能

### 測驗類型
- **MBTI**: 40 題 (外向-內向、感覺-直覺、思考-情感、判斷-知覺)
- **DISC**: 40 題 (支配、影響、穩健、謹慎)
- **Big5**: 44 題 (開放性、盡責性、外向性、親和性、神經質)
- **Enneagram**: 40 題 (九型人格)

### 核心功能
- ✅ 四種測驗類型
- ✅ 智能進度追蹤
- ✅ 答案驗證和提交
- ✅ 響應式設計
- ✅ 綜合分析報告
- ✅ 雷達圖視覺化
- ✅ 整合洞察功能

## ⚠️ 注意事項

1. **執行位置**: 確保在專案根目錄執行命令
2. **首次運行**: 需要先初始化資料庫
3. **服務器運行**: 前後端服務器需要在不同終端中運行
4. **停止服務**: 在對應終端中按 `Ctrl+C` 停止服務

## 🛠️ 系統要求

- **Python 3.8+**
- **Node.js 16+** 和 **npm**
- **Windows 10/11** (支援 PowerShell)

## 🔧 故障排除

### 1. 初始化資料庫
```cmd
cd backend
python scripts/init_db.py
```

### 2. PowerShell 執行政策錯誤
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. 端口被佔用
```cmd
# 檢查端口佔用
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 終止佔用進程
taskkill /PID <進程ID> /F
```

### 4. 依賴安裝失敗
```cmd
# 後端依賴
cd backend
pip install -r requirements.txt

# 前端依賴
cd frontend
npm install
```

### 5. 模組導入錯誤
```cmd
# 確保在正確目錄執行
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 系統狀態檢查

### 檢查服務器狀態
```cmd
# 檢查後端
curl http://localhost:8000/health

# 檢查前端
curl http://localhost:3000
```

### 檢查題庫狀態
```cmd
cd backend
python -c "from data.personality_questions import get_question_count_by_type; print(get_question_count_by_type())"
```

## 🚪 停止服務

### 方法一：使用 Ctrl+C
- 在運行服務的終端中按 `Ctrl+C`

### 方法二：終止進程
```cmd
# 終止所有相關進程
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

## 📝 開發日誌

### 最新更新 (2025-01-20)
- ✅ 完成綜合分析報告功能
- ✅ 實現雷達圖視覺化
- ✅ 完成整合洞察功能
- ✅ 優化檔案結構和清理廢棄檔案
- ✅ 更新專案文檔

---

**版本**: 2.0.0  
**最後更新**: 2025-01-20  
**作者**: AI Assistant 