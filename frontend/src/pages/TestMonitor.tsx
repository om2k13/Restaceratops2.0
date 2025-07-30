import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  PlayIcon, 
  StopIcon, 
  ChartBarIcon, 
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  EyeIcon,
  CogIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';

interface ExecutionSession {
  session_id: string;
  name: string;
  description: string;
  start_time: string;
  end_time?: string;
  status: string;
  duration?: number;
  metrics: {
    total_tests: number;
    passed_tests: number;
    failed_tests: number;
    success_rate: number;
    performance_level: string;
    bottlenecks?: string[];
    recommendations?: string[];
  };
}

interface PerformanceReport {
  session_id: string;
  session_name: string;
  overall_metrics: {
    total_tests: number;
    success_rate: number;
    performance_level: string;
    total_duration: number;
    average_duration: number;
    average_response_time: number;
  };
  status_breakdown: Record<string, {
    count: number;
    percentage: number;
    average_duration: number;
    average_response_time: number;
  }>;
  performance_trends: {
    moving_average_duration: number[];
    moving_average_response_time: number[];
    trend_direction: string;
  };
  top_performers: Array<{
    test_name: string;
    duration: number;
    response_time: number;
    rank: number;
  }>;
  problematic_tests: Array<{
    test_name: string;
    total_runs: number;
    success_rate: number;
    average_duration: number;
    average_response_time: number;
    issues: {
      failures: number;
      errors: number;
      timeouts: number;
    };
  }>;
  bottlenecks: string[];
  recommendations: string[];
}

