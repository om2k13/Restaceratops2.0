import { useState, useEffect } from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
// import { apiService } from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface TestReport {
  id: string;
  name: string;
  status: 'success' | 'failed' | 'partial';
  totalTests: number;
  passedTests: number;
  failedTests: number;
  avgResponseTime: number;
  startTime: Date;
  endTime: Date;
  duration: number;
  results: TestResult[];
}

interface TestResult {
  test_name: string;
  status: 'success' | 'failed';
  response_time: number;
  response_code: number;
  response_body: string;
  error?: string;
}

const Reports = () => {
  const [reports, setReports] = useState<TestReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<TestReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d' | 'all'>('7d');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true);
        // Mock data for now - in real implementation, this would come from the API
        const mockReports: TestReport[] = [
          {
            id: '1',
            name: 'User API Test Suite',
            status: 'success',
            totalTests: 15,
            passedTests: 15,
            failedTests: 0,
            avgResponseTime: 245.6,
            startTime: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
            endTime: new Date(Date.now() - 2 * 60 * 60 * 1000 + 30000), // 30 seconds later
            duration: 30000,
            results: [
              {
                test_name: 'User Authentication',
                status: 'success',
                response_time: 180.2,
                response_code: 200,
                response_body: 'Token generated successfully'
              },
              {
                test_name: 'User Profile Retrieval',
                status: 'success',
                response_time: 120.5,
                response_code: 200,
                response_body: 'Profile data retrieved'
              },
              {
                test_name: 'User Update',
                status: 'success',
                response_time: 210.8,
                response_code: 200,
                response_body: 'User updated successfully'
              }
            ]
          },
          {
            id: '2',
            name: 'Payment API Test Suite',
            status: 'partial',
            totalTests: 8,
            passedTests: 6,
            failedTests: 2,
            avgResponseTime: 320.1,
            startTime: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
            endTime: new Date(Date.now() - 4 * 60 * 60 * 1000 + 25000), // 25 seconds later
            duration: 25000,
            results: [
              {
                test_name: 'Payment Processing',
                status: 'success',
                response_time: 450.3,
                response_code: 200,
                response_body: 'Payment processed successfully'
              },
              {
                test_name: 'Payment Validation',
                status: 'failed',
                response_time: 95.8,
                response_code: 400,
                response_body: 'Invalid payment data',
                error: 'Validation failed for payment amount'
              },
              {
                test_name: 'Refund Processing',
                status: 'success',
                response_time: 280.5,
                response_code: 200,
                response_body: 'Refund processed successfully'
              }
            ]
          },
          {
            id: '3',
            name: 'Data API Test Suite',
            status: 'failed',
            totalTests: 12,
            passedTests: 3,
            failedTests: 9,
            avgResponseTime: 180.9,
            startTime: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
            endTime: new Date(Date.now() - 6 * 60 * 60 * 1000 + 15000), // 15 seconds later
            duration: 15000,
            results: [
              {
                test_name: 'Data Export',
                status: 'success',
                response_time: 120.1,
                response_code: 200,
                response_body: 'Data exported successfully'
              },
              {
                test_name: 'Data Import',
                status: 'failed',
                response_time: 5000,
                response_code: 500,
                response_body: 'Internal server error',
                error: 'Database connection timeout'
              },
              {
                test_name: 'Data Validation',
                status: 'failed',
                response_time: 85.2,
                response_code: 422,
                response_body: 'Validation failed',
                error: 'Invalid data format'
              }
            ]
          }
        ];

        setReports(mockReports);
        setError(null);
      } catch (err) {
        setError('Failed to load reports');
        console.error('Load reports error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [timeRange]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'bg-success-500';
      case 'failed': return 'bg-error-500';
      case 'partial': return 'bg-warning-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'success': return 'Success';
      case 'failed': return 'Failed';
      case 'partial': return 'Partial';
      default: return 'Unknown';
    }
  };

  const getSuccessRate = (report: TestReport) => {
    return (report.passedTests / report.totalTests) * 100;
  };

  // Chart data for overall statistics
  const overallStats = {
    totalReports: reports.length,
    totalTests: reports.reduce((sum, report) => sum + report.totalTests, 0),
    totalPassed: reports.reduce((sum, report) => sum + report.passedTests, 0),
    totalFailed: reports.reduce((sum, report) => sum + report.failedTests, 0),
    avgResponseTime: reports.length > 0 
      ? reports.reduce((sum, report) => sum + report.avgResponseTime, 0) / reports.length 
      : 0,
    successRate: reports.length > 0
      ? (reports.reduce((sum, report) => sum + report.passedTests, 0) / 
         reports.reduce((sum, report) => sum + report.totalTests, 0)) * 100
      : 0
  };

  // Chart data
  const successRateData = {
    labels: reports.map(report => report.name),
    datasets: [
      {
        label: 'Success Rate (%)',
        data: reports.map(report => getSuccessRate(report)),
        backgroundColor: reports.map(report => 
          report.status === 'success' ? 'rgba(34, 197, 94, 0.8)' :
          report.status === 'failed' ? 'rgba(239, 68, 68, 0.8)' :
          'rgba(245, 158, 11, 0.8)'
        ),
        borderColor: reports.map(report => 
          report.status === 'success' ? 'rgb(34, 197, 94)' :
          report.status === 'failed' ? 'rgb(239, 68, 68)' :
          'rgb(245, 158, 11)'
        ),
        borderWidth: 1,
      },
    ],
  };

  const responseTimeData = {
    labels: reports.map(report => report.name),
    datasets: [
      {
        label: 'Average Response Time (ms)',
        data: reports.map(report => report.avgResponseTime),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const testResultsData = {
    labels: ['Passed', 'Failed'],
    datasets: [
      {
        data: [overallStats.totalPassed, overallStats.totalFailed],
        backgroundColor: [
          'rgb(34, 197, 94)',
          'rgb(239, 68, 68)',
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
        <div className="text-error-600 text-lg font-semibold mb-2">Error Loading Reports</div>
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Test Reports</h1>
          <p className="text-sm text-gray-600 mt-1">
            Detailed analysis of test execution results and performance metrics
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="input-field w-auto"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="all">All Time</option>
          </select>
          <button className="btn-primary text-sm">
            Export Report
          </button>
        </div>
      </div>

      {/* Overall Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Reports</p>
              <p className="text-2xl font-semibold text-gray-900">{overallStats.totalReports}</p>
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
              <p className="text-2xl font-semibold text-gray-900">{overallStats.successRate.toFixed(1)}%</p>
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
              <p className="text-2xl font-semibold text-gray-900">{overallStats.avgResponseTime.toFixed(0)}ms</p>
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
              <p className="text-sm font-medium text-gray-600">Total Tests</p>
              <p className="text-2xl font-semibold text-gray-900">{overallStats.totalTests}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Success Rate by Test Suite</h3>
          <Bar data={successRateData} options={chartOptions} />
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Results Distribution</h3>
          <Doughnut data={testResultsData} options={chartOptions} />
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Response Time Trends</h3>
        <Line data={responseTimeData} options={chartOptions} />
      </div>

      {/* Detailed Reports */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Reports</h3>
        
        {reports.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p className="text-sm">No reports available</p>
            <p className="text-xs">Run some tests to generate reports</p>
          </div>
        ) : (
          <div className="space-y-4">
            {reports.map((report) => (
              <div key={report.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(report.status)}`}></div>
                    <div>
                      <h4 className="text-lg font-medium text-gray-900">{report.name}</h4>
                      <p className="text-sm text-gray-500">
                        {report.startTime.toLocaleString()} - {report.duration}ms
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(report.status)} text-white`}>
                      {getStatusText(report.status)}
                    </span>
                    <button
                      onClick={() => setSelectedReport(selectedReport?.id === report.id ? null : report)}
                      className="text-primary-600 hover:text-primary-800"
                    >
                      {selectedReport?.id === report.id ? 'Hide Details' : 'View Details'}
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{report.totalTests}</div>
                    <div className="text-xs text-gray-500">Total Tests</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-success-600">{report.passedTests}</div>
                    <div className="text-xs text-gray-500">Passed</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-error-600">{report.failedTests}</div>
                    <div className="text-xs text-gray-500">Failed</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{report.avgResponseTime.toFixed(0)}ms</div>
                    <div className="text-xs text-gray-500">Avg Response</div>
                  </div>
                </div>

                {selectedReport?.id === report.id && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <h5 className="font-medium text-gray-900 mb-2">Test Results</h5>
                    <div className="space-y-2">
                      {report.results.map((result, index) => (
                        <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                          <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${result.status === 'success' ? 'bg-success-500' : 'bg-error-500'}`}></div>
                            <span className="text-sm font-medium">{result.test_name}</span>
                          </div>
                          <div className="flex items-center space-x-4 text-xs text-gray-500">
                            <span>{result.response_time}ms</span>
                            <span>Code: {result.response_code}</span>
                            <span className={`px-2 py-1 rounded ${result.status === 'success' ? 'bg-success-100 text-success-800' : 'bg-error-100 text-error-800'}`}>
                              {result.status}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Reports; 