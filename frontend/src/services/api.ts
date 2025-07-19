import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 題目相關 API
export const getQuestions = async (testType: string, random: boolean = false) => {
  const response = await api.get(`/api/v1/questions/${testType}`, {
    params: { random }
  });
  return response.data;
};

export const getTestTypes = async () => {
  const response = await api.get('/api/v1/questions/types');
  return response.data;
};

// 會話管理 API
export const createSession = async (userId: string, testType: string, questionIds?: number[]) => {
  const response = await api.post('/api/v1/sessions/create', {
    user_id: userId,
    test_type: testType,
    question_ids: questionIds,
  });
  return response.data;
};

export const getLatestSession = async (userId: string, testType: string) => {
  const response = await api.get(`/api/v1/sessions/${userId}/${testType}/latest`);
  return response.data;
};

export const pauseSession = async (sessionId: number, data?: { elapsed_seconds: number }) => {
  const response = await api.post(`/api/v1/sessions/${sessionId}/pause`, data);
  return response.data;
};

export const resumeSession = async (sessionId: number) => {
  const response = await api.post(`/api/v1/sessions/${sessionId}/resume`);
  return response.data;
};

export const updateSessionTime = async (sessionId: number, elapsedSeconds: number) => {
  const response = await api.post(`/api/v1/sessions/${sessionId}/update-time`, {
    elapsed_seconds: elapsedSeconds
  });
  return response.data;
};

export const getAllSessions = async (userId: string) => {
  const response = await api.get(`/api/v1/sessions/${userId}/all`);
  return response.data;
};

// 答案提交 API
export const submitAnswers = async (data: {
  user_id: string;
  test_type: string;
  answers: Array<{ question_id: number; answer: string }>;
  session_id?: number;
}) => {
  const response = await api.post('/api/v1/answers/submit', data);
  return response.data;
};

export const getUserAnswers = async (userId: string) => {
  const response = await api.get(`/api/v1/answers/${userId}`);
  return response.data;
};

export const getUserAnswersByType = async (userId: string, testType: string) => {
  const response = await api.get(`/api/v1/answers/${userId}/${testType}`);
  return response.data;
};

// 報告生成 API
export const generateReport = async (userId: string, testType: string) => {
  const response = await api.post('/api/v1/reports/generate', {
    user_id: userId,
    test_type: testType,
  });
  return response.data;
};

export const getUserReport = async (userId: string, testType: string) => {
  const response = await api.get(`/api/v1/reports/${userId}/${testType}`);
  return response.data;
};

// 健康檢查
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// 類型定義
export interface Question {
  id: number;
  text: string;
  category: string;
  test_type: string;
  options: string[];
  weight: any;
}

export interface Session {
  session_id: number;
  user_id: string;
  test_type: string;
  total_questions: number;
  question_ids: string[];
  status: string;
  message: string;
}

export interface SessionProgress {
  has_session: boolean;
  session_id?: number;
  user_id?: string;
  test_type?: string;
  total_questions?: number;
  answered_count?: number;
  progress_percentage?: number;
  next_question_index?: number;
  status?: string;
  started_at?: string;
  finished_at?: string;
  elapsed_seconds?: number;
  question_ids?: string[];
  answered_questions?: Record<string, { answer: string; answered_at: string }>;
  message?: string;
}

export interface Answer {
  id: number;
  user_id: string;
  question_id: number;
  answer: string;
  created_at: string;
}

export interface Report {
  user_id: string;
  test_type: string;
  total_questions: number;
  analysis: string;
  recommendations: string[];
  generated_at: string;
  created_at?: string;
}

// API 服務對象
export const apiService = {
  getQuestions,
  getTestTypes,
  createSession,
  getLatestSession,
  pauseSession,
  resumeSession,
  updateSessionTime,
  getAllSessions,
  submitAnswers,
  getUserAnswers,
  getUserAnswersByType,
  generateReport,
  getUserReport,
  healthCheck,
}; 