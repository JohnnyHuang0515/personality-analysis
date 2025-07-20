import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface TraitScoreCardsProps {
  scores: Record<string, number>;
  testType: string;
}

const TraitScoreCards: React.FC<TraitScoreCardsProps> = ({ scores, testType }) => {
  // 根據測驗類型定義特質信息
  const getTraitInfo = () => {
    switch (testType.toUpperCase()) {
      case 'MBTI':
        return [
          { code: 'E', name: '外向', description: '傾向於從外部世界獲取能量' },
          { code: 'I', name: '內向', description: '傾向於從內心世界獲取能量' },
          { code: 'S', name: '感覺', description: '注重具體的事實和細節' },
          { code: 'N', name: '直覺', description: '注重可能性和未來發展' },
          { code: 'T', name: '思考', description: '基於邏輯和客觀分析做決定' },
          { code: 'F', name: '情感', description: '基於價值觀和感受做決定' },
          { code: 'J', name: '判斷', description: '喜歡有計劃和結構的生活' },
          { code: 'P', name: '知覺', description: '喜歡保持選項開放和靈活' },
        ];
      
      case 'DISC':
        return [
          { code: 'D', name: '支配性', description: '直接、果斷、喜歡挑戰' },
          { code: 'I', name: '影響性', description: '樂觀、友善、善於交際' },
          { code: 'S', name: '穩定性', description: '耐心、可靠、善於合作' },
          { code: 'C', name: '謹慎性', description: '準確、分析、注重品質' },
        ];
      
      case 'BIG5':
        return [
          { code: 'O', name: '開放性', description: '對新經驗的開放程度' },
          { code: 'C', name: '盡責性', description: '自我控制和目標導向' },
          { code: 'E', name: '外向性', description: '社交性和能量水平' },
          { code: 'A', name: '親和性', description: '合作性和信任度' },
          { code: 'N', name: '神經質', description: '情緒穩定性和壓力反應' },
        ];
      
      case 'ENNEAGRAM':
        return [
          { code: '1', name: '完美主義者', description: '理性、理想主義、有原則' },
          { code: '2', name: '助人者', description: '關心他人、慷慨、善解人意' },
          { code: '3', name: '成就者', description: '適應性強、有野心、注重形象' },
          { code: '4', name: '藝術家', description: '浪漫、自我表達、獨特' },
          { code: '5', name: '觀察者', description: '好奇、獨立、善於分析' },
          { code: '6', name: '忠誠者', description: '負責任、焦慮、忠誠' },
          { code: '7', name: '冒險家', description: '樂觀、多才多藝、愛玩' },
          { code: '8', name: '領導者', description: '自信、果斷、保護他人' },
          { code: '9', name: '調停者', description: '接受、信任、尋求和諧' },
        ];
      
      default:
        return Object.keys(scores).map(code => ({
          code,
          name: code,
          description: '特質描述'
        }));
    }
  };

  const traitInfo = getTraitInfo();

  // 獲取特質的顏色
  const getTraitColor = (index: number) => {
    const colors = [
      'bg-blue-500',
      'bg-purple-500',
      'bg-green-500',
      'bg-yellow-500',
      'bg-red-500',
      'bg-pink-500',
      'bg-cyan-500',
      'bg-indigo-500',
      'bg-emerald-500',
    ];
    return colors[index % colors.length];
  };

  // 獲取得分等級
  const getScoreLevel = (score: number) => {
    if (score >= 8) return { level: '很高', color: 'text-green-600', icon: <TrendingUp className="w-4 h-4" /> };
    if (score >= 6) return { level: '高', color: 'text-blue-600', icon: <TrendingUp className="w-4 h-4" /> };
    if (score >= 4) return { level: '中等', color: 'text-yellow-600', icon: <Minus className="w-4 h-4" /> };
    if (score >= 2) return { level: '低', color: 'text-orange-600', icon: <TrendingDown className="w-4 h-4" /> };
    return { level: '很低', color: 'text-red-600', icon: <TrendingDown className="w-4 h-4" /> };
  };

  return (
    <div className="w-full bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
        {testType} 特質得分詳情
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {traitInfo.map((trait, index) => {
          const score = scores[trait.code] || 0;
          const scoreLevel = getScoreLevel(score);
          const colorClass = getTraitColor(index);
          
          return (
            <div key={trait.code} className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${colorClass}`}></div>
                  <h4 className="font-semibold text-gray-900">{trait.name}</h4>
                </div>
                <div className="flex items-center space-x-1">
                  {scoreLevel.icon}
                  <span className={`text-sm font-medium ${scoreLevel.color}`}>
                    {scoreLevel.level}
                  </span>
                </div>
              </div>
              
              <div className="mb-3">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm text-gray-600">得分</span>
                  <span className="text-lg font-bold text-gray-900">{score.toFixed(1)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${colorClass.replace('bg-', 'bg-').replace('-500', '-400')}`}
                    style={{ width: `${(score / 10) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 leading-relaxed">
                {trait.description}
              </p>
            </div>
          );
        })}
      </div>
      
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2">得分說明</h4>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-sm">
          <div className="flex items-center space-x-1">
            <TrendingUp className="w-3 h-3 text-green-600" />
            <span className="text-green-600">8-10: 很高</span>
          </div>
          <div className="flex items-center space-x-1">
            <TrendingUp className="w-3 h-3 text-blue-600" />
            <span className="text-blue-600">6-7.9: 高</span>
          </div>
          <div className="flex items-center space-x-1">
            <Minus className="w-3 h-3 text-yellow-600" />
            <span className="text-yellow-600">4-5.9: 中等</span>
          </div>
          <div className="flex items-center space-x-1">
            <TrendingDown className="w-3 h-3 text-orange-600" />
            <span className="text-orange-600">2-3.9: 低</span>
          </div>
          <div className="flex items-center space-x-1">
            <TrendingDown className="w-3 h-3 text-red-600" />
            <span className="text-red-600">0-1.9: 很低</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TraitScoreCards; 