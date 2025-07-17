import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, CheckCircle, Circle, Clock, BarChart3 } from 'lucide-react';
import { apiService, Question } from '../services/api';
import { useTest } from '../contexts/TestContext';

const TestPage: React.FC = () => {
  const { testType } = useParams<{ testType: string }>();
  const navigate = useNavigate();
  const { state, dispatch } = useTest();
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [userId] = useState(`user_${Date.now()}`);

  useEffect(() => {
    const fetchQuestions = async () => {
      if (!testType) return;
      
      try {
        const response = await apiService.getQuestions(testType);
        setQuestions(response.data.questions);
        dispatch({ 
          type: 'START_TEST', 
          payload: { 
            testType, 
            userId,
            totalQuestions: response.data.questions.length
          } 
        });
      } catch (error) {
        console.error('Failed to fetch questions:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [testType, dispatch, userId]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const currentQuestion = questions[state.currentQuestion];
  const progress = (state.currentQuestion / questions.length) * 100;
  const answeredCount = Object.keys(state.answers).length;

  const handleAnswer = (answer: string) => {
    if (!currentQuestion) return;
    
    dispatch({
      type: 'ANSWER_QUESTION',
      payload: { questionId: currentQuestion.id, answer }
    });
  };

  const handleNext = () => {
    if (state.currentQuestion < questions.length - 1) {
      dispatch({ type: 'NEXT_QUESTION' });
    }
  };

  const handlePrev = () => {
    if (state.currentQuestion > 0) {
      dispatch({ type: 'PREV_QUESTION' });
    }
  };

  const handleSubmit = async () => {
    if (!testType) return;
    
    setSubmitting(true);
    try {
      const answers = Object.entries(state.answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId),
        answer
      }));

      await apiService.submitAnswers({
        user_id: userId,
        test_type: testType,
        answers
      });

      dispatch({ type: 'COMPLETE_TEST' });
      navigate(`/report/${userId}/${testType}`);
    } catch (error) {
      console.error('Failed to submit answers:', error);
      alert('提交失敗，請重試');
    } finally {
      setSubmitting(false);
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
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="text-center">
        <p className="text-gray-600">沒有找到題目</p>
      </div>
    );
  }

  const isAnswered = state.answers[currentQuestion.id];
  const isLastQuestion = state.currentQuestion === questions.length - 1;
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
        
        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-sm text-gray-600 mt-2">
          <span>題目 {state.currentQuestion + 1} / {questions.length}</span>
          <span>{Math.round(progress)}% 完成</span>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {currentQuestion.text}
            </h2>
            {/* <p className="text-sm text-gray-600">
              類別: {currentQuestion.category}
            </p> */}
          </div>

          {/* Options */}
          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswer(option)}
                className={`w-full p-4 text-left rounded-lg border-2 transition-all duration-200 ${
                  isAnswered === option
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  {isAnswered === option ? (
                    <CheckCircle className="w-5 h-5 text-primary-500" />
                  ) : (
                    <Circle className="w-5 h-5 text-gray-400" />
                  )}
                  <span className="font-medium">{option}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={handlePrev}
          disabled={state.currentQuestion === 0}
          className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>上一題</span>
        </button>

        <div className="flex items-center space-x-4">
          {isLastQuestion ? (
            <button
              onClick={handleSubmit}
              disabled={!canSubmit || submitting}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>提交中...</span>
                </>
              ) : (
                <>
                  <CheckCircle className="w-4 h-4" />
                  <span>完成測驗</span>
                </>
              )}
            </button>
          ) : (
            <button
              onClick={handleNext}
              disabled={!isAnswered}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span>下一題</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Completion Warning */}
      {!canSubmit && isLastQuestion && (
        <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
          <p className="text-warning-800 text-sm">
            請至少完成 {Math.ceil(questions.length * 0.8)} 題才能提交測驗。
            目前已完成 {answeredCount} 題。
          </p>
        </div>
      )}
    </div>
  );
};

export default TestPage; 