import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  ChatBubbleLeftRightIcon, 
  DocumentTextIcon, 
  ChartBarIcon, 
  CogIcon,
  PlayIcon,
  BeakerIcon,
  SparklesIcon,
  EyeIcon,
  PresentationChartLineIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';
import './App.css';
import ChatInterface from './pages/ChatInterface';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import TestBuilder from './pages/TestBuilder';
import TestRunner from './pages/TestRunner';
import WorkflowInterface from './pages/WorkflowInterface';
import TestGenerator from './pages/TestGenerator';
import TestMonitor from './pages/TestMonitor';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import EnterpriseDashboard from './pages/EnterpriseDashboard';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'AI Chat', href: '/chat', icon: ChatBubbleLeftRightIcon },
  { name: 'Workflow', href: '/workflow', icon: PlayIcon },
  { name: 'Test Generator', href: '/test-generator', icon: SparklesIcon },
  { name: 'Test Monitor', href: '/test-monitor', icon: EyeIcon },
  { name: 'Analytics', href: '/analytics', icon: PresentationChartLineIcon },
  { name: 'Enterprise', href: '/enterprise', icon: BuildingOfficeIcon },
  { name: 'Test Builder', href: '/test-builder', icon: DocumentTextIcon },
  { name: 'Test Runner', href: '/test-runner', icon: BeakerIcon },
  { name: 'Reports', href: '/reports', icon: ChartBarIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

function Sidebar() {
  const location = useLocation();

  return (
    <div className="flex h-full w-64 flex-col bg-white border-r border-gray-200">
      <div className="flex h-16 items-center justify-center border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">🦖</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">Restaceratops</h1>
            <p className="text-xs text-gray-500">AI Testing Platform</p>
          </div>
        </div>
      </div>
      
      <nav className="flex-1 space-y-1 px-4 py-4">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-50 text-blue-700 border border-blue-200'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <item.icon
                className={`mr-3 h-5 w-5 flex-shrink-0 ${
                  isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                }`}
                aria-hidden="true"
              />
              {item.name}
            </Link>
          );
        })}
      </nav>
      
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-gray-600 text-sm font-medium">U</span>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">User</p>
            <p className="text-xs text-gray-500">user@example.com</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="/workflow" element={<WorkflowInterface />} />
            <Route path="/test-generator" element={<TestGenerator />} />
            <Route path="/test-monitor" element={<TestMonitor />} />
            <Route path="/analytics" element={<AnalyticsDashboard />} />
            <Route path="/enterprise" element={<EnterpriseDashboard />} />
            <Route path="/test-builder" element={<TestBuilder />} />
            <Route path="/test-runner" element={<TestRunner />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
