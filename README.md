# 綜合人格特質分析系統

## 專案簡介
本專案為一站式多元人格測驗與分析平台，整合 MBTI、DISC、Big5、Enneagram 四大人格理論，提供線上測驗、報告與綜合分析。

## 技術棧
- **後端**：FastAPI + SQLite + SQLAlchemy
- **前端**：React + TypeScript + Tailwind CSS
- **依賴管理**：Poetry (Python)、npm (Node)

## 主要資料夾結構
```
backend/         # 後端 API 與資料庫
  app/           # FastAPI 主程式、models、schemas、api
  tests/         # pytest 測試
  data/          # 題庫與靜態資料
  scripts/       # 初始化與維運腳本
frontend/        # 前端 React 專案
  src/           # 主要程式碼
  public/        # 靜態資源
config/          # 共用設定
scripts/         # 跨模組腳本
config/          # 設定檔
```

## 快速啟動
### 後端
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 執行測試
```bash
cd backend
poetry run pytest
```

## 主要功能
- 支援 MBTI、DISC、Big5、Enneagram 四大人格測驗
- 題庫自動去重、品質控管
- 單題作答、進度查詢、報告產生
- 綜合分析與個人化建議
- 前後端 API 串接、響應式 UI

## 進階
- 詳細 API 規格、資料結構與開發規範請見 docs/ 目錄
- 進度與開發紀錄請見 docs/00_project_brief_prd_summary.md 