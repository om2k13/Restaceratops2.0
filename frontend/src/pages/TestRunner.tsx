import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { websocketService } from '../services/websocket';
import type { TestExecutionRequest, TestExecutionStatus } from '../services/api';
import type { TestCompleted } from '../services/websocket';

interface TestExecution {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  startTime: Date;
  endTime?: Date;
  duration?: number;
  results?: any[];
  error?: string;
  executionId?: string;
}

const TestRunner = () => {
  const [availableTests, setAvailableTests] = useState<any[]>([]);
  const [selectedTests, setSelectedTests] = useState<string[]>([]);
  const [executions, setExecutions] = useState<TestExecution[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  const [parallelExecution, setParallelExecution] = useState(false);

  useEffect(() => {
    const fetchAvailableTests = async () => {
      try {
        setLoading(true);
        const response = await apiService.getTestSpecifications();
        setAvailableTests(response.test_specifications || []);
        setError(null);
      } catch (err) {
        setError('Failed to load available tests');
        console.error('Load tests error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAvailableTests();
  }, []);

  useEffect(() => {
    // Set up WebSocket connection for real-time updates
    const connectWebSocket = async () => {
      try {
        await websocketService.connect();
        setConnectionStatus('connected');
        
        // Subscribe to test completion messages
        const unsubscribeTestCompleted = websocketService.subscribeToTestCompleted((message: TestCompleted) => {
          const testData = message.data;
          setExecutions(prev => prev.map(exec => {
            if (exec.executionId === testData.execution_id) {
              return {
                ...exec,
                status: 'completed',
                endTime: new Date(),
                duration: new Date().getTime() - exec.startTime.getTime(),
                results: testData.results,
                progress: 100
              };
            }
            return exec;
          }));
          
          setIsRunning(false);
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
          unsubscribeTestCompleted();
          unsubscribePong();
          clearInterval(statusInterval);
          websocketService.disconnect();
        };
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        setConnectionStatus('disconnected');
        return () => {};
      }
    };

    const cleanup = connectWebSocket();

    return () => {
      cleanup.then(cleanupFn => cleanupFn && cleanupFn());
    };
  }, []);

  const toggleTestSelection = (testName: string) => {
    setSelectedTests(prev => 
      prev.includes(testName) 
        ? prev.filter(name => name !== testName)
        : [...prev, testName]
    );
  };

  const runSelectedTests = async () => {
    if (selectedTests.length === 0) {
      setError('Please select at least one test to run');
      return;
    }

    setIsRunning(true);
    setError(null);

    try {
      // Create execution request
      const request: TestExecutionRequest = {
        test_files: selectedTests,
        parallel: parallelExecution,
        timeout: 30000
      };

      // Start test execution
      const response = await apiService.runTests(request);
      
      // Create execution entries for selected tests
      const newExecutions: TestExecution[] = selectedTests.map(testName => ({
        id: Date.now().toString() + Math.random(),
        name: testName,
        status: 'pending',
        progress: 0,
        startTime: new Date(),
        executionId: response.execution_id
      }));

      setExecutions(prev => [...prev, ...newExecutions]);

      // Start polling for execution status updates
      const stopPolling = await apiService.pollExecutionStatus(
        response.execution_id,
        (status: TestExecutionStatus) => {
          setExecutions(prev => prev.map(exec => {
            if (exec.executionId === status.execution_id) {
              return {
                ...exec,
                status: status.status,
                progress: status.progress,
                endTime: status.end_time ? new Date(status.end_time) : undefined,
                duration: status.end_time ? new Date(status.end_time).getTime() - exec.startTime.getTime() : undefined,
                results: status.results,
                error: status.error
              };
            }
            return exec;
          }));

          // Check if all executions are complete
          const allComplete = status.status === 'completed' || status.status === 'failed';
          if (allComplete) {
            setIsRunning(false);
            stopPolling();
          }
        },
        1000 // Poll every second
      );

      setSelectedTests([]);
    } catch (err) {
      setError('Failed to run tests. Please try again.');
      console.error('Run tests error:', err);
      setIsRunning(false);
    }
  };

  const clearExecutions = () => {
    setExecutions([]);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-gray-500';
      case 'running': return 'bg-blue-500';
      case 'completed': return 'bg-success-500';
      case 'failed': return 'bg-error-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending': return 'Pending';
      case 'running': return 'Running';
      case 'completed': return 'Completed';
      case 'failed': return 'Failed';
      default: return 'Unknown';
    }
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Test Runner</h1>
          <p className="text-sm text-gray-600 mt-1">
            Execute and monitor API tests in real-time
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${getConnectionStatusColor()} animate-pulse`}></div>
            <span className="text-sm text-gray-600">{getConnectionStatusText()}</span>
          </div>
          <button
            onClick={clearExecutions}
            className="btn-secondary text-sm"
          >
            Clear History
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-800 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Test Selection */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Tests</h3>
          
          {availableTests.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-sm">No test files found</p>
              <p className="text-xs">Create tests in the Test Builder first</p>
            </div>
          ) : (
            <div className="space-y-2">
              {availableTests.map((test) => (
                <div
                  key={test.name}
                  className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                    selectedTests.includes(test.name)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => toggleTestSelection(test.name)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        checked={selectedTests.includes(test.name)}
                        onChange={() => toggleTestSelection(test.name)}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {test.name}
                        </div>
                        <div className="text-xs text-gray-500">
                          {test.path}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={parallelExecution}
                onChange={(e) => setParallelExecution(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="ml-2 text-sm text-gray-700">Run tests in parallel</span>
            </div>
            
            <button
              onClick={runSelectedTests}
              disabled={isRunning || selectedTests.length === 0}
              className="w-full btn-primary"
            >
              {isRunning ? 'Running Tests...' : `Run ${selectedTests.length} Selected Test${selectedTests.length !== 1 ? 's' : ''}`}
            </button>
          </div>
        </div>

        {/* Execution History */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Execution History</h3>
          
          {executions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <p className="text-sm">No test executions yet</p>
              <p className="text-xs">Select and run tests to see execution history</p>
            </div>
          ) : (
            <div className="space-y-3">
              {executions.map((execution) => (
                <div key={execution.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center space-x-2">
                      <div className={`w-2 h-2 rounded-full ${getStatusColor(execution.status)}`}></div>
                      <span className="text-sm font-medium text-gray-900">
                        {execution.name}
                      </span>
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${getStatusColor(execution.status)} text-white`}>
                        {getStatusText(execution.status)}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {execution.startTime.toLocaleTimeString()}
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${
                        execution.status === 'completed' ? 'bg-success-500' :
                        execution.status === 'failed' ? 'bg-error-500' :
                        execution.status === 'running' ? 'bg-blue-500' : 'bg-gray-500'
                      }`}
                      style={{ width: `${execution.progress}%` }}
                    ></div>
                  </div>

                  {/* Execution Details */}
                  <div className="text-xs text-gray-600 space-y-1">
                    <div>Progress: {execution.progress}%</div>
                    {execution.duration && (
                      <div>Duration: {execution.duration}ms</div>
                    )}
                    {execution.results && execution.results.length > 0 && (
                      <div className="mt-2 p-2 bg-gray-50 rounded">
                        <div className="font-medium mb-1">Results:</div>
                        {execution.results.map((result, index) => (
                          <div key={index} className="text-xs">
                            • {result.test_name || result.name || 'Unknown'}: {result.status} 
                            {result.response_time && ` (${result.response_time}ms)`}
                          </div>
                        ))}
                      </div>
                    )}
                    {execution.error && (
                      <div className="text-error-600 mt-2">
                        Error: {execution.error}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TestRunner; 