import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, BarChart3 } from 'lucide-react';
import { apiService } from '../services/api';

interface Question {
  id: number;
  question_text: string;
  options: string[];
  test_type: string;
}

interface SessionProgress {
  answered_count: number;
  progress_percentage: number;
  total_time_seconds: number;
}

const TestPage: React.FC = () => {
  const { testType } = useParams<{ testType: string }>();
  const navigate = useNavigate();
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeSpent, setTimeSpent] = useState(0);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [sessionProgress, setSessionProgress] = useState<SessionProgress | null>(null);
  const [hasExistingSession, setHasExistingSession] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [restarting, setRestarting] = useState(false);

  // 獲取標準化的測驗類型
  const getNormalizedTestType = (type: string) => {
    const typeMap: Record<string, string> = {
      'mbti': 'MBTI',
      'disc': 'DISC',
      'enneagram': 'ENNEAGRAM',
      'big5': 'BIG5'
    };
    return typeMap[type.toLowerCase()] || type.toUpperCase();
  };

  // 獲取或生成用戶ID
  const getUserId = () => {
    let userId = localStorage.getItem('personality_test_user_id');
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('personality_test_user_id', userId);
    }
    return userId;
  };

  const normalizedTestType = getNormalizedTestType(testType || '');
  const userId = getUserId();
  const currentQuestion = questions[currentQuestionIndex];
  const answeredCount = Object.keys(answers).length;
  const progress = questions.length > 0 ? (answeredCount / questions.length) * 100 : 0;

  // 獲取題目和會話
  useEffect(() => {
    const fetchQuestionsAndSession = async () => {
      if (!normalizedTestType) {
        setError('無效的測驗類型');
        setLoading(false);
        return;
      }

      try {
                 // 獲取題目
         const questionsResponse = await apiService.getQuestions(normalizedTestType!);
         const questionsData = questionsResponse.questions || questionsResponse;
         // 轉換字段名稱以匹配前端期望的格式
         const formattedQuestions = questionsData.map((q: any) => ({
           id: q.id,
           question_text: q.text,
           options: q.options,
           test_type: q.test_type
         }));
         setQuestions(formattedQuestions);

         // 檢查是否有進行中的會話
         try {
           const sessionResponse = await apiService.getLatestSession(userId, normalizedTestType!);
           const sessionData = sessionResponse;
          
          if (sessionData && sessionData.status === 'in_progress') {
            setSessionId(sessionData.id);
            setTimeSpent(sessionData.total_time_seconds || 0);
            setHasExistingSession(true);
            
            // 獲取已答題目
            const answersResponse = await apiService.getUserAnswers(userId);
            const answersData = answersResponse.data || answersResponse;
            
            if (answersData && answersData.length > 0) {
              const answersMap: Record<number, string> = {};
              answersData.forEach((answer: any) => {
                answersMap[answer.question_id] = answer.answer;
              });
              setAnswers(answersMap);
              
              // 計算進度
              const answeredCount = Object.keys(answersMap).length;
              const progressPercentage = (answeredCount / questionsData.length) * 100;
              setSessionProgress({
                answered_count: answeredCount,
                progress_percentage: progressPercentage,
                total_time_seconds: sessionData.total_time_seconds || 0
              });
              
              // 設置當前題目索引為下一個未答題目
              const answeredQuestionIds = Object.keys(answersMap).map(Number);
              const nextUnansweredIndex = questionsData.findIndex((q: Question) => 
                !answeredQuestionIds.includes(q.id)
              );
              if (nextUnansweredIndex !== -1) {
                setCurrentQuestionIndex(nextUnansweredIndex);
              }
            }
          }
        } catch (sessionError) {
          console.log('沒有找到進行中的會話，將創建新會話');
        }

        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch questions:', error);
        setError('載入題目失敗，請重試');
        setLoading(false);
      }
    };

    fetchQuestionsAndSession();
  }, [normalizedTestType, userId]);

  // 計時器效果
  useEffect(() => {
    if (!loading && sessionId) {
      const timer = setInterval(() => {
        setTimeSpent(prev => prev + 1);
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [loading, sessionId]);

  // 頁面離開時保存時間
  useEffect(() => {
    const handleBeforeUnload = (event: BeforeUnloadEvent) => {
      if (sessionId) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/api/v1/sessions/${sessionId}/pause`, false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ elapsed_seconds: timeSpent }));
      }
    };

    const handleVisibilityChange = async () => {
      if (document.hidden && sessionId) {
        try {
          await apiService.pauseSession(sessionId, { elapsed_seconds: timeSpent });
        } catch (error) {
          console.error('暫停會話失敗:', error);
        }
      } else if (!document.hidden && sessionId) {
        try {
          const sessionResponse = await apiService.getLatestSession(userId, normalizedTestType!);
          const sessionData = sessionResponse;
          if (sessionData) {
            setTimeSpent(sessionData.total_time_seconds || 0);
          }
        } catch (error) {
          console.error('恢復會話失敗:', error);
        }
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [sessionId, timeSpent, userId, normalizedTestType]);

  // 創建會話
  useEffect(() => {
    const createSession = async () => {
      if (!sessionId && questions.length > 0 && !loading) {
        try {
          const questionIds = questions.map(q => q.id);
          const response = await apiService.createSession(userId, normalizedTestType!, questionIds);
          setSessionId(response.session_id);
        } catch (error) {
          console.error('創建會話失敗:', error);
        }
      }
    };

    createSession();
  }, [sessionId, questions, loading, userId, normalizedTestType]);

  // 處理答案選擇
  const handleAnswer = (answer: string) => {
    if (!currentQuestion) return;

    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: answer
    }));

    // 自動保存答案到後端
    saveAnswerToBackend(currentQuestion.id, answer);
  };

     // 保存答案到後端
   const saveAnswerToBackend = async (questionId: number, answer: string) => {
     if (!sessionId) return;

     try {
       await apiService.submitAnswers({
         user_id: userId,
         test_type: normalizedTestType!,
         answers: [{ question_id: questionId, answer }],
         session_id: sessionId
       });
     } catch (error) {
       console.error('保存答案失敗:', error);
     }
   };

  // 下一題
  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  // 上一題
  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  // 提交測驗
  const handleSubmit = async () => {
    if (!normalizedTestType) {
      alert('無法提交測驗，因為測驗類型未指定。');
      return;
    }

    if (!canSubmit) {
      alert(`請至少完成 ${Math.ceil(questions.length * 0.8)} 題才能提交測驗。`);
      return;
    }

    setSubmitting(true);
    try {
      // 生成報告
      await apiService.generateReport(userId, normalizedTestType!);
      
      // 導航到報告頁面
      navigate(`/report/${userId}/${normalizedTestType}`);
    } catch (error) {
      console.error('Failed to submit answers:', error);
      alert('提交失敗，請重試');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRestartTest = async () => {
    if (!normalizedTestType) {
      alert('無法重新開始測驗，因為測驗類型未指定。');
      return;
    }

    // 確認用戶是否真的要重新開始
    const confirmed = window.confirm(
      '確定要重新開始測驗嗎？\n\n' +
      '⚠️ 這將清除：\n' +
      '• 所有已答題目\n' +
      '• 當前進度\n' +
      '• 計時記錄\n\n' +
      '此操作無法撤銷！'
    );
    if (!confirmed) {
      return;
    }

    setRestarting(true);
    try {
      // 如果有進行中的會話，先暫停它
      if (sessionId) {
        try {
          await apiService.pauseSession(sessionId);
          console.log('已暫停當前會話');
        } catch (error) {
          console.error('暫停會話失敗:', error);
        }
      }

      // 清除本地狀態
      setAnswers({});
      setCurrentQuestionIndex(0);
      setTimeSpent(0);
      setSessionProgress(null);
      setSessionId(null);
      setHasExistingSession(false);

      // 清除 localStorage 中的用戶 ID，強制生成新的用戶 ID
      localStorage.removeItem('personality_test_user_id');

      // 重新載入頁面以完全重置狀態
      window.location.reload();
    } catch (error) {
      console.error('重新開始測驗失敗:', error);
      alert('重新開始測驗失敗，請重試。');
      setRestarting(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="text-gray-600">正在載入測驗...</p>
          <p className="text-sm text-gray-500">測驗類型: {normalizedTestType}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h2 className="text-xl font-semibold text-red-800 mb-2">載入失敗</h2>
          <p className="text-red-600 mb-4">{error}</p>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">測驗類型: {normalizedTestType}</p>
            <p className="text-sm text-gray-600">用戶 ID: {userId}</p>
          </div>
          <div className="mt-4 space-x-4">
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              重新載入
            </button>
            <button
              onClick={() => navigate('/')}
              className="btn-secondary"
            >
              返回首頁
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-yellow-800 mb-2">沒有找到題目</h2>
          <p className="text-yellow-600 mb-4">
            載入了 {questions.length} 個題目，但當前題目索引 {currentQuestionIndex} 超出範圍
          </p>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">測驗類型: {normalizedTestType}</p>
            <p className="text-sm text-gray-600">題目總數: {questions.length}</p>
            <p className="text-sm text-gray-600">當前索引: {currentQuestionIndex}</p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="btn-primary mt-4"
          >
            返回首頁
          </button>
        </div>
      </div>
    );
  }

  const isAnswered = answers[currentQuestion.id];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const canSubmit = answeredCount >= questions.length * 0.8; // 至少完成80%

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors duration-200"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>返回首頁</span>
          </button>
          <div className="flex items-center space-x-4">
            <button
              onClick={handleRestartTest}
              disabled={restarting}
              className="flex items-center space-x-2 text-red-600 hover:text-red-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              title="重新開始測驗"
            >
              {restarting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
                  <span>重新開始中...</span>
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>重新測驗</span>
                </>
              )}
            </button>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{formatTime(timeSpent)}</span>
              </div>
              <div className="flex items-center space-x-1">
                <BarChart3 className="w-4 h-4" />
                <span>{answeredCount}/{questions.length}</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* 會話狀態提示 */}
        {hasExistingSession && sessionProgress && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-blue-800 text-sm">
              📚 歡迎回來！您上次完成了 {sessionProgress.answered_count} 題 
              ({Math.round(sessionProgress.progress_percentage!)}%)，現在從第 {currentQuestionIndex + 1} 題繼續。
            </p>
          </div>
        )}
        
        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-gray-500">
              題目 {currentQuestionIndex + 1} / {questions.length}
            </span>
            {isAnswered && (
              <span className="text-sm text-green-600 bg-green-50 px-2 py-1 rounded-full">
                ✓ 已答題
              </span>
            )}
          </div>
          
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            {currentQuestion.question_text}
          </h2>

          {/* Options */}
          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswer(option)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all duration-200 ${
                  isAnswered === option
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <span className="font-medium">{option}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between pt-6 border-t border-gray-200">
          <button
            onClick={handlePrev}
            disabled={currentQuestionIndex === 0}
            className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-primary-600 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>上一題</span>
          </button>

          <div className="flex items-center space-x-4">
            {isLastQuestion ? (
              <button
                onClick={handleSubmit}
                disabled={!canSubmit || submitting}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>提交中...</span>
                  </div>
                ) : (
                  '提交測驗'
                )}
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={currentQuestionIndex === questions.length - 1}
                className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-primary-600 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>下一題</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Submit Warning */}
      {isLastQuestion && !canSubmit && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800 text-sm">
            ⚠️ 請至少完成 {Math.ceil(questions.length * 0.8)} 題才能提交測驗。
            目前已完成 {answeredCount} 題。
          </p>
        </div>
      )}
    </div>
  );
};

export default TestPage;