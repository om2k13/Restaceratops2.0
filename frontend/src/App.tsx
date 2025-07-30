import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import TestBuilder from './pages/TestBuilder'
import TestRunner from './pages/TestRunner'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import ChatInterface from './pages/ChatInterface'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <Router>
      <div className="h-screen flex overflow-hidden bg-gray-50">
        {/* Sidebar */}
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
        
        {/* Main content */}
        <div className="flex-1 overflow-auto focus:outline-none md:ml-64">
          <div className="relative z-10 flex-shrink-0 flex h-16 bg-white shadow">
            <button
              type="button"
              className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 md:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <span className="sr-only">Open sidebar</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            {/* Header */}
            <div className="flex-1 px-4 flex justify-between">
              <div className="flex-1 flex items-center">
                <h1 className="text-2xl font-semibold text-gray-900">
                  🦖 Restaceratops
                </h1>
              </div>
              <div className="ml-4 flex items-center md:ml-6">
                {/* Status indicator */}
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-500">System Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Page content */}
          <main className="flex-1 relative overflow-y-auto focus:outline-none">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/test-builder" element={<TestBuilder />} />
                  <Route path="/test-runner" element={<TestRunner />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/chat" element={<ChatInterface />} />
                  <Route path="/settings" element={<Settings />} />
                </Routes>
              </div>
            </div>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
