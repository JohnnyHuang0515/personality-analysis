# 人格特質分析系統

一個基於 React + FastAPI 的現代化人格特質分析平台，支援四種測驗類型（MBTI、DISC、Big5、Enneagram）並具備完整的測驗功能和綜合分析報告。

## 🚀 功能特色

### 核心功能
- **四種測驗類型**：MBTI、DISC、Big5、Enneagram 人格測驗
- **綜合分析報告**：整合四種測驗的統一報告
- **智能進度追蹤**：視覺化進度條和答題狀態
- **詳細分析報告**：個人化的人格特質分析
- **雷達圖視覺化**：直觀展示特質分布
- **整合洞察**：領導風格、溝通偏好、工作環境、發展建議
- **響應式設計**：支援桌面和移動設備
- **答案驗證**：確保所有題目完成後才能提交

### 技術特色
- **前端**：React + TypeScript + Tailwind CSS
- **後端**：FastAPI + SQLite + SQLAlchemy
- **狀態管理**：React Context 管理測驗狀態
- **API設計**：RESTful API，完整的錯誤處理

## 📁 專案結構

```
personality-analysis/
├── frontend/                 # React 前端應用
│   ├── src/
│   │   ├── components/      # React 組件
│   │   ├── pages/          # 頁面組件
│   │   ├── services/       # API 服務
│   │   └── contexts/       # React Context
│   └── public/             # 靜態資源
├── backend/                 # FastAPI 後端服務
│   ├── app/                # 主要應用代碼
│   │   ├── api/           # API 路由
│   │   ├── models/        # 資料模型
│   │   ├── schemas/       # Pydantic 模式
│   │   └── services/      # 業務邏輯
│   ├── data/              # 題庫資料 (JSON 格式)
│   └── scripts/           # 工具腳本
├── docs/                   # 專案文檔
└── design_templates/       # 設計模板
```

## 🛠️ 快速開始

### 環境要求
- Node.js 16+
- Python 3.8+
- Git

### 1. 克隆專案
```bash
git clone <repository-url>
cd personality-analysis
```

### 2. 後端設置
```bash
cd backend

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python scripts/init_db.py

# 啟動後端服務
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端設置
```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發服務器
npm start
```

### 4. 訪問應用
- 前端：http://localhost:3000
- 後端API：http://localhost:8000
- API文檔：http://localhost:8000/docs

## 📊 題庫統計

### 當前題庫內容
- **MBTI**: 40 題 (外向-內向、感覺-直覺、思考-情感、判斷-知覺)
- **DISC**: 40 題 (支配、影響、穩健、謹慎)
- **Big5**: 44 題 (開放性、盡責性、外向性、親和性、神經質)
- **Enneagram**: 40 題 (九型人格)
- **總計**: 164 題

### 題庫格式
所有題目採用標準化 JSON 格式，包含：
- 題目文字
- 選項列表
- 權重設定
- 反向計分標記

## 🧪 測試

### 功能測試
1. **題目載入**：確認各測驗類型能正確載入題目
2. **答案提交**：測試完成測驗後的提交功能
3. **報告生成**：驗證分析報告的生成和顯示

### API 測試
```bash
# 健康檢查
curl http://localhost:8000/health

# 獲取題目
curl http://localhost:8000/api/v1/questions/MBTI

# 提交答案
curl -X POST http://localhost:8000/api/v1/answers/submit \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "test_type": "mbti", "answers": []}'
```

## 📚 文檔

- [系統架構設計](docs/02_system_architecture.md)
- [API設計規格](docs/04_api_design_specification.md)
- [開發指南](docs/development_guideline.md)
- [資料夾結構說明](docs/folder_structure.md)

## 🔧 開發指南

### 測驗流程
1. **選擇測驗類型**：用戶選擇要進行的測驗
2. **載入題目**：從後端 API 獲取對應題目
3. **答題過程**：用戶逐題回答，進度自動保存
4. **提交測驗**：完成所有題目後提交答案
5. **生成報告**：後端分析答案並生成報告

### 代碼風格
- 前端：TypeScript + ESLint + Prettier
- 後端：Python + Black + isort
- 提交信息：遵循 Conventional Commits

## 🚀 部署

### 生產環境
```bash
# 後端
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端
cd frontend
npm run build
```

### Windows 環境
```bash
# 使用 PowerShell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd frontend
npm start
```

## 🤝 貢獻

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權

本專案採用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 檔案了解詳情

## 🎯 專案狀態

- ✅ 四種測驗類型完成
- ✅ 題庫更新完成 (164 題)
- ✅ 前端介面完成
- ✅ 後端 API 完成
- ✅ 答案提交功能完成
- ✅ 綜合分析報告完成
- ✅ 雷達圖視覺化完成
- ✅ 整合洞察功能完成

---

**最後更新**：2025-01-20
**版本**：v2.0.0 