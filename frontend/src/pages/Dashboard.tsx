import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { DashboardStats } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await apiService.getDashboardStats();
        setStats(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading dashboard data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">
            <strong>Error:</strong> {error}
          </p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">No dashboard data available.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">🦖 Restaceratops Dashboard</h1>
      <p className="text-gray-600 mb-4">Welcome to the AI-Powered Testing Platform!</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Total Tests</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.total_tests}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Success Rate</h3>
          <p className="text-3xl font-bold text-green-600">{(stats.success_rate * 100).toFixed(0)}%</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Avg Response</h3>
          <p className="text-3xl font-bold text-orange-600">{stats.avg_response_time}ms</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900">Running</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.running_tests}</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Test Results</h3>
        <div className="space-y-3">
          {stats.recent_results.map((result, index) => (
            <div 
              key={index}
              className={`flex items-center justify-between p-3 rounded ${
                result.status === 'success' ? 'bg-green-50' : 'bg-red-50'
              }`}
            >
              <div className="flex-1">
                <span className="font-medium">{result.test_name}</span>
                <div className="text-sm text-gray-500">
                  Response: {result.response_time}ms | Code: {result.response_code}
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`font-semibold ${
                  result.status === 'success' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {result.status === 'success' ? '✓ Success' : '✗ Error'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-blue-800">
          <strong>Status:</strong> Dashboard connected to real backend data! 
          Last updated: {new Date().toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
};

export default Dashboard; 