import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TestRunner from './pages/TestRunner';
import ChatInterface from './pages/ChatInterface';
import { ChatProvider } from './contexts/ChatContext';
import './App.css';

const Navigation: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/test-runner', label: 'Test Runner', icon: '🧪' },
    { path: '/chat', label: 'AI Chat', icon: '🤖' },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg border-r border-gray-200">
        {/* Logo */}
        <div className="flex items-center justify-center h-16 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">🦖 Restaceratops</h1>
        </div>
        
        {/* Navigation Items */}
        <nav className="mt-6">
          <div className="px-4 space-y-2">
            {navItems.map((item) => (
                              <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-200 sidebar-nav-item ${
                    location.pathname === item.path
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  {item.label}
                </Link>
            ))}
          </div>
        </nav>
        
        {/* Footer */}
        <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200">
          <div className="text-xs text-gray-500 text-center">
            <p>🦖 API Testing Platform</p>
            <p className="mt-1">Powered by AI</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto main-content">
        <main className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/test-runner" element={<TestRunner />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <ChatProvider>
        <Navigation />
      </ChatProvider>
    </Router>
  );
};

export default App;
