import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import PersonalityRadarChart from '../components/PersonalityRadarChart';
import { getComprehensiveReport } from '../services/api';

interface ComprehensiveReport {
  user_id: string;
  report_generated_at: string;
  summary: {
    mbti_type: string;
    disc_primary: string;
    big5_type: string;
    enneagram_type: string;
  };
  detailed_analysis: {
    mbti: any;
    disc: any;
    big5: any;
    enneagram: any;
  };
  integrated_insights: {
    leadership_style: any;
    communication_preferences: any;
    work_environment_fit: any;
    personal_development_priorities: any;
  };
}

const ComprehensiveReportPage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [report, setReport] = useState<ComprehensiveReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    if (userId) {
      loadComprehensiveReport();
    }
  }, [userId]);

  const loadComprehensiveReport = async () => {
    try {
      setLoading(true);
      const data = await getComprehensiveReport(userId!);
      setReport(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '載入報告失敗');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">正在生成綜合人格分析報告...</p>
        </div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">載入失敗</h2>
          <p className="text-gray-600">{error || '無法載入報告'}</p>
        </div>
      </div>
    );
  }

  const renderSummary = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">人格特質摘要</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{report.summary.mbti_type}</div>
            <div className="text-sm text-gray-600">MBTI 類型</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600">{report.summary.disc_primary}</div>
            <div className="text-sm text-gray-600">DISC 風格</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-lg font-bold text-yellow-600">{report.summary.big5_type}</div>
            <div className="text-sm text-gray-600">Big5 類型</div>
          </div>
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-3xl font-bold text-red-600">類型 {report.summary.enneagram_type}</div>
            <div className="text-sm text-gray-600">Enneagram</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">整合洞察</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">領導風格</h4>
            <p className="text-gray-600">{report.integrated_insights.leadership_style.primary_style}</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">溝通偏好</h4>
            <p className="text-gray-600">{report.integrated_insights.communication_preferences.primary_approach}</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">理想工作環境</h4>
            <p className="text-gray-600">{report.integrated_insights.work_environment_fit.ideal_environment}</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">發展重點</h4>
            <p className="text-gray-600">{report.integrated_insights.personal_development_priorities.high_priority[0]}</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderDetailedAnalysis = () => (
    <div className="space-y-6">
      {/* MBTI 詳細分析 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">MBTI 詳細分析</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">人格類型</h4>
              <p className="text-2xl font-bold text-blue-600">{report.detailed_analysis.mbti.personality_type}</p>
              <p className="text-gray-600">{report.detailed_analysis.mbti.description}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">優點</h4>
              <ul className="list-disc list-inside text-gray-600">
                {report.detailed_analysis.mbti.strengths.map((strength: string, index: number) => (
                  <li key={index}>{strength}</li>
                ))}
              </ul>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">職業建議</h4>
              <div className="flex flex-wrap gap-2">
                {report.detailed_analysis.mbti.career_suggestions.map((career: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {career}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-4">特質分布</h4>
            <div className="h-64">
              <PersonalityRadarChart 
                scores={report.detailed_analysis.mbti.scores} 
                testType="MBTI" 
              />
            </div>
          </div>
        </div>
      </div>

      {/* DISC 詳細分析 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">DISC 詳細分析</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">主要風格</h4>
              <p className="text-2xl font-bold text-green-600">{report.detailed_analysis.disc.primary_style}</p>
              <p className="text-gray-600">{report.detailed_analysis.disc.description}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">溝通風格</h4>
              <p className="text-gray-600">{report.detailed_analysis.disc.communication_style}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">工作風格</h4>
              <p className="text-gray-600">{report.detailed_analysis.disc.work_style}</p>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-4">風格分布</h4>
            <div className="h-64">
              <PersonalityRadarChart 
                scores={report.detailed_analysis.disc.scores} 
                testType="DISC" 
              />
            </div>
          </div>
        </div>
      </div>

      {/* Big5 詳細分析 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Big5 詳細分析</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">人格檔案</h4>
              <div className="text-gray-600 whitespace-pre-line">{report.detailed_analysis.big5.personality_profile}</div>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">人際關係風格</h4>
              <p className="text-gray-600">{report.detailed_analysis.big5.interpersonal_style}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">職業匹配</h4>
              <div className="flex flex-wrap gap-2">
                {report.detailed_analysis.big5.career_matches.map((career: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                    {career}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-4">特質分布</h4>
            <div className="h-64">
              <PersonalityRadarChart 
                scores={report.detailed_analysis.big5.scores} 
                testType="BIG5" 
              />
            </div>
          </div>
        </div>
      </div>

      {/* Enneagram 詳細分析 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Enneagram 詳細分析</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">主要類型</h4>
              <p className="text-2xl font-bold text-red-600">類型 {report.detailed_analysis.enneagram.primary_type}</p>
              <p className="text-gray-600">{report.detailed_analysis.enneagram.description}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">核心恐懼</h4>
              <p className="text-gray-600">{report.detailed_analysis.enneagram.fear}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">基本慾望</h4>
              <p className="text-gray-600">{report.detailed_analysis.enneagram.desire}</p>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">成長路徑</h4>
              <p className="text-gray-600">{report.detailed_analysis.enneagram.growth}</p>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-gray-700 mb-4">類型分布</h4>
            <div className="h-64">
              <PersonalityRadarChart 
                scores={report.detailed_analysis.enneagram.scores} 
                testType="ENNEAGRAM" 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderDevelopmentPlan = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">個人發展計劃</h3>
        
        <div className="mb-6">
          <h4 className="font-semibold text-gray-700 mb-3">高優先級發展領域</h4>
          <div className="space-y-2">
            {report.integrated_insights.personal_development_priorities.high_priority.map((item: string, index: number) => (
              <div key={index} className="flex items-center p-3 bg-red-50 rounded-lg">
                <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                <span className="text-gray-700">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h4 className="font-semibold text-gray-700 mb-3">中等優先級發展領域</h4>
          <div className="space-y-2">
            {report.integrated_insights.personal_development_priorities.medium_priority.map((item: string, index: number) => (
              <div key={index} className="flex items-center p-3 bg-yellow-50 rounded-lg">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                <span className="text-gray-700">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-gray-700 mb-3">長期發展目標</h4>
          <div className="space-y-2">
            {report.integrated_insights.personal_development_priorities.long_term_goals.map((item: string, index: number) => (
              <div key={index} className="flex items-center p-3 bg-blue-50 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                <span className="text-gray-700">{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">綜合人格分析報告</h1>
          <p className="text-gray-600">用戶 ID: {report.user_id}</p>
          <p className="text-gray-600">生成時間: {new Date(report.report_generated_at).toLocaleString()}</p>
        </div>

        {/* 標籤頁 */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'summary', name: '摘要', icon: '📊' },
              { id: 'detailed', name: '詳細分析', icon: '🔍' },
              { id: 'development', name: '發展計劃', icon: '📈' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* 內容區域 */}
        <div className="mb-8">
          {activeTab === 'summary' && renderSummary()}
          {activeTab === 'detailed' && renderDetailedAnalysis()}
          {activeTab === 'development' && renderDevelopmentPlan()}
        </div>
      </div>
    </div>
  );
};

export default ComprehensiveReportPage; 