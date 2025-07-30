import React, { useState, useEffect } from 'react';
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  ArrowRightIcon,
  ArrowLeftIcon,
  PlayIcon,
  PauseIcon,
  DocumentTextIcon,
  CogIcon,
  ChartBarIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';

interface WorkflowStep {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'active' | 'completed' | 'error';
  icon: React.ComponentType<any>;
}

interface WorkflowData {
  applicationUrl: string;
  jiraConfig: {
    baseUrl: string;
    username: string;
    apiToken: string;
    projectKey: string;
  };
  selectedStories: string[];
  validationResults: any;
  testCases: any[];
  testData: any;
  executionResults: any;
  evaluationResults: any;
}

const WorkflowInterface: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [workflowData, setWorkflowData] = useState<WorkflowData>({
    applicationUrl: '',
    jiraConfig: {
      baseUrl: '',
      username: '',
      apiToken: '',
      projectKey: ''
    },
    selectedStories: [],
    validationResults: null,
    testCases: [],
    testData: null,
    executionResults: null,
    evaluationResults: null
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const workflowSteps: WorkflowStep[] = [
    {
      id: 'connectivity',
      title: 'Connectivity',
      description: 'Connect to your application and Jira project',
      status: 'active',
      icon: CogIcon
    },
    {
      id: 'user-story-selection',
      title: 'User Story Selection',
      description: 'Select user stories for test case generation',
      status: 'pending',
      icon: DocumentTextIcon
    },
    {
      id: 'review-validate',
      title: 'Review & Validate',
      description: 'Review and validate selected user stories',
      status: 'pending',
      icon: CheckIcon
    },
    {
      id: 'generate-test-cases',
      title: 'Generate Test Cases',
      description: 'Generate test cases from validated user stories',
      status: 'pending',
      icon: DocumentTextIcon
    },
    {
      id: 'generate-test-data',
      title: 'Generate Test Data',
      description: 'Generate test data for the test cases',
      status: 'pending',
      icon: ChartBarIcon
    },
    {
      id: 'execute-test',
      title: 'Execute Test',
      description: 'Execute the generated test cases',
      status: 'pending',
      icon: PlayIcon
    },
    {
      id: 'evaluate-test-results',
      title: 'Evaluate Test Results',
      description: 'Evaluate and analyze test execution results',
      status: 'pending',
      icon: ChartBarIcon
    }
  ];

  const updateStepStatus = (stepIndex: number, status: WorkflowStep['status']) => {
    const updatedSteps = [...workflowSteps];
    updatedSteps[stepIndex].status = status;
    // In a real implementation, you'd update the state properly
  };

  const handleNext = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Validate current step data
      const isValid = await validateCurrentStep();
      if (!isValid) {
        throw new Error('Current step validation failed');
      }

      // Execute current step
      await executeCurrentStep();

      // Move to next step
      if (currentStep < workflowSteps.length - 1) {
        updateStepStatus(currentStep, 'completed');
        setCurrentStep(currentStep + 1);
        updateStepStatus(currentStep + 1, 'active');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      updateStepStatus(currentStep, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      updateStepStatus(currentStep, 'pending');
      setCurrentStep(currentStep - 1);
      updateStepStatus(currentStep - 1, 'active');
    }
  };

  const validateCurrentStep = async (): Promise<boolean> => {
    // Implement validation logic for current step
    return true;
  };

  const executeCurrentStep = async () => {
    // Implement step execution logic
    await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API call
  };

  const getStepContent = () => {
    switch (currentStep) {
      case 0:
        return <ConnectivityStep data={workflowData} setData={setWorkflowData} />;
      case 1:
        return <UserStorySelectionStep data={workflowData} setData={setWorkflowData} />;
      case 2:
        return <ReviewValidateStep data={workflowData} setData={setWorkflowData} />;
      case 3:
        return <GenerateTestCasesStep data={workflowData} setData={setWorkflowData} />;
      case 4:
        return <GenerateTestDataStep data={workflowData} setData={setWorkflowData} />;
      case 5:
        return <ExecuteTestStep data={workflowData} setData={setWorkflowData} />;
      case 6:
        return <EvaluateTestResultsStep data={workflowData} setData={setWorkflowData} />;
      default:
        return <div>Unknown step</div>;
    }
  };

  const getProgressPercentage = () => {
    return ((currentStep + 1) / workflowSteps.length) * 100;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🦖</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Restaceratops</h1>
                <p className="text-sm text-gray-500">AI-Powered Test Case Generation</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">Progress</p>
                <p className="text-sm text-gray-500">{Math.round(getProgressPercentage())}% Complete</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Workflow Steps */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Workflow Steps</h2>
              <div className="space-y-4">
                {workflowSteps.map((step, index) => (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`relative p-4 rounded-lg border-2 transition-all duration-200 ${
                      step.status === 'active'
                        ? 'border-blue-500 bg-blue-50'
                        : step.status === 'completed'
                        ? 'border-green-500 bg-green-50'
                        : step.status === 'error'
                        ? 'border-red-500 bg-red-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        step.status === 'active'
                          ? 'bg-blue-500 text-white'
                          : step.status === 'completed'
                          ? 'bg-green-500 text-white'
                          : step.status === 'error'
                          ? 'bg-red-500 text-white'
                          : 'bg-gray-300 text-gray-600'
                      }`}>
                        {step.status === 'completed' ? (
                          <CheckIcon className="w-5 h-5" />
                        ) : step.status === 'error' ? (
                          <XMarkIcon className="w-5 h-5" />
                        ) : (
                          <step.icon className="w-5 h-5" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className={`text-sm font-medium ${
                          step.status === 'active' ? 'text-blue-900' : 'text-gray-900'
                        }`}>
                          {step.title}
                        </h3>
                        <p className="text-xs text-gray-500 mt-1">{step.description}</p>
                      </div>
                    </div>
                    {index < workflowSteps.length - 1 && (
                      <div className={`absolute left-4 top-12 w-0.5 h-8 ${
                        step.status === 'completed' ? 'bg-green-500' : 'bg-gray-200'
                      }`} />
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200">
              {/* Progress Bar */}
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    {workflowSteps[currentStep].title}
                  </h2>
                  <div className="text-sm text-gray-500">
                    Step {currentStep + 1} of {workflowSteps.length}
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${getProgressPercentage()}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>

              {/* Step Content */}
              <div className="p-6">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentStep}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    {getStepContent()}
                  </motion.div>
                </AnimatePresence>

                {/* Error Display */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
                  >
                    <div className="flex items-center space-x-2">
                      <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />
                      <p className="text-sm text-red-700">{error}</p>
                    </div>
                  </motion.div>
                )}

                {/* Navigation Buttons */}
                <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
                  <button
                    onClick={handlePrevious}
                    disabled={currentStep === 0 || isLoading}
                    className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <ArrowLeftIcon className="w-4 h-4" />
                    <span>Previous</span>
                  </button>

                  <div className="flex items-center space-x-3">
                    {isLoading && (
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                        <span>Processing...</span>
                      </div>
                    )}
                  </div>

                  <button
                    onClick={handleNext}
                    disabled={isLoading}
                    className="flex items-center space-x-2 px-6 py-2 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm"
                  >
                    <span>{currentStep === workflowSteps.length - 1 ? 'Complete' : 'Next'}</span>
                    {currentStep < workflowSteps.length - 1 && <ArrowRightIcon className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Step Components
const ConnectivityStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Application Configuration</h3>
      <p className="text-sm text-gray-600 mb-4">
        Connect to your application and configure Jira integration for seamless test case generation.
      </p>
    </div>

    <div className="grid grid-cols-1 gap-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Application URL
        </label>
        <input
          type="url"
          value={data.applicationUrl}
          onChange={(e) => setData({ ...data, applicationUrl: e.target.value })}
          placeholder="https://your-application.com"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
        />
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Jira Configuration</h4>
        <div className="grid grid-cols-1 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
            <input
              type="url"
              value={data.jiraConfig.baseUrl}
              onChange={(e) => setData({
                ...data,
                jiraConfig: { ...data.jiraConfig, baseUrl: e.target.value }
              })}
              placeholder="https://your-company.atlassian.net"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                value={data.jiraConfig.username}
                onChange={(e) => setData({
                  ...data,
                  jiraConfig: { ...data.jiraConfig, username: e.target.value }
                })}
                placeholder="your-email@company.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Project Key</label>
              <input
                type="text"
                value={data.jiraConfig.projectKey}
                onChange={(e) => setData({
                  ...data,
                  jiraConfig: { ...data.jiraConfig, projectKey: e.target.value }
                })}
                placeholder="PROJ"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">API Token</label>
            <input
              type="password"
              value={data.jiraConfig.apiToken}
              onChange={(e) => setData({
                ...data,
                jiraConfig: { ...data.jiraConfig, apiToken: e.target.value }
              })}
              placeholder="Enter your Jira API token"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
);

const UserStorySelectionStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Select User Stories</h3>
      <p className="text-sm text-gray-600 mb-4">
        Choose the user stories you want to generate test cases for.
      </p>
    </div>

    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-medium text-gray-900">Available Stories</h4>
        <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
          Refresh Stories
        </button>
      </div>
      
      <div className="space-y-3">
        {[
          { id: 'AT-21', summary: 'As a user, I want to know about the potential impacts of climate change on human health and food supplies, so I can understand direct societal consequences.' },
          { id: 'AT-22', summary: 'As a user, I want an analysis of the geopolitical implications of shifting agricultural zones due to climate change, so I can understand potential conflicts over newly arable land and disruptions in international food trade.' }
        ].map((story) => (
          <div key={story.id} className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-gray-200">
            <input
              type="checkbox"
              checked={data.selectedStories.includes(story.id)}
              onChange={(e) => {
                if (e.target.checked) {
                  setData({
                    ...data,
                    selectedStories: [...data.selectedStories, story.id]
                  });
                } else {
                  setData({
                    ...data,
                    selectedStories: data.selectedStories.filter(id => id !== story.id)
                  });
                }
              }}
              className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <div className="flex-1">
              <h5 className="text-sm font-medium text-gray-900">{story.id}</h5>
              <p className="text-sm text-gray-600 mt-1">{story.summary}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

const ReviewValidateStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Review & Validate Stories</h3>
      <p className="text-sm text-gray-600 mb-4">
        Review the selected user stories and their validation results.
      </p>
    </div>

    <div className="space-y-4">
      {data.selectedStories.map((storyId) => (
        <div key={storyId} className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-medium text-gray-900">{storyId}</h4>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Validated
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-3">
            Story summary and acceptance criteria details...
          </p>
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <span>Score: 85%</span>
            <span>Issues: 0</span>
            <span>Suggestions: 2</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const GenerateTestCasesStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Generate Test Cases</h3>
      <p className="text-sm text-gray-600 mb-4">
        AI will generate comprehensive test cases from your validated user stories.
      </p>
    </div>

    <div className="bg-blue-50 rounded-lg p-4">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
          <DocumentTextIcon className="w-5 h-5 text-white" />
        </div>
        <div>
          <h4 className="text-sm font-medium text-blue-900">Test Case Generation</h4>
          <p className="text-sm text-blue-700">
            Generating test cases for {data.selectedStories.length} user stories...
          </p>
        </div>
      </div>
    </div>

    <div className="grid grid-cols-1 gap-4">
      <div className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg">
        <div>
          <h5 className="text-sm font-medium text-gray-900">Test Cases per Story</h5>
          <p className="text-sm text-gray-600">Number of test cases to generate for each user story</p>
        </div>
        <div className="flex items-center space-x-2">
          <button className="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50">
            -
          </button>
          <span className="w-12 text-center text-sm font-medium">3</span>
          <button className="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50">
            +
          </button>
        </div>
      </div>
    </div>
  </div>
);

const GenerateTestDataStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Generate Test Data</h3>
      <p className="text-sm text-gray-600 mb-4">
        Generate test data for your test cases to ensure comprehensive coverage.
      </p>
    </div>

    <div className="bg-green-50 rounded-lg p-4">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
          <ChartBarIcon className="w-5 h-5 text-white" />
        </div>
        <div>
          <h4 className="text-sm font-medium text-green-900">Test Data Generation</h4>
          <p className="text-sm text-green-700">
            Generating test data for {data.testCases.length} test cases...
          </p>
        </div>
      </div>
    </div>
  </div>
);

const ExecuteTestStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Execute Tests</h3>
      <p className="text-sm text-gray-600 mb-4">
        Execute the generated test cases against your application.
      </p>
    </div>

    <div className="bg-purple-50 rounded-lg p-4">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
          <PlayIcon className="w-5 h-5 text-white" />
        </div>
        <div>
          <h4 className="text-sm font-medium text-purple-900">Test Execution</h4>
          <p className="text-sm text-purple-700">
            Executing {data.testCases.length} test cases...
          </p>
        </div>
      </div>
    </div>
  </div>
);

const EvaluateTestResultsStep: React.FC<{ data: WorkflowData; setData: (data: WorkflowData) => void }> = ({ data, setData }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Evaluate Test Results</h3>
      <p className="text-sm text-gray-600 mb-4">
        Analyze and evaluate the test execution results.
      </p>
    </div>

    <div className="bg-orange-50 rounded-lg p-4">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
          <ChartBarIcon className="w-5 h-5 text-white" />
        </div>
        <div>
          <h4 className="text-sm font-medium text-orange-900">Result Evaluation</h4>
          <p className="text-sm text-orange-700">
            Evaluating test execution results...
          </p>
        </div>
      </div>
    </div>
  </div>
);

export default WorkflowInterface; 