import { useState, useEffect } from 'react';
import { Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { apiService } from '../services/api';
import { websocketService } from '../services/websocket';
import type { DashboardStats } from '../services/api';
import type { DashboardUpdate, TestCompleted } from '../services/websocket';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await apiService.getDashboardStats();
        setStats(data);
        setError(null);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    // Initial data fetch
    fetchDashboardData();

    // Set up WebSocket connection
    const connectWebSocket = async () => {
      try {
        await websocketService.connect();
        setConnectionStatus('connected');
        
        // Subscribe to dashboard updates
        websocketService.subscribeToDashboard();
        
        // Subscribe to dashboard update messages
        const unsubscribeDashboard = websocketService.subscribeToDashboardUpdates((message: DashboardUpdate) => {
          setStats(message.data);
        });

        // Subscribe to test completion messages
        const unsubscribeTestCompleted = websocketService.subscribeToTestCompleted((_message: TestCompleted) => {
          // Refresh dashboard data when tests complete
          fetchDashboardData();
        });

        // Subscribe to pong messages for connection monitoring
        const unsubscribePong = websocketService.subscribeToPong(() => {
          setConnectionStatus('connected');
        });

        // Set up connection status monitoring
        const statusInterval = setInterval(() => {
          setConnectionStatus(websocketService.getConnectionStatus());
        }, 5000);

        return () => {
          unsubscribeDashboard();
          unsubscribeTestCompleted();
          unsubscribePong();
          clearInterval(statusInterval);
          websocketService.disconnect();
        };
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        setConnectionStatus('disconnected');
        // Fallback to polling if WebSocket fails
        const interval = setInterval(fetchDashboardData, 30000);
        return () => clearInterval(interval);
      }
    };

    const cleanup = connectWebSocket();

    return () => {
      cleanup.then(cleanupFn => cleanupFn && cleanupFn());
    };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-error-600 text-lg font-semibold mb-2">Error Loading Dashboard</div>
        <div className="text-gray-600">{error}</div>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 btn-primary"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!stats) {
    return <div>No data available</div>;
  }

  // Prepare chart data
  const responseTimeData = {
    labels: ['1m ago', '30s ago', 'Now'],
    datasets: [
      {
        label: 'Response Time (ms)',
        data: [stats.avg_response_time * 0.8, stats.avg_response_time * 1.1, stats.avg_response_time],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const testResultsData = {
    labels: ['Success', 'Error', 'Pending'],
    datasets: [
      {
        data: [
          Math.round(stats.total_tests * stats.success_rate),
          Math.round(stats.total_tests * (1 - stats.success_rate)),
          stats.running_tests,
        ],
        backgroundColor: [
          'rgb(34, 197, 94)',
          'rgb(239, 68, 68)',
          'rgb(245, 158, 11)',
        ],
        borderWidth: 0,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
    },
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'bg-success-500';
      case 'connecting': return 'bg-warning-500';
      case 'disconnected': return 'bg-error-500';
      default: return 'bg-gray-500';
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return 'Real-time Connected';
      case 'connecting': return 'Connecting...';
      case 'disconnected': return 'Real-time Disconnected';
      default: return 'Unknown';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${getConnectionStatusColor()} animate-pulse`}></div>
            <span className="text-sm text-gray-600">{getConnectionStatusText()}</span>
          </div>
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Tests</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.total_tests}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-success-100 rounded-lg">
              <svg className="w-6 h-6 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-2xl font-semibold text-gray-900">{(stats.success_rate * 100).toFixed(1)}%</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-warning-100 rounded-lg">
              <svg className="w-6 h-6 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.avg_response_time.toFixed(0)}ms</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-info-100 rounded-lg">
              <svg className="w-6 h-6 text-info-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Running Tests</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.running_tests}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Response Time Trend</h3>
          <Line data={responseTimeData} options={chartOptions} />
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Results Distribution</h3>
          <Doughnut data={testResultsData} options={chartOptions} />
        </div>
      </div>

      {/* Recent Results */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Test Results</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Test Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Response Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Code
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats.recent_results.map((result, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {result.test_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      result.status === 'success' 
                        ? 'bg-success-100 text-success-800' 
                        : 'bg-error-100 text-error-800'
                    }`}>
                      {result.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {result.response_time.toFixed(0)}ms
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {result.response_code}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 