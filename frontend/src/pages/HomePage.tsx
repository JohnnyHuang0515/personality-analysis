import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import TestCard from '../components/TestCard';
import { useTest } from '../contexts/TestContext';
import { Brain, Target, Zap, Heart } from 'lucide-react';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { state, dispatch } = useTest();

  // 生成或獲取用戶 ID（使用 localStorage 保持一致性）
  const getUserId = () => {
    let userId = localStorage.getItem('personality_test_user_id');
    if (!userId) {
      userId = `user_${Date.now()}`;
      localStorage.setItem('personality_test_user_id', userId);
    }
    return userId;
  };

  const userId = getUserId();

  // 重置用戶 ID（用於測試）
  const resetUserId = () => {
    localStorage.removeItem('personality_test_user_id');
    window.location.reload();
  };

  const tests = [
    {
      id: 'mbti',
      title: 'MBTI 人格類型',
      description: '邁爾斯-布里格斯類型指標,了解你的認知偏好和行為模式。',
      icon: <Brain className="w-6 h-6" />,
      colorTheme: 'blue' as const,
      features: ['16種人格類型', '認知偏好分析', '職業發展建議'],
      estimatedTime: '20-25 分鐘'
    },
    {
      id: 'disc',
      title: 'DISC 行為風格',
      description: 'DISC 行為評估,分析你的溝通風格和工作偏好。',
      icon: <Target className="w-6 h-6" />,
      colorTheme: 'green' as const,
      features: ['4種行為風格', '溝通方式分析', '團隊合作建議'],
      estimatedTime: '15-20 分鐘'
    },
    {
      id: 'big5',
      title: '五大人格特質',
      description: '大五人格模型,科學化的人格特質評估。',
      icon: <Zap className="w-6 h-6" />,
      colorTheme: 'purple' as const,
      features: ['5個核心特質', '科學化評估', '個人成長建議'],
      estimatedTime: '18-25 分鐘'
    },
    {
      id: 'enneagram',
      title: '九型人格',
      description: '九型人格學,深入探索你的核心動機和恐懼。',
      icon: <Heart className="w-6 h-6" />,
      colorTheme: 'pink' as const,
      features: ['9種人格類型', '核心動機分析', '成長方向指引'],
      estimatedTime: '15-20 分鐘'
    }
  ];

  const handleTestClick = (testId: string) => {
    navigate(`/test/${testId}`);
  };

  const getTestStatus = (testId: string) => {
    if (state.currentTest === testId) {
      if (state.isCompleted) return 'completed';
      return 'ongoing';
    }
    return 'available';
  };

  const getTestProgress = (testId: string) => {
    if (state.currentTest === testId && !state.isCompleted) {
      // 固定使用30題計算進度
      const FIXED_TOTAL_QUESTIONS = 30;
      return (Object.keys(state.answers).length / FIXED_TOTAL_QUESTIONS) * 100;
    }
    return undefined;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">綜合人格特質分析</h1>
              <p className="text-gray-600 mt-1">探索你的內在世界，了解真實的自己</p>
            </div>
            <div className="flex items-center space-x-4">
              {userId && (
                <div className="text-sm text-gray-600">
                  用戶 ID: {userId}
                </div>
              )}
              <button
                onClick={resetUserId}
                className="text-sm text-gray-500 hover:text-gray-700 underline"
              >
                重置用戶
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            選擇你想要進行的測驗
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            我們提供多種專業的人格測驗，幫助你深入了解自己的性格特質、行為模式和內在動機。
            每個測驗都經過精心設計，提供準確且有意義的分析結果。
          </p>
        </div>

        {/* Test Cards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {tests.map((test) => (
            <TestCard
              key={test.id}
              title={test.title}
              description={test.description}
              icon={test.icon}
              status={getTestStatus(test.id)}
              progress={getTestProgress(test.id)}
              onClick={() => handleTestClick(test.id)}
              features={test.features}
              estimatedTime={test.estimatedTime}
              colorTheme={test.colorTheme}
            />
          ))}
        </div>

        {/* Additional Information */}
        <div className="mt-16 text-center">
          <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-100">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              為什麼選擇我們的測驗？
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-gray-600">
              <div>
                <div className="font-semibold text-gray-900 mb-2">🔬 科學可靠</div>
                <p>基於心理學理論和實證研究，確保測驗的科學性和可靠性</p>
              </div>
              <div>
                <div className="font-semibold text-gray-900 mb-2">📊 詳細分析</div>
                <p>提供深入的人格分析報告，幫助你更好地了解自己</p>
              </div>
              <div>
                <div className="font-semibold text-gray-900 mb-2">🔒 隱私保護</div>
                <p>你的所有數據都受到嚴格保護，確保個人隱私安全</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage; 