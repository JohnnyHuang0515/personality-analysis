import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Question {
  id: number;
  text: string;
  category: string;
  test_type: string;
  options: string[];
  weight: Record<string, Record<string, number>>;
}

export interface TestSubmission {
  user_id: string;
  test_type: string;
  answers: Array<{
    question_id: number;
    answer: string;
  }>;
}

export interface Report {
  user_id: string;
  test_type: string;
  report: any;
  generated_at: string;
}

export const apiService = {
  // 健康檢查
  healthCheck: () => api.get('/health'),

  // 取得所有測驗類型
  getTestTypes: () => api.get('/api/v1/questions/types'),

  // 取得特定測驗類型的題目
  getQuestions: (testType: string) => 
    api.get<{ questions: Question[]; total: number; test_type: string }>(`/api/v1/questions/${testType}`),

  // 提交測驗答案
  submitAnswers: (submission: TestSubmission) => 
    api.post('/api/v1/answers/submit', submission),

  // 取得用戶答案
  getUserAnswers: (userId: string) => 
    api.get(`/api/v1/answers/${userId}`),

  // 生成報告
  generateReport: (userId: string, testType: string) => 
    api.get<Report>(`/api/v1/reports/${userId}/${testType}`),

  // 取得用戶所有報告
  getUserReports: (userId: string) => 
    api.get(`/api/v1/reports/${userId}`),

  // 生成綜合報告
  generateCompositeReport: (userId: string) => 
    api.get(`/api/v1/reports/${userId}/composite`),
};

export default api; 