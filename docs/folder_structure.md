# 專案資料夾結構規劃（綜合人格特質分析平台）

---

## 頂層結構

```
綜合人格特質分析/
├── backend/                # 後端服務（FastAPI, Python, Poetry）
├── frontend/               # 前端專案（React, TypeScript, Ant Design）
├── docs/                   # 專案文件（PRD, 架構、設計、API 規範等）
├── scripts/                # 部署、資料匯入、維運腳本
├── tests/                  # 後端單元/整合測試
├── data/                   # 靜態資料（如題庫、分析規則、初始化SQL）
├── .env.example            # 環境變數範例
├── README.md               # 專案說明文件
├── folder_structure.md     # 本文件
```

---

## backend/
```
backend/
├── app/
│   ├── main.py                 # FastAPI 入口
│   ├── api/                    # API 路由模組
│   │   ├── endpoints/          # 各測驗/分析API分組
│   │   │   ├── mbti.py
│   │   │   ├── disc.py
│   │   │   ├── big5.py
│   │   │   ├── enneagram.py
│   │   │   ├── composite.py
│   │   │   └── questions.py
│   │   └── __init__.py
│   ├── core/                   # 共用邏輯（設定、工具、例外處理）
│   ├── models/                 # SQLAlchemy ORM 資料表定義
│   ├── schemas/                # Pydantic 資料驗證/序列化
│   ├── services/               # 各測驗/分析服務邏輯
│   │   ├── mbti.py
│   │   ├── disc.py
│   │   ├── big5.py
│   │   ├── enneagram.py
│   │   ├── composite.py
│   │   └── __init__.py
│   ├── db/                     # 資料庫連線、初始化、遷移
│   └── utils/                  # 工具函式
├── alembic/                    # 資料庫遷移腳本
├── pyproject.toml              # Poetry 設定
├── .env                        # 環境變數（不納入版控）
└── README.md
```

---

## frontend/
```
frontend/
├── src/
│   ├── components/             # 共用元件
│   ├── pages/                  # 各主要頁面（測驗、報告、綜合分析等）
│   ├── api/                    # API 請求封裝
│   ├── utils/                  # 工具/常數
│   ├── styles/                 # 樣式
│   └── App.tsx                 # 入口
├── public/                     # 靜態資源
├── package.json                # 前端依賴
└── README.md
```

---

## docs/
- 00_project_brief_prd_summary.md   # PRD/專案簡報
- 02_system_architecture.md         # 系統架構設計
- 03_system_design_personality_analysis.md # 詳細設計（人格測驗與分析模組）
- 04_api_design_specification.md    # API 設計規範
- ...（其他設計/審查/會議記錄等）

---

## data/
- questions_mbti.json               # MBTI 題庫
- questions_disc.json               # DISC 題庫
- questions_big5.json               # 五大人格題庫
- questions_enneagram.json          # 九型人格題庫
- analysis_rules.json               # 分析規則/靜態建議
- ...（其他初始化資料）

---

## scripts/
- init_db.py                        # 初始化資料庫/匯入題庫
- backup_db.sh                      # 資料庫備份腳本
- ...（其他維運/部署腳本）

---

## tests/
- test_mbti.py                      # MBTI 相關測試
- test_disc.py                      # DISC 相關測試
- test_big5.py                      # 五大人格測試
- test_enneagram.py                 # 九型人格測試
- test_composite.py                 # 綜合分析測試
- ...

---

## .env.example
- 提供資料庫、Redis、API 相關環境變數範例

---

## README.md
- 專案簡介、安裝、啟動、資料夾結構說明 