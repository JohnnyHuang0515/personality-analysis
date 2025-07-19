import React from 'react';
import { ArrowRight, CheckCircle, Play, Brain, Users, Target, Heart } from 'lucide-react';

export interface TestCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  status?: 'available' | 'ongoing' | 'completed';
  progress?: number;
  onClick: () => void;
  questionCount: number;
  features: string[];
  estimatedTime: string;
  colorTheme?: 'blue' | 'green' | 'purple' | 'pink';
}

const TestCard: React.FC<TestCardProps> = ({
  title,
  description,
  icon,
  status = 'available',
  progress,
  onClick,
  questionCount,
  features,
  estimatedTime,
  colorTheme = 'blue'
}) => {
  const getColorConfig = (theme: string) => {
    const colorMap = {
      blue: {
        background: 'bg-blue-50',
        iconBg: 'bg-blue-100',
        iconColor: 'text-blue-600'
      },
      green: {
        background: 'bg-green-50',
        iconBg: 'bg-green-100',
        iconColor: 'text-green-600'
      },
      purple: {
        background: 'bg-purple-50',
        iconBg: 'bg-purple-100',
        iconColor: 'text-purple-600'
      },
      pink: {
        background: 'bg-pink-50',
        iconBg: 'bg-pink-100',
        iconColor: 'text-pink-600'
      }
    };
    return colorMap[theme as keyof typeof colorMap] || colorMap.blue;
  };

  const getStatusConfig = () => {
    switch (status) {
      case 'ongoing':
        return {
          buttonText: '繼續測驗',
          buttonIcon: <ArrowRight className="w-4 h-4" />,
          statusLabel: '🔄 進行中'
        };
      case 'completed':
        return {
          buttonText: '查看報告',
          buttonIcon: <CheckCircle className="w-4 h-4" />,
          statusLabel: '✅ 已完成'
        };
      default:
        return {
          buttonText: '開始測驗',
          buttonIcon: <ArrowRight className="w-4 h-4" />,
          statusLabel: null
        };
    }
  };

  const config = getStatusConfig();
  const colors = getColorConfig(colorTheme);

  return (
    <div className={`${colors.background} rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 min-h-[280px] flex flex-col`}>
      {/* 題目數量標籤 */}
      <div className="flex justify-between items-start mb-4">
        <div className={`${colors.iconBg} p-3 rounded-lg`}>
          <div className={colors.iconColor}>
            {icon}
          </div>
        </div>
        <div className="bg-gray-100 text-gray-600 text-sm px-3 py-1 rounded-full font-medium">
          {questionCount}題
        </div>
      </div>

      {/* 狀態標籤（僅在進行中或已完成時顯示） */}
      {config.statusLabel && (
        <div className="mb-4">
          <span className="bg-white/80 text-gray-700 text-sm px-3 py-1 rounded-full font-medium">
            {config.statusLabel}
          </span>
        </div>
      )}

      {/* 標題 */}
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>

      {/* 描述 */}
      <p className="text-gray-600 text-sm mb-4 leading-relaxed">{description}</p>

      {/* 特色列表 */}
      <div className="mb-6 flex-1">
        <ul className="space-y-2">
          {features.map((feature, index) => (
            <li key={index} className="text-gray-700 text-sm flex items-center">
              <span className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2"></span>
              {feature}
            </li>
          ))}
        </ul>
      </div>

      {/* 進度條（僅在進行中時顯示） */}
      {status === 'ongoing' && progress !== undefined && (
        <div className="mb-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">進度</span>
            <span className="font-medium text-gray-900">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* 底部區域 */}
      <div className="mt-auto">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {status === 'ongoing' ? '點擊繼續測驗' : status === 'completed' ? '查看詳細報告' : `預估時間: ${estimatedTime}`}
          </div>
          <button
            onClick={onClick}
            className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            <span>{config.buttonText}</span>
            {config.buttonIcon}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TestCard; 