const TestMonitor: React.FC = () => {
  const [sessions, setSessions] = useState<{ active_sessions: ExecutionSession[], completed_sessions: ExecutionSession[] }>({
    active_sessions: [],
    completed_sessions: []
  });
  const [selectedSession, setSelectedSession] = useState<ExecutionSession | null>(null);
  const [performanceReport, setPerformanceReport] = useState<PerformanceReport | null>(null);
  const [globalStats, setGlobalStats] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'sessions' | 'performance' | 'analytics'>('sessions');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchSessions();
    fetchGlobalStats();
    
    // Set up polling for real-time updates
    const interval = setInterval(() => {
      fetchSessions();
      fetchGlobalStats();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await fetch('/api/workflow/execution/sessions');
      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchGlobalStats = async () => {
    try {
      const response = await fetch('/api/workflow/execution/global-stats');
      if (response.ok) {
        const data = await response.json();
        setGlobalStats(data);
      }
    } catch (error) {
      console.error('Error fetching global stats:', error);
    }
  };

  const fetchPerformanceReport = async (sessionId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/workflow/execution/session/${sessionId}/performance`);
      if (response.ok) {
        const data = await response.json();
        setPerformanceReport(data);
      }
    } catch (error) {
      console.error('Error fetching performance report:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPerformanceLevelColor = (level: string) => {
    switch (level) {
      case 'excellent': return 'bg-green-100 text-green-800';
      case 'good': return 'bg-blue-100 text-blue-800';
      case 'fair': return 'bg-yellow-100 text-yellow-800';
      case 'poor': return 'bg-orange-100 text-orange-800';
      case 'critical': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(0)}s`;
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🦖 Test Execution Monitor
          </h1>
          <p className="text-xl text-gray-600">
            Real-time Test Execution Monitoring & Performance Analytics
          </p>
        </motion.div>

        {/* Global Stats Cards */}
        {globalStats && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
          >
            <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-3xl font-bold">{globalStats.total_sessions || 0}</div>
                  <div className="text-sm opacity-90">Total Sessions</div>
                </div>
                <ChartBarIcon className="w-8 h-8 opacity-80" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-3xl font-bold">{globalStats.total_tests || 0}</div>
                  <div className="text-sm opacity-90">Total Tests</div>
                </div>
                <PlayIcon className="w-8 h-8 opacity-80" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-3xl font-bold">{(globalStats.overall_success_rate || 0).toFixed(1)}%</div>
                  <div className="text-sm opacity-90">Success Rate</div>
                </div>
                <ArrowTrendingUpIcon className="w-8 h-8 opacity-80" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-orange-400 to-orange-600 text-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-3xl font-bold">{globalStats.active_sessions || 0}</div>
                  <div className="text-sm opacity-90">Active Sessions</div>
                </div>
                <ClockIcon className="w-8 h-8 opacity-80" />
              </div>
            </div>
          </motion.div>
        )}

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-lg p-1">
            <div className="flex space-x-1">
              {[
                { id: 'sessions', label: 'Sessions', icon: PlayIcon },
                { id: 'performance', label: 'Performance', icon: ChartBarIcon },
                { id: 'analytics', label: 'Analytics', icon: ArrowTrendingUpIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-xl shadow-xl p-8"
        >
          {activeTab === 'sessions' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Test Execution Sessions
              </h2>

              {/* Active Sessions */}
              {sessions.active_sessions.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                    Active Sessions ({sessions.active_sessions.length})
                  </h3>
                  <div className="space-y-4">
                    {sessions.active_sessions.map((session) => (
                      <motion.div
                        key={session.session_id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="border border-green-200 bg-green-50 rounded-lg p-6 hover:shadow-md transition-shadow"
                      >
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="text-lg font-semibold text-gray-900 mb-2">
                              {session.name}
                            </h4>
                            <p className="text-gray-600 mb-2">{session.description}</p>
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <span>Started: {formatDateTime(session.start_time)}</span>
                              <span>Tests: {session.metrics.total_tests}</span>
                              <span>Success Rate: {session.metrics.success_rate.toFixed(1)}%</span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(session.status)}`}>
                              {session.status}
                            </span>
                            <button
                              onClick={() => {
                                setSelectedSession(session);
                                fetchPerformanceReport(session.session_id);
                                setActiveTab('performance');
                              }}
                              className="p-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                            >
                              <EyeIcon className="w-5 h-5" />
                            </button>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Completed Sessions */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Completed Sessions ({sessions.completed_sessions.length})
                </h3>
                <div className="space-y-4">
                  {sessions.completed_sessions.slice(0, 10).map((session) => (
                    <motion.div
                      key={session.session_id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-lg font-semibold text-gray-900 mb-2">
                            {session.name}
                          </h4>
                          <p className="text-gray-600 mb-2">{session.description}</p>
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>Started: {formatDateTime(session.start_time)}</span>
                            {session.end_time && (
                              <span>Ended: {formatDateTime(session.end_time)}</span>
                            )}
                            {session.duration && (
                              <span>Duration: {formatDuration(session.duration)}</span>
                            )}
                            <span>Tests: {session.metrics.total_tests}</span>
                            <span>Success Rate: {session.metrics.success_rate.toFixed(1)}%</span>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(session.status)}`}>
                            {session.status}
                          </span>
                          <span className={`px-3 py-1 text-sm font-medium rounded-full ${getPerformanceLevelColor(session.metrics.performance_level)}`}>
                            {session.metrics.performance_level}
                          </span>
                          <button
                            onClick={() => {
                              setSelectedSession(session);
                              fetchPerformanceReport(session.session_id);
                              setActiveTab('performance');
                            }}
                            className="p-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                          >
                            <EyeIcon className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'performance' && selectedSession && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Performance Report: {selectedSession.name}
                </h2>
                <button
                  onClick={() => setActiveTab('sessions')}
                  className="px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  ← Back to Sessions
                </button>
              </div>

              {isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
              ) : performanceReport ? (
                <div className="space-y-8">
                  {/* Overall Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-lg">
                      <div className="text-3xl font-bold">{performanceReport.overall_metrics.total_tests}</div>
                      <div className="text-sm opacity-90">Total Tests</div>
                    </div>
                    <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-lg">
                      <div className="text-3xl font-bold">{performanceReport.overall_metrics.success_rate.toFixed(1)}%</div>
                      <div className="text-sm opacity-90">Success Rate</div>
                    </div>
                    <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-lg">
                      <div className="text-3xl font-bold">{formatDuration(performanceReport.overall_metrics.average_duration)}</div>
                      <div className="text-sm opacity-90">Avg Duration</div>
                    </div>
                    <div className="bg-gradient-to-r from-orange-400 to-orange-600 text-white p-6 rounded-lg">
                      <div className="text-3xl font-bold">{performanceReport.overall_metrics.average_response_time.toFixed(0)}ms</div>
                      <div className="text-sm opacity-90">Avg Response</div>
                    </div>
                  </div>

                  {/* Status Breakdown */}
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Status Breakdown</h3>
                    <div className="space-y-3">
                      {Object.entries(performanceReport.status_breakdown).map(([status, data]) => (
                        <div key={status} className="flex items-center justify-between">
                          <span className="capitalize text-gray-700">{status}</span>
                          <div className="flex items-center space-x-4">
                            <span className="text-sm font-medium text-gray-900">{data.count} tests</span>
                            <span className="text-sm text-gray-500">({data.percentage.toFixed(1)}%)</span>
                            <span className="text-sm text-gray-500">{formatDuration(data.average_duration)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Top Performers */}
                  {performanceReport.top_performers.length > 0 && (
                    <div className="bg-green-50 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performers</h3>
                      <div className="space-y-2">
                        {performanceReport.top_performers.map((test, index) => (
                          <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="text-sm font-medium text-gray-900">#{test.rank}</span>
                              <span className="text-sm text-gray-700">{test.test_name}</span>
                            </div>
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <span>{formatDuration(test.duration)}</span>
                              <span>{test.response_time.toFixed(0)}ms</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Problematic Tests */}
                  {performanceReport.problematic_tests.length > 0 && (
                    <div className="bg-red-50 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Problematic Tests</h3>
                      <div className="space-y-4">
                        {performanceReport.problematic_tests.map((test, index) => (
                          <div key={index} className="border border-red-200 rounded-lg p-4">
                            <div className="flex justify-between items-start mb-2">
                              <span className="font-medium text-gray-900">{test.test_name}</span>
                              <span className="text-sm text-red-600">{test.success_rate.toFixed(1)}% success</span>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                              <span>Runs: {test.total_runs}</span>
                              <span>Avg Duration: {formatDuration(test.average_duration)}</span>
                              <span>Failures: {test.issues.failures}</span>
                              <span>Errors: {test.issues.errors}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommendations */}
                  {performanceReport.recommendations.length > 0 && (
                    <div className="bg-blue-50 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
                      <ul className="space-y-2">
                        {performanceReport.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <CogIcon className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-gray-700">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  No performance data available for this session.
                </div>
              )}
            </div>
          )}

          {activeTab === 'analytics' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Analytics Dashboard
              </h2>
              <div className="text-center py-12 text-gray-500">
                Advanced analytics features coming soon...
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default TestMonitor; 