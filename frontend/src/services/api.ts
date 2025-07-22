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

export const getQuestionsBatch = async (questionIds: number[]) => {
  const response = await api.post('/api/v1/questions/batch', {
    ids: questionIds
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
  // 由於後端只有綜合報告端點，我們直接獲取綜合報告
  // 綜合報告會自動包含所有測驗類型的分析
  const response = await api.get(`/api/v1/reports/${userId}`);
  return response.data;
};

export const getUserReport = async (userId: string, testType: string) => {
  try {
    // 由於後端只有綜合報告端點，我們獲取綜合報告並提取對應的測驗結果
    const response = await api.get(`/api/v1/reports/${userId}`);
    const comprehensiveReport = response.data;
    
    // 從綜合報告中提取對應測驗類型的詳細分析
    const testTypeLower = testType.toLowerCase();
    const detailedAnalysis = comprehensiveReport.detailed_analysis;
    
    let testReport;
    if (testTypeLower === 'mbti') {
      testReport = detailedAnalysis.mbti;
    } else if (testTypeLower === 'disc') {
      testReport = detailedAnalysis.disc;
    } else if (testTypeLower === 'big5') {
      testReport = detailedAnalysis.big5;
    } else if (testTypeLower === 'enneagram') {
      testReport = detailedAnalysis.enneagram;
    } else {
      throw new Error(`不支援的測驗類型: ${testType}`);
    }
    
    // 檢查是否有有效的報告數據
    if (!testReport || !testReport.scores) {
      throw new Error(`用戶 ${userId} 尚未完成 ${testType} 測驗`);
    }
    
    // 構建符合前端期望的報告格式
    return {
      user_id: userId,
      test_type: testType,
      report: {
        user_id: userId,
        test_type: testType,
        scores: testReport.scores,
        personality_type: testReport.personality_type || testReport.primary_style || testReport.primary_type,
        description: testReport.description,
        preference_strengths: testReport.preference_strengths,
        strengths: testReport.strengths,
        weaknesses: testReport.weaknesses,
        career_suggestions: testReport.career_suggestions || testReport.career_matches,
        communication_style: testReport.communication_style || testReport.interpersonal_style,
        work_style: testReport.work_style,
        development_suggestions: testReport.development_suggestions
      },
      generated_at: comprehensiveReport.report_generated_at,
      created_at: comprehensiveReport.report_generated_at
    };
  } catch (error: any) {
    // 如果是 404 錯誤或其他錯誤，提供更友好的錯誤信息
    if (error.response?.status === 404) {
      throw new Error(`用戶 ${userId} 尚未完成任何測驗，無法生成報告`);
    }
    throw error;
  }
};

export const getComprehensiveReport = async (userId: string) => {
  const response = await api.get(`/api/v1/reports/${userId}`);
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
  report: {
    user_id: string;
    test_type: string;
    scores: Record<string, number>;
    personality_type?: string;
    description?: string;
    preference_strengths?: Record<string, number>;
    strengths?: string[];
    weaknesses?: string[];
    career_suggestions?: string[];
    communication_style?: string;
    work_style?: string;
    development_suggestions?: string[];
  };
  generated_at: string;
  created_at?: string;
}

// API 服務對象
export const apiService = {
  getQuestions,
  getQuestionsBatch,
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
  getComprehensiveReport,
  healthCheck,
}; 