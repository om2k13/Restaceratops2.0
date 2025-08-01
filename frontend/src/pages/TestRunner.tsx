import React, { useState } from 'react';
import { apiService } from '../services/api';

interface TestResult {
  test_name: string;
  status: string;
  response_time: number;
  response_code: number;
  response_body: string;
  error?: string;
  timestamp: string;
}

interface TestExecutionResult {
  execution_id: string;
  status: string;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  success_rate: number;
  avg_response_time: number;
  results: TestResult[];
  test_file: string;
  timestamp: string;
}

const CleanTestRunner: React.FC = () => {
  const [testFile, setTestFile] = useState('tests/simple_test.yml');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<TestExecutionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showReport, setShowReport] = useState(false);

  const availableTestFiles = [
    'backend/tests/simple_test.yml',
    'backend/tests/comprehensive_test.yml',
    'backend/tests/real-world-example.yml',
    'backend/tests/production_ready.yml',
    'backend/tests/advanced_features.yml',
    'backend/tests/my-api-example.yml',
    'tests/simple_test.yml',
    'tests/comprehensive_test.yml',
    'tests/real-world-example.yml',
    'tests/production_ready.yml',
    'tests/generated_openrouter.yml'
  ];

  const runTests = async () => {
    if (!testFile && !uploadedFile) {
      setError('Please select a test file or upload one');
      return;
    }

    setIsRunning(true);
    setError(null);
    setResults(null);
    setShowReport(false);

    try {
      let fileToUse = testFile;
      
      // If user uploaded a file, use that instead
      if (uploadedFile) {
        // For now, we'll use the uploaded file name
        // In a real implementation, you'd upload the file to the backend
        fileToUse = uploadedFile.name;
      }

      // Call the backend directly - it returns results immediately
      const response = await apiService.runTests({
        test_files: [fileToUse],
        parallel: true,
        timeout: 30000
      });

      // The backend returns results directly, no need to poll
      const formattedResults: TestExecutionResult = {
        execution_id: response.execution_id,
        status: response.status,
        total_tests: response.total_tests,
        passed_tests: response.passed_tests,
        failed_tests: response.failed_tests,
        success_rate: response.success_rate,
        avg_response_time: response.avg_response_time,
        results: response.results.map((r: any) => ({
          test_name: r.test_name,
          status: r.status,
          response_time: r.response_time,
          response_code: r.response_code,
          response_body: r.response_body,
          error: r.error,
          timestamp: r.timestamp
        })),
        test_file: fileToUse,
        timestamp: response.timestamp
      };
      
      setResults(formattedResults);
      setShowReport(true);
      setIsRunning(false);
      
    } catch (err) {
      console.error('Test execution error:', err);
      setError('Failed to execute tests');
      setIsRunning(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      setTestFile(''); // Clear dropdown selection
    }
  };

  const generateReport = () => {
    if (!results) return '';

    const report = `
# 🦖 Restaceratops Test Report

**Execution ID:** ${results.execution_id}
**Test File:** ${results.test_file}
**Timestamp:** ${new Date(results.timestamp).toLocaleString()}

## 📊 Summary
- **Total Tests:** ${results.total_tests}
- **Passed:** ${results.passed_tests}
- **Failed:** ${results.failed_tests}
- **Success Rate:** ${results.success_rate.toFixed(1)}%
- **Average Response Time:** ${results.avg_response_time.toFixed(0)}ms

## 📋 Detailed Results

${results.results.map((result, index) => `
### Test ${index + 1}: ${result.test_name}
- **Status:** ${result.status}
- **Response Time:** ${result.response_time}ms
- **Response Code:** ${result.response_code}
${result.error ? `- **Error:** ${result.error}` : ''}
`).join('')}

## 🎯 Recommendations
${results.success_rate >= 90 ? '✅ Excellent test performance!' : 
  results.success_rate >= 70 ? '⚠️ Some tests failed. Review failed tests.' : 
  '❌ Multiple test failures. Investigate API issues.'}
    `;

    return report;
  };

  const downloadReport = () => {
    const report = generateReport();
    const blob = new Blob([report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `restaceratops-report-${results?.execution_id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🧪 Test Runner</h1>
        <p className="text-gray-600">Execute API tests and generate comprehensive reports</p>
      </div>

      {/* Test Configuration */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Test Configuration</h2>
        
        <div className="space-y-4">
          <div>
            <label htmlFor="testFile" className="block text-sm font-medium text-gray-700 mb-2">
              Test File
            </label>
            <select
              id="testFile"
              value={testFile}
              onChange={(e) => setTestFile(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              disabled={!!uploadedFile}
            >
              {availableTestFiles.map((file) => (
                <option key={file} value={file}>
                  {file}
                </option>
              ))}
            </select>
          </div>
          
          <div className="border-t pt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Or Upload Custom Test File
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="file"
                accept=".yml,.yaml"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              {uploadedFile && (
                <button
                  onClick={() => {
                    setUploadedFile(null);
                    setTestFile('tests/simple_test.yml');
                  }}
                  className="px-3 py-2 text-sm text-red-600 hover:text-red-800"
                >
                  Clear
                </button>
              )}
            </div>
            {uploadedFile && (
              <p className="mt-2 text-sm text-green-600">
                ✅ Using uploaded file: {uploadedFile.name}
              </p>
            )}
          </div>

          <button
            onClick={runTests}
            disabled={isRunning}
            className={`w-full px-4 py-2 text-white font-medium rounded-md ${
              isRunning
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }`}
          >
            {isRunning ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Running Tests...
              </div>
            ) : (
              'Run Tests'
            )}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Test Results Summary</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{results.total_tests}</div>
                <div className="text-sm text-gray-500">Total Tests</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{results.passed_tests}</div>
                <div className="text-sm text-gray-500">Passed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">{results.failed_tests}</div>
                <div className="text-sm text-gray-500">Failed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{results.success_rate.toFixed(1)}%</div>
                <div className="text-sm text-gray-500">Success Rate</div>
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={() => setShowReport(!showReport)}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
              >
                {showReport ? 'Hide' : 'Show'} Detailed Report
              </button>
              <button
                onClick={downloadReport}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                Download Report
              </button>
            </div>
          </div>

          {/* Detailed Results */}
          {showReport && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Detailed Test Results</h2>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Response Time</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Response Code</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {results.results.map((result, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {result.test_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            result.status === 'passed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {result.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {result.response_time}ms
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {result.response_code}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {result.error ? (
                            <span className="text-red-600">{result.error}</span>
                          ) : (
                            <span className="text-green-600">Success</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CleanTestRunner; 