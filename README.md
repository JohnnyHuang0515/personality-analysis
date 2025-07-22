# 人格特質分析系統

一個基於 React + FastAPI 的現代化人格特質分析平台，支援四種測驗類型（MBTI、DISC、Big5、Enneagram）並具備完整的測驗功能、綜合分析報告和智能會話管理系統。

---

## 🏆 專案摘要與歷史

- **專案名稱**：人格特質分析系統
- **版本**：v2.1.0
- **狀態**：✅ 完成（活躍維護）
- **最後更新**：2025-01-20
- **專案成就**：
  - 四大人格測驗整合（MBTI、DISC、Big5、Enneagram）
  - 完整題庫（363題，已優化、去重、繁體化）
  - 綜合分析報告、雷達圖、整合洞察
  - 會話管理、進度追蹤、暫停/恢復、跨設備同步
  - 前後端分離，API 完整，文件齊全

---

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
- **會話管理**：支援測驗暫停/恢復和時間追蹤 ⭐ 新增

### 技術特色
- **前端**：React + TypeScript + Tailwind CSS
- **後端**：FastAPI + SQLite + SQLAlchemy
- **狀態管理**：React Context 管理測驗狀態
- **API設計**：RESTful API，完整的錯誤處理
- **會話管理**：智能時間追蹤和進度同步 ⭐ 新增

---

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
│   │   │   ├── answers.py     # 答案管理
│   │   │   ├── questions.py   # 題目管理
│   │   │   ├── reports.py     # 報告生成
│   │   │   └── sessions.py    # 會話管理 ⭐ 新增
│   │   ├── models/        # 資料模型
│   │   ├── schemas/       # Pydantic 模式
│   │   └── services/      # 業務邏輯
│   ├── data/              # 題庫資料 (JSON 格式)
│   └── scripts/           # 工具腳本
├── docs/                   # 專案文檔
└── design_templates/       # 設計模板（保留）
```

---

## 🛠️ 快速啟動指引

### 1. 環境需求
- Python 3.8+
- Node.js 16+
- Windows 10/11（支援 PowerShell）

### 2. 後端啟動
```bash
cd backend
pip install -r requirements.txt
python scripts/init_db.py  # 初始化資料庫（如需）
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端啟動
```bash
cd frontend
npm install
npm start
```

### 4. 一鍵啟動（Windows）
```batch
start.bat
```

### 5. 常用網址
- 前端：http://localhost:3000
- 後端API：http://localhost:8000
- API文檔：http://localhost:8000/docs

---

## 📊 題庫與資料庫狀態

- **MBTI**: 80 題
- **DISC**: 80 題
- **Big5**: 80 題
- **Enneagram**: 123 題
- **總計**: 363 題
- 題庫已繁體化、去重、分布均衡，並正確匯入資料庫

### 資料庫結構
- `test_question`：題目表（含 options/weight JSON 格式、is_reverse）
- `test_answer`：答案表（含 session_id）
- `test_session`：會話表（進度/暫停/恢復/同步）
- `test_report`：報告表

---

## 🧹 專案清理與最佳實踐

- 已移除所有臨時測試腳本、重複報告、Scratchpad 等冗餘檔案
- 文件內容已合併至本 README，成為唯一權威文件
- 保留 design_templates/ 供未來設計/審查參考
- 專案結構清晰，便於維護與交付

---

## 🧪 測試與驗證

- API、前端、資料庫均已驗證可用
- 題庫載入、答案提交、報告生成、會話管理等功能皆已測試通過
- 可用 Postman/curl 或前端頁面進行驗證

---

## 📝 專案歷史與成就紀錄

- 2025-01-20：完成資料庫結構優化、會話管理、題庫最終匯入與全專案清理
- 2025-07-20：綜合報告功能完成，前後端整合測試通過
- 2025-07-19：四大測驗類型與 API/前端核心功能全部完成

---

## 🤝 貢獻與維護

- 請參考本 README 及 docs/ 內設計/規格文件
- 如需貢獻，請 Fork 專案、建立分支、提交 Pull Request
- 問題回報請附上詳細錯誤訊息與重現步驟

---

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 LICENSE

---

**本 README 已整合所有專案歷史、狀態、啟動、清理、成就與最佳實踐，為唯一權威文件。** 