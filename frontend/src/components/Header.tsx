import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, Home, BarChart3 } from 'lucide-react';

const Header: React.FC = () => {
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
              className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors duration-200"
            >
              <Home className="w-4 h-4" />
              <span>首頁</span>
            </Link>
            <Link 
              to="/reports" 
              className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors duration-200"
            >
              <BarChart3 className="w-4 h-4" />
              <span>報告</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 