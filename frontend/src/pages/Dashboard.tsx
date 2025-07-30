import { useState, useEffect } from 'react';
// Temporarily comment out Chart.js imports to test
// import { Line, Doughnut } from 'react-chartjs-2';
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend,
//   ArcElement,
// } from 'chart.js';
// import { apiService } from '../services/api';
// import { websocketService } from '../services/websocket';
// import type { DashboardStats } from '../services/api';
// import type { DashboardUpdate, TestCompleted } from '../services/websocket';

// Temporarily comment out Chart.js registration
// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend,
//   ArcElement
// );

const Dashboard = () => {
  // Simple test component without API calls
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">🦖 Restaceratops Dashboard</h1>
      <p className="text-gray-600 mb-4">Welcome to the AI-Powered Testing Platform!</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Total Tests</h3>
          <p className="text-3xl font-bold text-blue-600">150</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Success Rate</h3>
          <p className="text-3xl font-bold text-green-600">95%</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Avg Response</h3>
          <p className="text-3xl font-bold text-orange-600">245ms</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Running</h3>
          <p className="text-3xl font-bold text-purple-600">3</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Test Results</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-green-50 rounded">
            <span className="font-medium">User Authentication Test</span>
            <span className="text-green-600 font-semibold">✓ Success</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-green-50 rounded">
            <span className="font-medium">API Endpoint Test</span>
            <span className="text-green-600 font-semibold">✓ Success</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-red-50 rounded">
            <span className="font-medium">Database Connection Test</span>
            <span className="text-red-600 font-semibold">✗ Error</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-blue-800">
          <strong>Status:</strong> Frontend is working! The dashboard is now rendering correctly.
        </p>
      </div>
    </div>
  );
};

export default Dashboard; 