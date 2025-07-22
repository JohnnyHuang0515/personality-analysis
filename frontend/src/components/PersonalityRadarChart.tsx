import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js/auto';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface PersonalityRadarChartProps {
  scores: Record<string, number>;
  testType: string;
}

const PersonalityRadarChart: React.FC<PersonalityRadarChartProps> = ({ scores, testType }) => {
  // 根據測驗類型定義特質標籤和顏色
  const getChartConfig = () => {
    switch (testType.toLowerCase()) {
      case 'MBTI':
        return {
          // 對立特質放在對面：E-I, S-N, T-F, J-P
          labels: ['外向 (E)', '感覺 (S)', '思考 (T)', '判斷 (J)', '內向 (I)', '直覺 (N)', '情感 (F)', '知覺 (P)'],
          colors: {
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            pointBackgroundColor: 'rgba(59, 130, 246, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(59, 130, 246, 1)'
          }
        };
      
      case 'DISC':
        return {
          // 對立特質放在對面：D-S (任務導向 vs 人際導向), I-C (外向 vs 內向)
          labels: ['支配性 (D)', '影響性 (I)', '穩定性 (S)', '謹慎性 (C)'],
          colors: {
            backgroundColor: 'rgba(34, 197, 94, 0.2)',
            borderColor: 'rgba(34, 197, 94, 1)',
            pointBackgroundColor: 'rgba(34, 197, 94, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(34, 197, 94, 1)'
          }
        };
      
      case 'BIG5':
        return {
          // 對立特質放在對面：O-N (開放 vs 封閉), C-E (內向 vs 外向), A (獨立維度)
          labels: ['開放性 (O)', '外向性 (E)', '親和性 (A)', '神經質 (N)', '盡責性 (C)'],
          colors: {
            backgroundColor: 'rgba(245, 158, 11, 0.2)',
            borderColor: 'rgba(245, 158, 11, 1)',
            pointBackgroundColor: 'rgba(245, 158, 11, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(245, 158, 11, 1)'
          }
        };
      
      case 'ENNEAGRAM':
        return {
          // 對立類型放在對面：1-9, 2-8, 3-7, 4-6, 5 (中心)
          labels: ['類型 1', '類型 3', '類型 5', '類型 7', '類型 9', '類型 2', '類型 4', '類型 6', '類型 8'],
          colors: {
            backgroundColor: 'rgba(239, 68, 68, 0.2)',
            borderColor: 'rgba(239, 68, 68, 1)',
            pointBackgroundColor: 'rgba(239, 68, 68, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(239, 68, 68, 1)'
          }
        };
      
      default:
        return {
          labels: Object.keys(scores),
          colors: {
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            borderColor: 'rgba(99, 102, 241, 1)',
            pointBackgroundColor: 'rgba(99, 102, 241, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(99, 102, 241, 1)'
          }
        };
    }
  };

  const config = getChartConfig();
  
  // 準備數據 - 確保所有特質維度都顯示，並轉換為比例
  const getNormalizedScores = () => {
    const rawScores = config.labels.map(label => {
      // 從標籤中提取特質代碼
      const traitCode = label.match(/\(([A-Z0-9]+)\)/)?.[1] || 
                       label.match(/類型 (\d+)/)?.[1] || 
                       label.split(' ')[0];
      
      // 查找對應的分數，如果沒有則為 0
      const score = scores[traitCode] || scores[label] || 0;
      return score;
    });
    
    // 計算最大值用於比例轉換
    const maxScore = Math.max(...rawScores, 1); // 避免除以0
    
    // 將原始分數轉換為0-10的比例
    const normalizedScores = rawScores.map(score => {
      // 轉換為0-10的比例
      const proportion = (score / maxScore) * 10;
      return Math.round(proportion * 100) / 100; // 保留兩位小數
    });
    
    return normalizedScores;
  };

  const data = {
    labels: config.labels,
    datasets: [
      {
        label: '特質得分',
        data: getNormalizedScores(),
        backgroundColor: config.colors.backgroundColor,
        borderColor: config.colors.borderColor,
        borderWidth: 2,
        pointBackgroundColor: config.colors.pointBackgroundColor,
        pointBorderColor: config.colors.pointBorderColor,
        pointBorderWidth: 2,
        pointHoverBackgroundColor: config.colors.pointHoverBackgroundColor,
        pointHoverBorderColor: config.colors.pointHoverBorderColor,
        pointHoverBorderWidth: 3,
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: 10,
        min: 0,
        ticks: {
          stepSize: 2,
          font: {
            size: 12,
            weight: 'bold' as const,
          },
          color: '#6b7280',
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.2)',
        },
        angleLines: {
          color: 'rgba(107, 114, 128, 0.2)',
        },
        pointLabels: {
          font: {
            size: 14,
            weight: 'bold' as const,
          },
          color: '#374151',
          padding: 20,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: false,
        callbacks: {
          label: function(context: any) {
            return `得分: ${context.parsed.r}`;
          },
        },
      },
    },
  };

  return (
    <div className="w-full h-96 bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
        {testType} 特質分析雷達圖
      </h3>
      <div className="w-full h-80">
        <Radar data={data} options={options} />
      </div>
      <div className="mt-4 text-center text-sm text-gray-600">
        <p>雷達圖顯示您在各個特質維度上的相對強度分布</p>
        <p>分數範圍：0-10（比例顯示），越高表示該特質相對越突出</p>
        <p className="text-xs text-gray-500 mt-1">
          {testType.toLowerCase() === 'mbti' && 'MBTI: 顯示各維度的相對偏好強度'}
          {testType.toLowerCase() === 'disc' && 'DISC: 顯示各風格的相對強度'}
          {testType.toLowerCase() === 'big5' && 'Big5: 顯示各特質的相對強度'}
          {testType.toLowerCase() === 'enneagram' && 'Enneagram: 顯示各類型的相對偏好強度'}
        </p>
      </div>
    </div>
  );
};

export default PersonalityRadarChart; 