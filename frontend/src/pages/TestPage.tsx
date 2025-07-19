import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, BarChart3 } from 'lucide-react';
import { apiService } from '../services/api';
import { useTest } from '../contexts/TestContext';

interface Question {
  id: number;
  question_text: string;
  options: string[];
  test_type: string;
}

const TestPage: React.FC = () => {
  const { testType } = useParams<{ testType: string }>();
  const navigate = useNavigate();
  const { state, dispatch, getAnsweredCount, getCurrentQuestionAnswer, isQuestionAnswered } = useTest();
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const isRestarting = useRef(false);

  // 獲取標準化的測驗類型 - 映射到後端支援的類型
  const getNormalizedTestType = (type: string) => {
    const typeMap: Record<string, string> = {
      'mbti': 'MBTI',
      'disc': 'DISC',
      'enneagram': 'enneagram',
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
  
  const currentQuestion = questions[state.currentQuestion];
  const answeredCount = getAnsweredCount();
  const FIXED_TOTAL_QUESTIONS = 30;
  const progress = (answeredCount / FIXED_TOTAL_QUESTIONS) * 100;

  // 獲取題目
  useEffect(() => {
    const fetchQuestions = async () => {
      if (!normalizedTestType) {
        setError('無效的測驗類型');
        setLoading(false);
        return;
      }

      // 如果正在重新測驗，不要重新載入固定題目
      if (isRestarting.current) {
        return;
      }

      try {
        // 預設使用固定題目（不隨機）
        const questionsResponse = await apiService.getQuestions(normalizedTestType, false);
        const questionsData = questionsResponse.questions || questionsResponse;
        
        const formattedQuestions = questionsData.map((q: any) => ({
          id: q.id,
          question_text: q.text,
          options: q.options,
          test_type: q.test_type
        }));
        
        setQuestions(formattedQuestions);

        // 如果 TestContext 中沒有當前測驗，則開始新測驗
        if (state.currentTest !== normalizedTestType) {
          dispatch({
            type: 'START_TEST',
            payload: {
              testType: normalizedTestType,
              userId: userId,
              totalQuestions: FIXED_TOTAL_QUESTIONS
            }
          });
        }

        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch questions:', error);
        setError(`載入題目失敗，請重試。錯誤: ${error instanceof Error ? error.message : '未知錯誤'}`);
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [normalizedTestType, userId, state.currentTest, dispatch]);

  // 處理答案選擇
  const handleAnswer = (answer: string) => {
    if (!currentQuestion) return;

    dispatch({
      type: 'ANSWER_QUESTION',
      payload: {
        questionId: currentQuestion.id,
        answer: answer
      }
    });
  };

  // 下一題
  const handleNext = () => {
    if (state.currentQuestion < questions.length - 1) {
      dispatch({ type: 'NEXT_QUESTION' });
    }
  };

  // 上一題
  const handlePrev = () => {
    if (state.currentQuestion > 0) {
      dispatch({ type: 'PREV_QUESTION' });
    }
  };

  // 提交測驗
  const handleSubmit = async () => {
    if (submitting) return;
    setSubmitting(true);

    try {
      // 提交所有答案到後端
      const answersArray = Object.entries(state.answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId),
        answer: answer
      }));

      await apiService.submitAnswers({
        user_id: userId,
        test_type: testType || '', // 使用實際的測驗類型 (mbti, disc, big5, enneagram)
        answers: answersArray,
        session_id: undefined
      });

      // 完成測驗
      dispatch({ type: 'COMPLETE_TEST' });

      // 導航到報告頁面 - 使用實際的測驗類型
      navigate(`/report/${userId}/${testType || ''}`);
    } catch (error) {
      console.error('提交測驗失敗:', error);
      alert('提交測驗失敗，請重試。');
    } finally {
      setSubmitting(false);
    }
  };

  // 重新開始測驗（隨機新題目）
  const handleRestartTest = async () => {
    setLoading(true);
    setError(null); // 清除錯誤狀態
    isRestarting.current = true; // 標記正在重新測驗
    
    try {
      // 先重置 TestContext
      dispatch({ type: 'RESET_TEST' });
      
      // 清空當前題目狀態
      setQuestions([]);
      
      // 使用隨機參數重新獲取題目
      const questionsResponse = await apiService.getQuestions(normalizedTestType, true);
      const questionsData = questionsResponse.questions || questionsResponse;
      
      const formattedQuestions = questionsData.map((q: any) => ({
        id: q.id,
        question_text: q.text,
        options: q.options,
        test_type: q.test_type
      }));
      
      // 設置新題目
      setQuestions(formattedQuestions);
      
      // 開始新測驗
      dispatch({
        type: 'START_TEST',
        payload: {
          testType: normalizedTestType,
          userId: userId,
          totalQuestions: FIXED_TOTAL_QUESTIONS
        }
      });
      
      setLoading(false);
      isRestarting.current = false; // 重置標記
    } catch (error) {
      console.error('重新開始測驗失敗:', error);
      setError(`重新開始測驗失敗，請重試。錯誤: ${error instanceof Error ? error.message : '未知錯誤'}`);
      setLoading(false);
      isRestarting.current = false; // 重置標記
    }
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
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <div className="text-red-500 text-xl">❌</div>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            重新載入
          </button>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <div className="text-red-500 text-xl">❌</div>
          <p className="text-red-600">找不到當前題目</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* 進度條 */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">
            進度: {answeredCount} / {FIXED_TOTAL_QUESTIONS} 題
          </span>
          <span className="text-sm text-gray-600">{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* 題目卡片 */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              <ArrowLeft size={20} />
              <span>返回首頁</span>
            </button>
          </div>
          <div className="text-sm text-gray-500">
            第 {state.currentQuestion + 1} 題 / 共 {FIXED_TOTAL_QUESTIONS} 題
          </div>
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">
            {currentQuestion.question_text}
          </h2>

          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => {
              const isSelected = getCurrentQuestionAnswer(currentQuestion.id) === option;
              return (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  className={`w-full p-4 text-left rounded-lg border-2 transition-all duration-200 ${
                    isSelected
                      ? 'border-primary-600 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
                  }`}
                >
                  {option}
                </button>
              );
            })}
          </div>
        </div>

        {/* 導航按鈕 */}
        <div className="flex justify-between items-center">
          <button
            onClick={handlePrev}
            disabled={state.currentQuestion === 0}
            className={`px-6 py-2 rounded-lg transition-colors ${
              state.currentQuestion === 0
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-gray-600 text-white hover:bg-gray-700'
            }`}
          >
            上一題
          </button>

          <div className="flex space-x-4">
            <button
              onClick={handleRestartTest}
              className="px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
              title="重新開始測驗並隨機換新題目"
            >
              重新測驗
            </button>

            {state.currentQuestion === questions.length - 1 ? (
              <button
                onClick={handleSubmit}
                disabled={submitting || answeredCount < FIXED_TOTAL_QUESTIONS}
                className={`px-8 py-2 rounded-lg transition-colors ${
                  answeredCount < FIXED_TOTAL_QUESTIONS
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-green-600 text-white hover:bg-green-700'
                }`}
              >
                {submitting ? '提交中...' : '提交測驗'}
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={!isQuestionAnswered(currentQuestion.id)}
                className={`px-6 py-2 rounded-lg transition-colors ${
                  !isQuestionAnswered(currentQuestion.id)
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-primary-600 text-white hover:bg-primary-700'
                }`}
              >
                下一題
              </button>
            )}
          </div>
        </div>
      </div>

      {/* 進度指示器 */}
      {questions.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <BarChart3 size={20} className="mr-2" />
            測驗進度 ({answeredCount}/{FIXED_TOTAL_QUESTIONS})
          </h3>
          <div className="grid grid-cols-10 gap-1">
            {questions.map((question, index) => (
              <div
                key={index}
                className={`h-8 rounded flex items-center justify-center text-xs font-medium ${
                  index === state.currentQuestion
                    ? 'bg-primary-600 text-white'
                    : isQuestionAnswered(question.id)
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {index + 1}
              </div>
            ))}
          </div>
          <div className="mt-3 text-sm text-gray-600">
            <span className="inline-block w-3 h-3 bg-primary-600 rounded mr-2"></span>
            當前題目
            <span className="inline-block w-3 h-3 bg-green-500 rounded mr-2 ml-4"></span>
            已回答
            <span className="inline-block w-3 h-3 bg-gray-200 rounded mr-2 ml-4"></span>
            未回答
          </div>
        </div>
      )}
    </div>
  );
};

export default TestPage;