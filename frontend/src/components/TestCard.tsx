import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

interface TestCardProps {
  testType: string;
  title: string;
  description: string;
  questionCount: number;
  duration: string;
  icon: React.ReactNode;
  gradient: string;
  features: string[];
}

const TestCard: React.FC<TestCardProps> = ({
  testType,
  title,
  description,
  questionCount,
  duration,
  icon,
  gradient,
  features
}) => {
  return (
    <div className={`card card-hover group ${gradient}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="p-3 bg-white rounded-lg shadow-sm group-hover:scale-110 transition-transform duration-200">
          {icon}
        </div>
        <div className="text-sm text-gray-600 bg-white/80 px-2 py-1 rounded-full">
          {questionCount} 題
        </div>
      </div>
      
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-4 leading-relaxed">{description}</p>
      
      <div className="space-y-2 mb-6">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center text-sm text-gray-600">
            <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mr-2"></div>
            {feature}
          </div>
        ))}
      </div>
      
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-500">
          預估時間: {duration}
        </div>
        <Link
          to={`/test/${testType}`}
          className="btn-primary flex items-center space-x-2 group-hover:scale-105 transition-transform duration-200"
        >
          <span>開始測驗</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
        </Link>
      </div>
    </div>
  );
};

export default TestCard; 