import React, { useState, useEffect } from 'react';
import { Users, Target, Zap, Heart, Star, TrendingUp, Shield, Award, Clock, ArrowRight } from 'lucide-react';
import TestCard from '../components/TestCard';
import { apiService } from '../services/api';
import { useTest } from '../contexts/TestContext';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const [testTypes, setTestTypes] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const { state, hasUnfinishedTest, getProgressPercentage, getAnsweredCount } = useTest();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTestTypes = async () => {
      try {
        const response = await apiService.getTestTypes();
        setTestTypes(response.data.total_questions || {});
      } catch (error) {
        console.error('Failed to fetch test types:', error);
        // 使用預設值
        setTestTypes({
          MBTI: 50,
          DISC: 50,
          Big5: 50,
          Enneagram: 100
        });
      } finally {
        setLoading(false);
      }
    };

    fetchTestTypes();
  }, []);

  const handleContinueTest = () => {
    if (state.currentTest) {
      navigate(`/test/${state.currentTest}`);
    }
  };

  const handleResetTest = () => {
    // 重置測驗
    window.location.reload(); // 簡單的重置方式
  };

  const tests = [
    {
      testType: 'MBTI',
      title: 'MBTI 人格類型',
      description: '邁爾斯-布里格斯類型指標，了解你的認知偏好和行為模式。',
      questionCount: testTypes.MBTI || 50,
      duration: '15-20 分鐘',
      icon: <Users className="w-6 h-6 text-blue-600" />,
      gradient: 'bg-gradient-to-br from-blue-50 to-indigo-50',
      features: ['16種人格類型', '認知偏好分析', '職業發展建議']
    },
    {
      testType: 'DISC',
      title: 'DISC 行為風格',
      description: 'DISC 行為評估，分析你的溝通風格和工作偏好。',
      questionCount: testTypes.DISC || 50,
      duration: '10-15 分鐘',
      icon: <Target className="w-6 h-6 text-green-600" />,
      gradient: 'bg-gradient-to-br from-green-50 to-emerald-50',
      features: ['4種行為風格', '溝通方式分析', '團隊合作建議']
    },
    {
      testType: 'Big5',
      title: '五大人格特質',
      description: '大五人格模型，科學化的人格特質評估。',
      questionCount: testTypes.Big5 || 50,
      duration: '12-18 分鐘',
      icon: <Zap className="w-6 h-6 text-yellow-600" />,
      gradient: 'bg-gradient-to-br from-yellow-50 to-orange-50',
      features: ['5個核心特質', '科學化評估', '個人成長建議']
    },
    {
      testType: 'Enneagram',
      title: '九型人格',
      description: '九型人格學，深入探索你的核心動機和恐懼。',
      questionCount: testTypes.Enneagram || 100,
      duration: '20-25 分鐘',
      icon: <Heart className="w-6 h-6 text-red-600" />,
      gradient: 'bg-gradient-to-br from-red-50 to-pink-50',
      features: ['9種人格類型', '核心動機分析', '成長方向指引']
    }
  ];

  const features = [
    {
      icon: <Star className="w-8 h-8 text-primary-600" />,
      title: '專業評估',
      description: '基於心理學理論的科學化評估工具'
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-success-600" />,
      title: '個人成長',
      description: '提供具體的個人發展建議和方向'
    },
    {
      icon: <Shield className="w-8 h-8 text-warning-600" />,
      title: '隱私保護',
      description: '嚴格保護您的個人資料和測驗結果'
    },
    {
      icon: <Award className="w-8 h-8 text-secondary-600" />,
      title: '綜合分析',
      description: '四種測驗的整合分析，提供全面的人格洞察'
    }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-12">
      {/* Unfinished Test Notice */}
      {hasUnfinishedTest() && (
        <section className="bg-gradient-to-r from-orange-50 to-red-50 border border-orange-200 rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-orange-100 rounded-lg">
                <Clock className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-orange-900">
                  你有未完成的測驗
                </h3>
                <p className="text-orange-700">
                  {state.currentTest} 測驗已完成 {getAnsweredCount()}/{state.totalQuestions} 題 
                  ({getProgressPercentage()}%)
                </p>
              </div>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={handleContinueTest}
                className="flex items-center space-x-2 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors duration-200"
              >
                <ArrowRight className="w-4 h-4" />
                <span>繼續測驗</span>
              </button>
              <button
                onClick={handleResetTest}
                className="text-orange-600 hover:text-orange-700 px-4 py-2 rounded-lg border border-orange-300 hover:bg-orange-50 transition-colors duration-200"
              >
                重新開始
              </button>
            </div>
          </div>
        </section>
      )}

      {/* Hero Section */}
      <section className="text-center space-y-6">
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gradient">
            探索你的內在世界
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            透過四種專業的人格測驗，深入了解你的性格特質、行為模式、認知偏好和核心動機，
            為你的個人成長和職業發展提供科學化的指引。
          </p>
        </div>
        
        <div className="flex flex-wrap justify-center gap-8 mt-8">
          {features.map((feature, index) => (
            <div key={index} className="flex flex-col items-center space-y-3 p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
              {feature.icon}
              <h3 className="font-semibold text-gray-900">{feature.title}</h3>
              <p className="text-sm text-gray-600 text-center max-w-48">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Test Cards Section */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">選擇你的測驗</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            每種測驗都有其獨特的視角和價值，你可以選擇其中一種或完成全部測驗來獲得最全面的分析。
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {tests.map((test, index) => (
            <div key={test.testType} className="animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <TestCard {...test} />
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl p-8 text-center text-white">
        <h2 className="text-2xl font-bold mb-4">準備好開始你的探索之旅了嗎？</h2>
        <p className="text-primary-100 mb-6 max-w-2xl mx-auto">
          選擇一個測驗開始，或完成所有測驗來獲得最全面的個人分析報告。
          每個測驗只需要 10-25 分鐘，讓我們一起探索你的內在世界！
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="bg-white text-primary-600 font-semibold py-3 px-6 rounded-lg hover:bg-gray-100 transition-colors duration-200">
            開始第一個測驗
          </button>
          <button className="border-2 border-white text-white font-semibold py-3 px-6 rounded-lg hover:bg-white hover:text-primary-600 transition-colors duration-200">
            了解更多
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 