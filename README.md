# 綜合人格特質分析系統

一個基於 React + FastAPI 的現代化人格特質分析平台，支援多種測驗類型（MBTI、DISC、Enneagram）並具備完整的時間記憶功能。

## 🚀 功能特色

### 核心功能
- **多種測驗類型**：MBTI、DISC、Enneagram 人格測驗
- **智能時間記憶**：暫停/恢復功能，自動保存進度
- **即時進度追蹤**：視覺化進度條和計時器
- **詳細分析報告**：個人化的人格特質分析
- **響應式設計**：支援桌面和移動設備

### 技術特色
- **前端**：React + TypeScript + Tailwind CSS
- **後端**：FastAPI + SQLite + SQLAlchemy
- **時間記憶**：簡化可靠的暫停/恢復機制
- **API設計**：RESTful API，完整的錯誤處理

## 📁 專案結構

```
綜合人格特質分析/
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
│   ├── tests/             # 測試檔案
│   └── data/              # 題庫資料
├── docs/                   # 專案文檔
├── design_templates/       # 設計模板
└── scripts/               # 工具腳本
```

## 🛠️ 快速開始

### 環境要求
- Node.js 16+
- Python 3.8+
- Git

### 1. 克隆專案
```bash
git clone <repository-url>
cd 綜合人格特質分析
```

### 2. 後端設置
```bash
cd backend

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python init_db.py

# 啟動後端服務
python main.py
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

## 🧪 測試

### 運行測試
```bash
cd backend
python run_tests.py
```

### 單獨測試
```bash
python test_simplified_time.py    # 時間記憶功能
python explain_time_memory.py     # 查看機制說明
```

## 📚 文檔

- [系統架構設計](docs/02_system_architecture.md)
- [API設計規格](docs/04_api_design_specification.md)
- [開發指南](docs/development_guideline.md)
- [資料夾結構說明](docs/folder_structure.md)

## 🔧 開發指南

### 時間記憶功能
系統採用簡化的時間記憶機制：
- **暫停時保存**：直接將當前時間保存到資料庫
- **恢復時讀取**：從資料庫讀取保存的時間
- **單一時間源**：避免複雜的同步邏輯

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
python main.py --host 0.0.0.0 --port 8000

# 前端
cd frontend
npm run build
```

### Docker 部署
```bash
docker-compose up -d
```

## 🤝 貢獻

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權

本專案採用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 檔案了解詳情

## 📞 聯繫

- 專案維護者：[Your Name]
- 電子郵件：[your.email@example.com]
- 專案連結：[https://github.com/yourusername/project-name]

## 🎯 專案狀態

- ✅ 核心功能完成
- ✅ 時間記憶功能優化
- ✅ 測試覆蓋完整
- ✅ 文檔更新完成
- 🔄 持續改進中

---

**最後更新**：2025-07-19
**版本**：v1.0.0 