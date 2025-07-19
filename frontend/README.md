# 前端應用 - 綜合人格特質分析系統

基於 React + TypeScript 的現代化前端應用，提供直觀易用的人格測驗介面。

## 🚀 功能特色

### 核心功能
- **多種測驗類型**：MBTI、DISC、Enneagram 人格測驗
- **智能時間記憶**：暫停/恢復功能，自動保存進度
- **即時進度追蹤**：視覺化進度條和計時器
- **響應式設計**：支援桌面和移動設備
- **現代化UI**：基於 Tailwind CSS 的美觀介面

### 技術特色
- **React 18**：最新的 React 版本
- **TypeScript**：類型安全的 JavaScript
- **Tailwind CSS**：實用優先的 CSS 框架
- **React Router**：客戶端路由
- **Axios**：HTTP 客戶端

## 📁 專案結構

```
frontend/
├── public/                  # 靜態資源
│   ├── index.html          # HTML 模板
│   └── favicon.ico         # 網站圖標
├── src/                    # 主要程式碼
│   ├── components/         # React 組件
│   │   ├── Header.tsx      # 頁面標題組件
│   │   └── TestCard.tsx    # 測驗卡片組件
│   ├── pages/              # 頁面組件
│   │   ├── HomePage.tsx    # 首頁
│   │   ├── TestPage.tsx    # 測驗頁面
│   │   └── ReportPage.tsx  # 報告頁面
│   ├── services/           # API 服務
│   │   └── api.ts          # API 調用函數
│   ├── contexts/           # React Context
│   │   └── TestContext.tsx # 測驗狀態管理
│   ├── App.tsx             # 主應用組件
│   └── index.tsx           # 應用入口
├── package.json            # 依賴配置
├── tsconfig.json           # TypeScript 配置
├── tailwind.config.js      # Tailwind CSS 配置
└── postcss.config.js       # PostCSS 配置
```

## 🛠️ 快速開始

### 環境要求
- Node.js 16+
- npm 或 yarn

### 1. 安裝依賴
```bash
npm install
# 或
yarn install
```

### 2. 啟動開發服務器
```bash
npm start
# 或
yarn start
```

### 3. 訪問應用
- 開發環境：http://localhost:3000
- 確保後端服務運行在 http://localhost:8000

## 🧪 測試

### 運行測試
```bash
npm test
# 或
yarn test
```

### 構建生產版本
```bash
npm run build
# 或
yarn build
```

## 🔧 開發指南

### 時間記憶功能

前端實現了簡化的時間記憶機制：

```typescript
// 頁面離開時保存時間
const handleBeforeUnload = (event: BeforeUnloadEvent) => {
  if (sessionId) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `/api/v1/sessions/${sessionId}/pause`, false);
    xhr.send(JSON.stringify({ elapsed_seconds: timeSpent }));
  }
};

// 頁面顯示時恢復時間
const handleVisibilityChange = async () => {
  if (!document.hidden && sessionId) {
    const sessionData = await apiService.getLatestSession(userId, testType);
    setTimeSpent(sessionData.elapsed_seconds);
  }
};
```

### 狀態管理

使用 React Context 管理測驗狀態：

```typescript
const TestContext = createContext<TestContextType | undefined>(undefined);

export const TestProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentTest, setCurrentTest] = useState<TestType | null>(null);
  const [testProgress, setTestProgress] = useState<TestProgress | null>(null);
  
  return (
    <TestContext.Provider value={{ currentTest, setCurrentTest, testProgress, setTestProgress }}>
      {children}
    </TestContext.Provider>
  );
};
```

### API 服務

封裝的 API 調用函數：

```typescript
export const apiService = {
  getQuestions: (testType: string) => api.get(`/api/v1/questions/${testType}`),
  createSession: (userId: string, testType: string, questionIds: number[]) => 
    api.post('/api/v1/sessions/create', { user_id: userId, test_type: testType, question_ids: questionIds }),
  pauseSession: (sessionId: number, data?: { elapsed_seconds: number }) => 
    api.post(`/api/v1/sessions/${sessionId}/pause`, data),
  // ... 其他 API 函數
};
```

## 🎨 UI 組件

### 測驗卡片組件
```typescript
interface TestCardProps {
  testType: TestType;
  title: string;
  description: string;
  questionCount: number;
  estimatedTime: string;
  onStart: () => void;
}
```

### 進度條組件
```typescript
const ProgressBar: React.FC<{ progress: number }> = ({ progress }) => (
  <div className="w-full bg-gray-200 rounded-full h-2">
    <div 
      className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
      style={{ width: `${progress}%` }}
    />
  </div>
);
```

## 🚀 部署

### 生產構建
```bash
npm run build
```

### 靜態文件部署
構建後的 `build/` 目錄包含所有靜態文件，可以部署到：
- Netlify
- Vercel
- GitHub Pages
- 任何靜態文件服務器

### Docker 部署
```dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

## 🔧 配置

### 環境變數
創建 `.env` 檔案：
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### Tailwind CSS 配置
```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 500: '#3B82F6' },
        secondary: { 500: '#8B5CF6' },
      }
    }
  },
  plugins: [],
}
```

## 📱 響應式設計

應用支援多種設備尺寸：
- **桌面**：完整功能，最佳體驗
- **平板**：適配觸控操作
- **手機**：垂直佈局，觸控優化

## 🔒 安全性

- API 請求驗證
- 輸入資料清理
- XSS 防護
- CSRF 保護

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