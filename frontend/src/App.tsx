import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import TestPage from './pages/TestPage';
import ReportPage from './pages/ReportPage';
import { TestProvider } from './contexts/TestContext';

function App() {
  return (
    <TestProvider>
      <Router>
        <div className="min-h-screen gradient-bg">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/test/:testType" element={<TestPage />} />
              <Route path="/report/:userId/:testType" element={<ReportPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </TestProvider>
  );
}

export default App; 