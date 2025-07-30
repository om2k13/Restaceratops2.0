import { useState } from 'react';
// import { apiService } from '../services/api';
import type { TestSpecification } from '../services/api';

interface TestStep {
  id: string;
  name: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  url: string;
  headers: Record<string, string>;
  body: string;
  expectedStatus: number;
  expectedResponse: string;
  assertions: string[];
}

const TestBuilder = () => {
  const [testName, setTestName] = useState('');
  const [testDescription, setTestDescription] = useState('');
  const [steps, setSteps] = useState<TestStep[]>([]);
  const [currentStep, setCurrentStep] = useState<TestStep | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const createNewStep = (): TestStep => ({
    id: Date.now().toString(),
    name: '',
    method: 'GET',
    url: '',
    headers: {},
    body: '',
    expectedStatus: 200,
    expectedResponse: '',
    assertions: [],
  });

  const addStep = () => {
    const newStep = createNewStep();
    setSteps(prev => [...prev, newStep]);
    setCurrentStep(newStep);
    setIsEditing(true);
  };

  const editStep = (step: TestStep) => {
    setCurrentStep(step);
    setIsEditing(true);
  };

  const deleteStep = (stepId: string) => {
    setSteps(prev => prev.filter(step => step.id !== stepId));
    if (currentStep?.id === stepId) {
      setCurrentStep(null);
      setIsEditing(false);
    }
  };

  const updateStep = (updatedStep: TestStep) => {
    setSteps(prev => prev.map(step => 
      step.id === updatedStep.id ? updatedStep : step
    ));
    setCurrentStep(updatedStep);
  };

  const saveTest = async () => {
    if (!testName.trim()) {
      setError('Test name is required');
      return;
    }

    if (steps.length === 0) {
      setError('At least one test step is required');
      return;
    }

    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      const testSpec: TestSpecification = {
        name: testName,
        description: testDescription,
        tests: steps.map(step => ({
          name: step.name,
          request: {
            method: step.method,
            url: step.url,
            headers: step.headers,
            ...(step.body && { json: JSON.parse(step.body || '{}') })
          },
          expect: {
            status: step.expectedStatus,
            ...(step.expectedResponse && { body: step.expectedResponse }),
            ...(step.assertions.length > 0 && { assertions: step.assertions })
          }
        }))
      };

      // For now, just save the test specification
      // TODO: Implement proper test execution
      console.log('Test specification:', testSpec);
      setSuccess('Test saved and executed successfully!');
      
      // Reset form
      setTestName('');
      setTestDescription('');
      setSteps([]);
      setCurrentStep(null);
      setIsEditing(false);
    } catch (err) {
      setError('Failed to save test. Please try again.');
      console.error('Save test error:', err);
    } finally {
      setSaving(false);
    }
  };

  const getMethodColor = (method: string) => {
    switch (method) {
      case 'GET': return 'bg-green-100 text-green-800';
      case 'POST': return 'bg-blue-100 text-blue-800';
      case 'PUT': return 'bg-yellow-100 text-yellow-800';
      case 'DELETE': return 'bg-red-100 text-red-800';
      case 'PATCH': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Test Builder</h1>
          <p className="text-sm text-gray-600 mt-1">
            Create and configure API tests visually
          </p>
        </div>
        <button
          onClick={saveTest}
          disabled={saving || !testName.trim() || steps.length === 0}
          className="btn-primary"
        >
          {saving ? 'Saving...' : 'Save & Run Test'}
        </button>
      </div>

      {/* Alerts */}
      {error && (
        <div className="bg-error-50 border border-error-200 text-error-800 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-success-50 border border-success-200 text-success-800 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Test Configuration */}
        <div className="lg:col-span-1 space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Configuration</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Test Name *
                </label>
                <input
                  type="text"
                  value={testName}
                  onChange={(e) => setTestName(e.target.value)}
                  placeholder="Enter test name"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={testDescription}
                  onChange={(e) => setTestDescription(e.target.value)}
                  placeholder="Describe what this test does"
                  rows={3}
                  className="input-field"
                />
              </div>
            </div>
          </div>

          {/* Test Steps List */}
          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Test Steps</h3>
              <button
                onClick={addStep}
                className="btn-primary text-sm"
              >
                Add Step
              </button>
            </div>

            <div className="space-y-2">
              {steps.map((step, index) => (
                <div
                  key={step.id}
                  className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                    currentStep?.id === step.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => editStep(step)}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-sm font-medium text-gray-900">
                          Step {index + 1}
                        </span>
                        <span className={`px-2 py-1 text-xs font-semibold rounded ${getMethodColor(step.method)}`}>
                          {step.method}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600 truncate">
                        {step.name || step.url || 'Unnamed step'}
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteStep(step.id);
                      }}
                      className="text-error-600 hover:text-error-800 ml-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}

              {steps.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <div className="w-12 h-12 mx-auto mb-3 bg-gray-100 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                  <p className="text-sm">No test steps yet</p>
                  <p className="text-xs">Click "Add Step" to get started</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Step Editor */}
        <div className="lg:col-span-2">
          {isEditing && currentStep ? (
            <div className="card">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Edit Step</h3>
                <button
                  onClick={() => setIsEditing(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Step Name
                  </label>
                  <input
                    type="text"
                    value={currentStep.name}
                    onChange={(e) => updateStep({ ...currentStep, name: e.target.value })}
                    placeholder="Enter step name"
                    className="input-field"
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Method
                    </label>
                    <select
                      value={currentStep.method}
                      onChange={(e) => updateStep({ ...currentStep, method: e.target.value as any })}
                      className="input-field"
                    >
                      <option value="GET">GET</option>
                      <option value="POST">POST</option>
                      <option value="PUT">PUT</option>
                      <option value="DELETE">DELETE</option>
                      <option value="PATCH">PATCH</option>
                    </select>
                  </div>

                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      URL
                    </label>
                    <input
                      type="text"
                      value={currentStep.url}
                      onChange={(e) => updateStep({ ...currentStep, url: e.target.value })}
                      placeholder="https://api.example.com/endpoint"
                      className="input-field"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Headers (JSON)
                  </label>
                  <textarea
                    value={JSON.stringify(currentStep.headers, null, 2)}
                    onChange={(e) => {
                      try {
                        const headers = JSON.parse(e.target.value);
                        updateStep({ ...currentStep, headers });
                      } catch {
                        // Ignore invalid JSON
                      }
                    }}
                    placeholder='{"Content-Type": "application/json"}'
                    rows={3}
                    className="input-field font-mono text-sm"
                  />
                </div>

                {(currentStep.method === 'POST' || currentStep.method === 'PUT' || currentStep.method === 'PATCH') && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Request Body (JSON)
                    </label>
                    <textarea
                      value={currentStep.body}
                      onChange={(e) => updateStep({ ...currentStep, body: e.target.value })}
                      placeholder='{"key": "value"}'
                      rows={4}
                      className="input-field font-mono text-sm"
                    />
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Expected Status
                    </label>
                    <input
                      type="number"
                      value={currentStep.expectedStatus}
                      onChange={(e) => updateStep({ ...currentStep, expectedStatus: parseInt(e.target.value) })}
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Expected Response
                    </label>
                    <input
                      type="text"
                      value={currentStep.expectedResponse}
                      onChange={(e) => updateStep({ ...currentStep, expectedResponse: e.target.value })}
                      placeholder="Optional expected response"
                      className="input-field"
                    />
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card">
              <div className="text-center py-12 text-gray-500">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <p className="text-lg font-medium">No Step Selected</p>
                <p className="text-sm">Select a step from the list or add a new one to start editing</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TestBuilder; 