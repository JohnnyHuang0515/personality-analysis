import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface TraitBarChartProps {
  scores: Record<string, number>;
  testType: string;
}

const TraitBarChart: React.FC<TraitBarChartProps> = ({ scores, testType }) => {
  // 根據測驗類型定義特質標籤和顏色
  const getChartConfig = () => {
    switch (testType.toUpperCase()) {
      case 'MBTI':
        return {
          labels: ['外向 (E)', '內向 (I)', '感覺 (S)', '直覺 (N)', '思考 (T)', '情感 (F)', '判斷 (J)', '知覺 (P)'],
          colors: [
            'rgba(59, 130, 246, 0.8)',   // 藍色
            'rgba(147, 51, 234, 0.8)',   // 紫色
            'rgba(16, 185, 129, 0.8)',   // 綠色
            'rgba(245, 158, 11, 0.8)',   // 黃色
            'rgba(239, 68, 68, 0.8)',    // 紅色
            'rgba(236, 72, 153, 0.8)',   // 粉色
            'rgba(6, 182, 212, 0.8)',    // 青色
            'rgba(168, 85, 247, 0.8)',   // 靛藍
          ]
        };
      
      case 'DISC':
        return {
          labels: ['支配性 (D)', '影響性 (I)', '穩定性 (S)', '謹慎性 (C)'],
          colors: [
            'rgba(239, 68, 68, 0.8)',    // 紅色
            'rgba(245, 158, 11, 0.8)',   // 黃色
            'rgba(16, 185, 129, 0.8)',   // 綠色
            'rgba(59, 130, 246, 0.8)',   // 藍色
          ]
        };
      
      case 'BIG5':
        return {
          labels: ['開放性 (O)', '盡責性 (C)', '外向性 (E)', '親和性 (A)', '神經質 (N)'],
          colors: [
            'rgba(245, 158, 11, 0.8)',   // 黃色
            'rgba(16, 185, 129, 0.8)',   // 綠色
            'rgba(59, 130, 246, 0.8)',   // 藍色
            'rgba(236, 72, 153, 0.8)',   // 粉色
            'rgba(239, 68, 68, 0.8)',    // 紅色
          ]
        };
      
      case 'ENNEAGRAM':
        return {
          labels: ['類型 1', '類型 2', '類型 3', '類型 4', '類型 5', '類型 6', '類型 7', '類型 8', '類型 9'],
          colors: [
            'rgba(239, 68, 68, 0.8)',    // 紅色
            'rgba(245, 158, 11, 0.8)',   // 黃色
            'rgba(16, 185, 129, 0.8)',   // 綠色
            'rgba(59, 130, 246, 0.8)',   // 藍色
            'rgba(147, 51, 234, 0.8)',   // 紫色
            'rgba(236, 72, 153, 0.8)',   // 粉色
            'rgba(6, 182, 212, 0.8)',    // 青色
            'rgba(168, 85, 247, 0.8)',   // 靛藍
            'rgba(34, 197, 94, 0.8)',    // 翠綠
          ]
        };
      
      default:
        return {
          labels: Object.keys(scores),
          colors: Object.keys(scores).map(() => 'rgba(99, 102, 241, 0.8)')
        };
    }
  };

  const config = getChartConfig();
  
  // 準備數據
  const data = {
    labels: config.labels,
    datasets: [
      {
        label: '特質得分',
        data: config.labels.map(label => {
          // 從標籤中提取特質代碼
          const traitCode = label.match(/\(([A-Z0-9]+)\)/)?.[1] || 
                           label.match(/類型 (\d+)/)?.[1] || 
                           label.split(' ')[0];
          
          // 查找對應的分數
          const score = scores[traitCode] || scores[label] || 0;
          return Math.round(score * 100) / 100; // 保留兩位小數
        }),
        backgroundColor: config.colors,
        borderColor: config.colors.map(color => color.replace('0.8', '1')),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
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
          color: 'rgba(107, 114, 128, 0.1)',
        },
      },
      x: {
        ticks: {
          font: {
            size: 12,
            weight: 'bold' as const,
          },
          color: '#374151',
          maxRotation: 45,
        },
        grid: {
          display: false,
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
            return `得分: ${context.parsed.y}`;
          },
        },
      },
    },
  };

  return (
    <div className="w-full h-96 bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
        {testType} 特質得分詳情
      </h3>
      <div className="w-full h-80">
        <Bar data={data} options={options} />
      </div>
      <div className="mt-4 text-center text-sm text-gray-600">
        <p>條形圖顯示您在各個特質維度上的具體得分</p>
        <p>分數範圍：0-10，越高表示該特質越突出</p>
      </div>
    </div>
  );
};

export default TraitBarChart; 