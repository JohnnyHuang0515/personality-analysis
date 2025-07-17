import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Share2, Star, TrendingUp, Users, Target } from 'lucide-react';
import { apiService, Report } from '../services/api';

const ReportPage: React.FC = () => {
  const { userId, testType } = useParams<{ userId: string; testType: string }>();
  const navigate = useNavigate();
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReport = async () => {
      if (!userId || !testType) return;
      
      try {
        const response = await apiService.generateReport(userId, testType);
        setReport(response.data);
      } catch (error: any) {
        console.error('Failed to fetch report:', error);
        setError(error.response?.data?.detail || '無法載入報告');
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [userId, testType]);

  const getTestInfo = (type: string) => {
    const testInfo = {
      MBTI: {
        title: 'MBTI 人格類型',
        description: '邁爾斯-布里格斯類型指標',
        color: 'blue',
        icon: <Users className="w-6 h-6 text-blue-600" />
      },
      DISC: {
        title: 'DISC 行為風格',
        description: 'DISC 行為評估',
        color: 'green',
        icon: <Target className="w-6 h-6 text-green-600" />
      },
      Big5: {
        title: '五大人格特質',
        description: '大五人格模型',
        color: 'yellow',
        icon: <TrendingUp className="w-6 h-6 text-yellow-600" />
      },
      Enneagram: {
        title: '九型人格',
        description: '九型人格學',
        color: 'red',
        icon: <Star className="w-6 h-6 text-red-600" />
      }
    };
    return testInfo[type as keyof typeof testInfo] || testInfo.MBTI;
  };

  const testInfo = getTestInfo(testType || '');

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <h2 className="text-xl font-semibold text-red-800 mb-2">載入失敗</h2>
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="btn-primary"
          >
            返回首頁
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="text-center">
        <p className="text-gray-600">沒有找到報告</p>
      </div>
    );
  }

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
          <div className="flex items-center space-x-3">
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>下載報告</span>
            </button>
            <button className="btn-secondary flex items-center space-x-2">
              <Share2 className="w-4 h-4" />
              <span>分享</span>
            </button>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-gray-100 rounded-lg">
            {testInfo.icon}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{testInfo.title}</h1>
            <p className="text-gray-600">{testInfo.description}</p>
          </div>
        </div>
      </div>

      {/* Report Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Report */}
        <div className="lg:col-span-2 space-y-6">
          {/* Summary */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">測驗摘要</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                <span className="text-gray-600">測驗類型</span>
                <span className="font-medium">{testInfo.title}</span>
              </div>
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                <span className="text-gray-600">完成時間</span>
                <span className="font-medium">{report.generated_at}</span>
              </div>
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                <span className="text-gray-600">用戶 ID</span>
                <span className="font-medium">{report.user_id}</span>
              </div>
            </div>
          </div>

          {/* Analysis */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">分析結果</h2>
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed">
                {report.report.analysis || '這是您的測驗分析結果。'}
              </p>
            </div>
          </div>

          {/* Recommendations */}
          {report.report.recommendations && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">建議</h2>
              <div className="space-y-3">
                {report.report.recommendations.map((rec: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-primary-50 rounded-lg">
                    <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-700">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">測驗資訊</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">測驗時間</span>
                <span className="font-medium text-primary-600">
                  {report.generated_at ? '已完成' : '計算中...'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">測驗日期</span>
                <span className="font-medium text-primary-600">
                  {report.generated_at ? 
                    new Date(report.generated_at).toLocaleDateString('zh-TW', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    }) : 
                    new Date().toLocaleDateString('zh-TW', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })
                  }
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">完成進度</span>
                <span className="font-medium text-success-600">100%</span>
              </div>
            </div>
          </div>

          {/* Test Notice */}
          <div className="card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">測驗說明</h3>
            <p className="text-blue-800 text-sm leading-relaxed">
              本測驗結果僅供參考，非正式診斷工具
            </p>
          </div>

          {/* Next Steps */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">下一步</h3>
            <div className="space-y-3">
              <button className="w-full btn-primary">
                完成其他測驗
              </button>
              <button className="w-full btn-secondary">
                查看詳細報告
              </button>
              <button className="w-full btn-secondary">
                個人發展建議
              </button>
            </div>
          </div>

          {/* Related Tests */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">相關測驗</h3>
            <div className="space-y-2">
              {['MBTI', 'DISC', 'Big5', 'Enneagram'].filter(type => type !== testType).map(type => (
                <button
                  key={type}
                  onClick={() => navigate(`/test/${type}`)}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors duration-200"
                >
                  <div className="font-medium text-gray-900">{getTestInfo(type).title}</div>
                  <div className="text-sm text-gray-600">{getTestInfo(type).description}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportPage; 