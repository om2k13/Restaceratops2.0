import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon, 
    ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  EyeIcon,
  CogIcon,
  DocumentTextIcon,
  PlayIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  StarIcon
} from '@heroicons/react/24/outline';

interface AnalyticsData {
  test_generation_stats: {
    total_tests_generated: number;
    total_stories_processed: number;
    average_tests_per_story: number;
    test_type_distribution: Record<string, number>;
  };
  execution_stats: {
    total_sessions: number;
    total_tests: number;
    overall_success_rate: number;
    average_duration: number;
    average_response_time: number;
  };
  evaluation_stats: {
    total_evaluations: number;
    average_confidence: number;
    evaluation_level_distribution: Record<string, number>;
  };
  trends: {
    daily_tests: Array<{ date: string; count: number }>;
    success_rates: Array<{ date: string; rate: number }>;
    performance_metrics: Array<{ date: string; duration: number; response_time: number }>;
  };
}

interface EvaluationResult {
  test_id: string;
  test_name: string;
  evaluation_metrics: Record<string, number>;
  evaluation_level: string;
  confidence_score: number;
  recommendations: string[];
}

const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [evaluationResults, setEvaluationResults] = useState<EvaluationResult[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'trends' | 'evaluations' | 'performance'>('overview');
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('30d');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsData();
    fetchEvaluationResults();
  }, [timeRange]);

  const fetchAnalyticsData = async () => {
    setIsLoading(true);
    try {
      // Fetch test generation stats
      const genResponse = await fetch('/api/workflow/test-generation/stats');
      const genStats = genResponse.ok ? await genResponse.json() : {};

      // Fetch execution stats
      const execResponse = await fetch('/api/workflow/execution/global-stats');
      const execStats = execResponse.ok ? await execResponse.json() : {};

      // Fetch evaluation stats
      const evalResponse = await fetch('/api/workflow/evaluation/stats');
      const evalStats = evalResponse.ok ? await evalResponse.json() : {};

      // Mock trends data (in real implementation, this would come from the API)
      const trends = {
        daily_tests: generateMockTrendData(30),
        success_rates: generateMockSuccessRates(30),
        performance_metrics: generateMockPerformanceData(30)
      };

      setAnalyticsData({
        test_generation_stats: genStats,
        execution_stats: execStats,
        evaluation_stats: evalStats,
        trends
      });
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchEvaluationResults = async () => {
    try {
      const response = await fetch('/api/workflow/evaluation/results');
      if (response.ok) {
        const data = await response.json();
        setEvaluationResults(data.results || []);
      }
    } catch (error) {
      console.error('Error fetching evaluation results:', error);
    }
  };

  const generateMockTrendData = (days: number) => {
    const data = [];
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      data.push({
        date: date.toISOString().split('T')[0],
        count: Math.floor(Math.random() * 50) + 10
      });
    }
    return data;
  };

  const generateMockSuccessRates = (days: number) => {
    const data = [];
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      data.push({
        date: date.toISOString().split('T')[0],
        rate: Math.random() * 0.3 + 0.7 // 70-100%
      });
    }
    return data;
  };

  const generateMockPerformanceData = (days: number) => {
    const data = [];
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      data.push({
        date: date.toISOString().split('T')[0],
        duration: Math.random() * 5 + 1, // 1-6 seconds
        response_time: Math.random() * 200 + 50 // 50-250ms
      });
    }
    return data;
  };

  const getEvaluationLevelColor = (level: string) => {
    switch (level) {
      case 'excellent': return 'bg-green-100 text-green-800';
      case 'good': return 'bg-blue-100 text-blue-800';
      case 'fair': return 'bg-yellow-100 text-yellow-800';
      case 'poor': return 'bg-orange-100 text-orange-800';
      case 'critical': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;
  const formatDuration = (seconds: number) => `${seconds.toFixed(1)}s`;
  const formatResponseTime = (ms: number) => `${ms.toFixed(0)}ms`;

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🦖 Analytics Dashboard
          </h1>
          <p className="text-xl text-gray-600">
            Comprehensive Analytics & Performance Insights
          </p>
        </motion.div>

        {/* Time Range Selector */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-lg p-1">
            <div className="flex space-x-1">
              {[
                { value: '7d', label: '7 Days' },
                { value: '30d', label: '30 Days' },
                { value: '90d', label: '90 Days' }
              ].map((range) => (
                <button
                  key={range.value}
                  onClick={() => setTimeRange(range.value as any)}
                  className={`px-4 py-2 rounded-md transition-all duration-200 ${
                    timeRange === range.value
                      ? 'bg-purple-500 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  {range.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-lg p-1">
            <div className="flex space-x-1">
              {[
                { id: 'overview', label: 'Overview', icon: EyeIcon },
                { id: 'trends', label: 'Trends', icon: ArrowTrendingUpIcon },
                { id: 'evaluations', label: 'Evaluations', icon: ChartBarIcon },
                { id: 'performance', label: 'Performance', icon: CogIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-purple-500 text-white shadow-md'
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
          {activeTab === 'overview' && analyticsData && (
            <div className="space-y-8">
              {/* Key Metrics Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-lg shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-3xl font-bold">{analyticsData.test_generation_stats.total_tests_generated || 0}</div>
                      <div className="text-sm opacity-90">Tests Generated</div>
                    </div>
                    <DocumentTextIcon className="w-8 h-8 opacity-80" />
                  </div>
                </div>
                <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-lg shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-3xl font-bold">{analyticsData.execution_stats.total_tests || 0}</div>
                      <div className="text-sm opacity-90">Tests Executed</div>
                    </div>
                    <PlayIcon className="w-8 h-8 opacity-80" />
                  </div>
                </div>
                <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-lg shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-3xl font-bold">{formatPercentage(analyticsData.execution_stats.overall_success_rate || 0)}</div>
                      <div className="text-sm opacity-90">Success Rate</div>
                    </div>
                    <CheckCircleIcon className="w-8 h-8 opacity-80" />
                  </div>
                </div>
                <div className="bg-gradient-to-r from-orange-400 to-orange-600 text-white p-6 rounded-lg shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-3xl font-bold">{analyticsData.evaluation_stats.total_evaluations || 0}</div>
                      <div className="text-sm opacity-90">Evaluations</div>
                    </div>
                    <StarIcon className="w-8 h-8 opacity-80" />
                  </div>
                </div>
              </div>

              {/* Test Type Distribution */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Type Distribution</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(analyticsData.test_generation_stats.test_type_distribution || {}).map(([type, count]) => (
                    <div key={type} className="bg-white rounded-lg p-4 shadow-sm">
                      <div className="text-2xl font-bold text-gray-900">{count}</div>
                      <div className="text-sm text-gray-600 capitalize">{type.replace('_', ' ')}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Average Duration</span>
                      <span className="font-medium">{formatDuration(analyticsData.execution_stats.average_duration || 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Average Response Time</span>
                      <span className="font-medium">{formatResponseTime(analyticsData.execution_stats.average_response_time || 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Evaluation Confidence</span>
                      <span className="font-medium">{formatPercentage(analyticsData.evaluation_stats.average_confidence || 0)}</span>
                    </div>
                  </div>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Evaluation Levels</h3>
                  <div className="space-y-3">
                    {Object.entries(analyticsData.evaluation_stats.evaluation_level_distribution || {}).map(([level, count]) => (
                      <div key={level} className="flex items-center justify-between">
                        <span className="capitalize text-gray-600">{level}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                level === 'excellent' ? 'bg-green-500' :
                                level === 'good' ? 'bg-blue-500' :
                                level === 'fair' ? 'bg-yellow-500' :
                                level === 'poor' ? 'bg-orange-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${(count / (analyticsData.evaluation_stats.total_evaluations || 1)) * 100}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium text-gray-900">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'trends' && analyticsData && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Trend Analysis</h2>
              
              {/* Daily Test Generation */}
              <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Test Generation</h3>
                <div className="h-64 flex items-end space-x-2">
                  {analyticsData.trends.daily_tests.slice(-14).map((data, index) => (
                    <div key={index} className="flex-1 bg-purple-500 rounded-t" style={{ height: `${(data.count / 60) * 100}%` }}>
                      <div className="text-xs text-center text-gray-600 mt-2">{data.count}</div>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-2">
                  <span>14 days ago</span>
                  <span>Today</span>
                </div>
              </div>

              {/* Success Rate Trends */}
              <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Success Rate Trends</h3>
                <div className="h-64 flex items-end space-x-2">
                  {analyticsData.trends.success_rates.slice(-14).map((data, index) => (
                    <div key={index} className="flex-1 bg-green-500 rounded-t" style={{ height: `${data.rate * 100}%` }}>
                      <div className="text-xs text-center text-gray-600 mt-2">{formatPercentage(data.rate)}</div>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-2">
                  <span>14 days ago</span>
                  <span>Today</span>
                </div>
              </div>

              {/* Performance Trends */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Duration Trends</h3>
                  <div className="space-y-2">
                    {analyticsData.trends.performance_metrics.slice(-7).map((data, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{data.date}</span>
                        <span className="text-sm font-medium">{formatDuration(data.duration)}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Response Time Trends</h3>
                  <div className="space-y-2">
                    {analyticsData.trends.performance_metrics.slice(-7).map((data, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{data.date}</span>
                        <span className="text-sm font-medium">{formatResponseTime(data.response_time)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'evaluations' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Evaluation Results</h2>
              
              <div className="space-y-4">
                {evaluationResults.map((result, index) => (
                  <motion.div
                    key={result.test_id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{result.test_name}</h3>
                        <p className="text-gray-600">Test ID: {result.test_id}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-3 py-1 text-sm font-medium rounded-full ${getEvaluationLevelColor(result.evaluation_level)}`}>
                          {result.evaluation_level}
                        </span>
                        <span className="text-sm text-gray-500">{formatPercentage(result.confidence_score)}</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      {Object.entries(result.evaluation_metrics).slice(0, 4).map(([metric, value]) => (
                        <div key={metric} className="text-center">
                          <div className="text-lg font-bold text-gray-900">{formatPercentage(value)}</div>
                          <div className="text-xs text-gray-600 capitalize">{metric.replace('_', ' ')}</div>
                        </div>
                      ))}
                    </div>

                    {result.recommendations.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Recommendations</h4>
                        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                          {result.recommendations.map((rec, i) => (
                            <li key={i}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'performance' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Analytics</h2>
              <div className="text-center py-12 text-gray-500">
                Advanced performance analytics features coming soon...
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard; 