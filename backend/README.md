# 後端服務 - 綜合人格特質分析系統

基於 FastAPI 的現代化後端服務，提供完整的人格測驗 API 和時間記憶功能。

## 🚀 功能特色

### 核心功能
- **多種測驗類型**：MBTI、DISC、Enneagram 人格測驗
- **智能時間記憶**：簡化的暫停/恢復機制
- **會話管理**：完整的會話生命週期管理
- **答案處理**：即時答案提交和進度追蹤
- **報告生成**：個人化的人格特質分析報告

### 技術特色
- **FastAPI**：現代化的 Python Web 框架
- **SQLite**：輕量級資料庫
- **SQLAlchemy**：ORM 資料庫操作
- **Pydantic**：資料驗證和序列化
- **Alembic**：資料庫遷移管理

## 📁 專案結構

```
backend/
├── app/                    # 主要應用代碼
│   ├── api/               # API 路由
│   │   ├── answers.py     # 答案相關 API
│   │   ├── questions.py   # 題目相關 API
│   │   ├── reports.py     # 報告相關 API
│   │   └── sessions.py    # 會話相關 API
│   ├── models/            # 資料模型
│   │   ├── answer.py      # 答案模型
│   │   ├── personality.py # 人格模型
│   │   ├── question.py    # 題目模型
│   │   └── report.py      # 報告模型
│   ├── schemas/           # Pydantic 模式
│   │   ├── answer.py      # 答案模式
│   │   ├── question.py    # 題目模式
│   │   └── report.py      # 報告模式
│   ├── services/          # 業務邏輯
│   │   └── analysis.py    # 分析服務
│   └── core/              # 核心配置
│       └── database.py    # 資料庫配置
├── data/                  # 題庫資料
│   └── personality_questions.py
├── tests/                 # 測試檔案
│   └── README.md
├── migrations/            # 資料庫遷移
├── config/                # 配置文件
├── scripts/               # 工具腳本
└── main.py               # 應用入口
```

## 🛠️ 快速開始

### 環境要求
- Python 3.8+
- pip 或 poetry

### 1. 安裝依賴
```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 poetry
poetry install
```

### 2. 初始化資料庫
```bash
python init_db.py
```

### 3. 啟動服務
```bash
# 開發模式
python main.py

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 訪問 API
- API 文檔：http://localhost:8000/docs
- 健康檢查：http://localhost:8000/health

## 🧪 測試

### 運行所有測試
```bash
python run_tests.py
```

### 單獨測試
```bash
# 時間記憶功能測試
python test_simplified_time.py

# 查看時間記憶機制說明
python explain_time_memory.py

# 完整 API 測試
python test_complete_api.py
```

## 📚 API 文檔

### 主要端點

#### 會話管理
- `POST /api/v1/sessions/create` - 創建新會話
- `GET /api/v1/sessions/{user_id}/{test_type}/latest` - 獲取最新會話
- `POST /api/v1/sessions/{session_id}/pause` - 暫停會話
- `POST /api/v1/sessions/{session_id}/resume` - 恢復會話
- `POST /api/v1/sessions/{session_id}/update-time` - 更新會話時間

#### 題目管理
- `GET /api/v1/questions/{test_type}` - 獲取題目
- `GET /api/v1/questions/types` - 獲取測驗類型

#### 答案處理
- `POST /api/v1/answers/submit` - 提交答案
- `GET /api/v1/answers/{user_id}` - 獲取用戶答案

#### 報告生成
- `POST /api/v1/reports/generate` - 生成報告
- `GET /api/v1/reports/{user_id}/{test_type}` - 獲取報告

## 🔧 開發指南

### 時間記憶機制

系統採用簡化的時間記憶設計：

```python
# 暫停時保存時間
@router.post("/sessions/{session_id}/pause")
def pause_session(session_id: int, data: Optional[Dict[str, Any]] = None):
    elapsed_seconds = data.get("elapsed_seconds", total_time_seconds)
    cursor.execute(
        "UPDATE test_session SET total_time_seconds = ? WHERE id = ?",
        (elapsed_seconds, session_id)
    )
```

### 資料庫模型

```python
class TestSession(Base):
    __tablename__ = "test_session"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(64), nullable=False)
    test_type = Column(String(16), nullable=False)
    total_time_seconds = Column(Integer, default=0)
    status = Column(String(16), default='in_progress')
    started_at = Column(DateTime, default=datetime.utcnow)
    paused_at = Column(DateTime)
```

### 環境變數

創建 `.env` 檔案：
```env
DATABASE_URL=sqlite:///./personality_test.db
API_KEY=your-api-key
DEBUG=True
```

## 🚀 部署

### 生產環境
```bash
# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python init_db.py

# 啟動服務
python main.py --host 0.0.0.0 --port 8000
```

### Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python init_db.py

EXPOSE 8000
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 監控

### 健康檢查
```bash
curl http://localhost:8000/health
```

### 日誌查看
```bash
# 查看應用日誌
tail -f logs/app.log

# 查看錯誤日誌
tail -f logs/error.log
```

## 🔒 安全性

- API 金鑰驗證
- 輸入資料驗證
- SQL 注入防護
- CORS 配置
- 速率限制

## 🤝 貢獻

1. Fork 專案
2. 創建功能分支
3. 提交更改
4. 推送到分支
5. 開啟 Pull Request

## 📄 授權

本專案採用 MIT 授權條款

---

**最後更新**：2025-07-19  
**版本**：v1.0.0
