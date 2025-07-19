import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';

export interface TestState {
  currentTest: string | null;
  currentQuestion: number;
  answers: Record<number, string>;
  isCompleted: boolean;
  userId: string;
  totalQuestions: number;
}

type TestAction =
  | { type: 'START_TEST'; payload: { testType: string; userId: string; totalQuestions: number } }
  | { type: 'ANSWER_QUESTION'; payload: { questionId: number; answer: string } }
  | { type: 'NEXT_QUESTION' }
  | { type: 'PREV_QUESTION' }
  | { type: 'COMPLETE_TEST' }
  | { type: 'RESET_TEST' }
  | { type: 'LOAD_PROGRESS'; payload: TestState };

const initialState: TestState = {
  currentTest: null,
  currentQuestion: 0,
  answers: {},
  isCompleted: false,
  userId: '',
  totalQuestions: 0,
};

// localStorage 鍵名
const STORAGE_KEY = 'personality_test_progress';

// 保存進度到 localStorage
const saveProgress = (state: TestState) => {
  if (state.currentTest && !state.isCompleted) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }
};

// 從 localStorage 載入進度
const loadProgress = (): TestState | null => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : null;
  } catch (error) {
    console.error('載入進度失敗:', error);
    return null;
  }
};

// 清除進度
const clearProgress = () => {
  localStorage.removeItem(STORAGE_KEY);
};

function testReducer(state: TestState, action: TestAction): TestState {
  let newState: TestState;

  switch (action.type) {
    case 'START_TEST':
      newState = {
        ...state,
        currentTest: action.payload.testType,
        currentQuestion: 0,
        answers: {},
        isCompleted: false,
        userId: action.payload.userId,
        totalQuestions: action.payload.totalQuestions,
      };
      break;
    
    case 'ANSWER_QUESTION':
      newState = {
        ...state,
        answers: {
          ...state.answers,
          [action.payload.questionId]: action.payload.answer,
        },
      };
      break;
    
    case 'NEXT_QUESTION':
      newState = {
        ...state,
        currentQuestion: state.currentQuestion + 1,
      };
      break;
    
    case 'PREV_QUESTION':
      newState = {
        ...state,
        currentQuestion: Math.max(0, state.currentQuestion - 1),
      };
      break;
    
    case 'COMPLETE_TEST':
      newState = {
        ...state,
        isCompleted: true,
      };
      clearProgress(); // 完成測驗後清除進度
      break;
    
    case 'RESET_TEST':
      newState = initialState;
      clearProgress(); // 重置測驗後清除進度
      break;

    case 'LOAD_PROGRESS':
      newState = action.payload;
      break;
    
    default:
      return state;
  }

  // 每次狀態更新後保存進度
  saveProgress(newState);
  return newState;
}

interface TestContextType {
  state: TestState;
  dispatch: React.Dispatch<TestAction>;
  hasUnfinishedTest: () => boolean;
  getProgressPercentage: () => number;
  getAnsweredCount: () => number;
  getCurrentQuestionAnswer: (questionId: number) => string | undefined;
  isQuestionAnswered: (questionId: number) => boolean;
}

const TestContext = createContext<TestContextType | undefined>(undefined);

export function TestProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(testReducer, initialState);

  // 初始化時載入進度
  useEffect(() => {
    const savedProgress = loadProgress();
    if (savedProgress && !savedProgress.isCompleted) {
      dispatch({ type: 'LOAD_PROGRESS', payload: savedProgress });
    }
  }, []);

  // 檢查是否有未完成的測驗
  const hasUnfinishedTest = (): boolean => {
    return !!(state.currentTest && !state.isCompleted && Object.keys(state.answers).length > 0);
  };

  // 計算進度百分比
  const getProgressPercentage = (): number => {
    // 固定使用30題計算進度
    const FIXED_TOTAL_QUESTIONS = 30;
    const answeredCount = Object.keys(state.answers).length;
    return Math.round((answeredCount / FIXED_TOTAL_QUESTIONS) * 100);
  };

  // 獲取已回答題目數量
  const getAnsweredCount = (): number => {
    return Object.keys(state.answers).length;
  };

  // 獲取當前題目的答案
  const getCurrentQuestionAnswer = (questionId: number): string | undefined => {
    return state.answers[questionId];
  };

  // 檢查題目是否已回答
  const isQuestionAnswered = (questionId: number): boolean => {
    return questionId in state.answers;
  };

  const contextValue: TestContextType = {
    state,
    dispatch,
    hasUnfinishedTest,
    getProgressPercentage,
    getAnsweredCount,
    getCurrentQuestionAnswer,
    isQuestionAnswered,
  };

  return (
    <TestContext.Provider value={contextValue}>
      {children}
    </TestContext.Provider>
  );
}

export function useTest() {
  const context = useContext(TestContext);
  if (context === undefined) {
    throw new Error('useTest must be used within a TestProvider');
  }
  return context;
} 