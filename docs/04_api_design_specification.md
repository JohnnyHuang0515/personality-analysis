# API 設計規範 (API Design Specification) - 人格測驗與綜合分析平台

---

**文件版本 (Document Version):** `v1.0.0`

**最後更新 (Last Updated):** `2024-07-16`

**主要作者/設計師 (Lead Author/Designer):** `[請填寫]`

**審核者 (Reviewers):** `[請填寫]`

**狀態 (Status):** `草稿 (Draft)`

**相關 SD 文檔:** `[docs/03_system_design_personality_analysis.md]`

**OpenAPI/Swagger 定義文件:** `[待補充]`

---

## 1. 引言 (Introduction)
### 1.1 目的 (Purpose)
* 本文件為人格測驗與綜合分析平台 API 設計規範，提供前後端開發、測試、文件撰寫的統一接口契約。

### 1.2 目標讀者 (Target Audience)
* 前端/後端開發者、測試工程師、API 文件撰寫者。

### 1.3 API 風格與原則 (API Style and Principles)
* 採用 RESTful 風格，資源導向、無狀態、冪等性（查詢類）、一致性、易用性。
* 所有端點使用 HTTPS（本地可 http://localhost:8000）。
* 路徑名詞複數，動詞用於動作明確端點（如 submit）。

---

## 2. 通用設計約定 (General Design Conventions)
### 2.1 基本 URL (Base URL)
* 開發環境：`http://localhost:8000/api`

### 2.2 版本控制 (Versioning)
* URL 路徑版本控制，預設 v1（如 `/api/v1/`，可省略於 MVP）

### 2.3 請求格式 (Request Formats)
* `application/json` (UTF-8)

### 2.4 回應格式 (Response Formats)
* `application/json` (UTF-8)
* 通用回應結構：
```json
{
  "data": { /* 實際數據 */ },
  "meta": { /* 元數據，如分頁 */ }
}
```

### 2.5 日期與時間格式 (Date and Time Formats)
* ISO 8601，UTC

### 2.6 命名約定 (Naming Conventions)
* 路徑小寫、單詞用連字符，JSON 欄位用 snake_case

### 2.7 分頁 (Pagination)
* Offset/Limit 方式，查詢參數 `offset`、`limit`，預設 0/20

### 2.8 排序 (Sorting)
* 查詢參數 `sort_by`，如 `sort_by=-created_at`

### 2.9 過濾 (Filtering)
* 查詢參數直接用欄位名

---

## 3. 認證與授權 (Authentication and Authorization)
* MVP 本地部署階段可略，後續可加 JWT/OAuth2。

---

## 4. 錯誤處理 (Error Handling)
* 標準格式：
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "參數驗證失敗",
    "details": [ { "target": "user_id", "message": "必填" } ]
  }
}
```
* 常用狀態碼：200, 201, 400, 404, 500

---

## 5. 速率限制與配額 (Rate Limiting and Quotas)
* 本地部署階段可略，預留 429。

---

## 6. API 端點詳述 (API Endpoint Definitions)

### 6.1 題庫資源（Test Questions）
#### 6.1.1 取得指定類型所有題目
- `GET /api/test-questions?type=mbti|disc|big5|enneagram&offset=0&limit=20`
  - 描述：取得指定測驗類型的所有題目，支援分頁
  - 查詢參數：
    - `type` (必填)：測驗類型
    - `offset` (選填)：預設 0
    - `limit` (選填)：預設 20
  - 回應：
```json
{
  "data": [
    { "id": 1, "type": "mbti", "content": "...", "options": {"A": "...", "B": "..."} },
    ...
  ],
  "meta": { "total": 40, "offset": 0, "limit": 20 }
}
```

### 6.2 測驗作答（Test Answers）
#### 6.2.1 提交測驗答案
- `POST /api/test/{type}/submit`
  - 描述：提交指定類型測驗答案
  - 路徑參數：
    - `type`：mbti/disc/big5/enneagram
  - 請求體：
```json
{
  "user_id": 123,
  "answers": [ { "question_id": 1, "value": "A" }, ... ]
}
```
  - 回應：
```json
{
  "data": { "report_id": 1, "score": {"E": 12, "I": 8}, "result": "ENFP" }
}
```

#### 6.2.2 查詢用戶歷史作答紀錄
- `GET /api/test/{type}/answers?user_id=123`
  - 描述：查詢用戶歷史作答紀錄
  - 回應：
```json
{
  "data": [ { "question_id": 1, "value": "A", "created_at": "2024-07-16T12:00:00Z" }, ... ]
}
```

### 6.3 測驗報告（Test Reports）
#### 6.3.1 查詢單一測驗報告
- `GET /api/test/{type}/report?user_id=123`
  - 描述：查詢用戶單一測驗報告
  - 回應：
```json
{
  "data": { "report_id": 1, "score": {"E": 12, "I": 8}, "result": "ENFP", "created_at": "2024-07-16T12:00:00Z" }
}
```

#### 6.3.2 查詢綜合分析報告
- `GET /api/composite/report?user_id=123`
  - 描述：查詢用戶綜合分析報告
  - 回應：
```json
{
  "data": { "report_id": 2, "summary": "你的人格特質為...", "suggestions": "建議...", "created_at": "2024-07-16T12:00:00Z" }
}
```

---
### [補充] 綜合分析產生邏輯
* 綜合分析報告的產生依賴於用戶已完成所有單項測驗（MBTI、DISC、五大人格、九型人格）。
* 若有任一測驗未完成，則無法產生完整的綜合分析報告，API 將回傳提示訊息。

#### API 回應補充範例
若用戶未完成所有測驗，`GET /api/composite/report` 回應如下：
```json
{
  "data": null,
  "meta": {
    "status": "incomplete",
    "message": "請先完成所有測驗，才能產生綜合分析報告。"
  }
}
```
---

## 7. 資料模型/Schema 定義 (Data Models / Schema Definitions)
### 7.1 TestQuestionSchema
```json
{
  "id": 1,
  "type": "mbti",
  "content": "你在團體中通常...",
  "options": { "A": "主動發言", "B": "安靜傾聽" }
}
```
### 7.2 TestAnswerSchema
```json
{
  "question_id": 1,
  "value": "A",
  "created_at": "2024-07-16T12:00:00Z"
}
```
### 7.3 TestReportSchema
```json
{
  "report_id": 1,
  "score": { "E": 12, "I": 8 },
  "result": "ENFP",
  "created_at": "2024-07-16T12:00:00Z"
}
```
### 7.4 CompositeReportSchema
```json
{
  "report_id": 2,
  "summary": "你的人格特質為...",
  "suggestions": "建議...",
  "created_at": "2024-07-16T12:00:00Z"
}
```

---

## 8. 安全性考量 (Security Considerations)
* 僅本地存取，嚴格參數驗證，防止 SQL Injection/XSS。
* 所有錯誤皆記錄日誌。

---

## 9. 向後兼容性與棄用策略 (Backward Compatibility and Deprecation Policy)
* 增加新欄位時保證向後兼容，重大變更需升版。

---

## 10. 附錄 (Appendices)
### 10.1 請求/回應範例
* 見各端點下方 JSON 範例。

---
**文件審核記錄 (Review History):**
| 日期 | 審核人 | 版本 | 變更摘要 |
| :--- | :--- | :--- | :--- |
| 2024-07-16 | Gemini | v1.0.0 | 初稿建立 | 