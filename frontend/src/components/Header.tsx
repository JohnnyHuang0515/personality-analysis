import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, Home, BarChart3, Target } from 'lucide-react';

const Header: React.FC = () => {
  const location = useLocation();
  
  // 獲取用戶 ID
  const getUserId = () => {
    return localStorage.getItem('personality_test_user_id') || 'user_default';
  };
  
  const userId = getUserId();
  
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="p-2 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg group-hover:scale-110 transition-transform duration-200">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gradient">綜合人格特質分析</h1>
              <p className="text-sm text-gray-600">探索你的內在世界</p>
            </div>
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link 
              to="/" 
              className={`flex items-center space-x-2 transition-colors duration-200 ${
                location.pathname === '/' 
                  ? 'text-primary-600 font-semibold' 
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              <Home className="w-4 h-4" />
              <span>首頁</span>
            </Link>
            <Link 
              to={`/comprehensive-report/${userId}`}
              className={`flex items-center space-x-2 transition-colors duration-200 ${
                location.pathname.includes('/comprehensive-report') 
                  ? 'text-primary-600 font-semibold' 
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              <Target className="w-4 h-4" />
              <span>綜合報告</span>
            </Link>
            <Link 
              to={`/report/${userId}/mbti`}
              className={`flex items-center space-x-2 transition-colors duration-200 ${
                location.pathname.includes('/report') && !location.pathname.includes('/comprehensive-report')
                  ? 'text-primary-600 font-semibold' 
                  : 'text-gray-600 hover:text-primary-600'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>個別報告</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 