import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  PlayIcon, 
  DocumentTextIcon, 
  ChartBarIcon, 
  CogIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface TestGenerationConfig {
  stories_per_test: number;
  include_negative_tests: boolean;
  include_edge_cases: boolean;
  include_performance_tests: boolean;
  include_security_tests: boolean;
  complexity_distribution?: {
    low: number;
    medium: number;
    high: number;
  };
  priority_distribution?: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
}

interface TestCase {
  id: string;
  name: string;
  description: string;
  test_type: string;
  priority: string;
  story_id: string;
  prerequisites: string[];
  steps: string[];
  test_data: any;
  expected_results: string[];
  assertions: any[];
  tags: string[];
  estimated_duration: number;
  complexity: string;
  risk_level: string;
  created_at: string;
  metadata: any;
}

interface GenerationStats {
  total_tests_generated: number;
  total_stories_processed: number;
  average_tests_per_story: number;
  test_type_distribution: Record<string, number>;
  generation_history: any[];
}

const TestGenerator: React.FC = () => {
  const [config, setConfig] = useState<TestGenerationConfig>({
    stories_per_test: 3,
    include_negative_tests: true,
    include_edge_cases: true,
    include_performance_tests: false,
    include_security_tests: false
  });

  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [stats, setStats] = useState<GenerationStats | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeTab, setActiveTab] = useState<'config' | 'results' | 'stats'>('config');
  const [generationProgress, setGenerationProgress] = useState(0);

  const generateTestCases = async () => {
    setIsGenerating(true);
    setGenerationProgress(0);
    
    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setGenerationProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await fetch('/api/workflow/test-generation/generate-custom', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      });

      clearInterval(progressInterval);
      setGenerationProgress(100);

      if (response.ok) {
        const data = await response.json();
        setTestCases(data.test_cases);
        setStats(data.generation_stats);
        setActiveTab('results');
      } else {
        throw new Error('Failed to generate test cases');
      }
    } catch (error) {
      console.error('Error generating test cases:', error);
    } finally {
      setIsGenerating(false);
      setGenerationProgress(0);
    }
  };

  const getTestTypeColor = (type: string) => {
    switch (type) {
      case 'positive': return 'bg-green-100 text-green-800';
      case 'negative': return 'bg-red-100 text-red-800';
      case 'edge_case': return 'bg-yellow-100 text-yellow-800';
      case 'performance': return 'bg-blue-100 text-blue-800';
      case 'security': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🦖 Advanced Test Generator
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Test Case Generation with Intelligent Analysis
          </p>
        </motion.div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-lg p-1">
            <div className="flex space-x-1">
              {[
                { id: 'config', label: 'Configuration', icon: CogIcon },
                { id: 'results', label: 'Generated Tests', icon: DocumentTextIcon },
                { id: 'stats', label: 'Statistics', icon: ChartBarIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-indigo-500 text-white shadow-md'
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
          {activeTab === 'config' && (
            <div className="space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Test Generation Configuration
                </h2>
                
                {/* Basic Settings */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tests per Story
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="10"
                      value={config.stories_per_test}
                      onChange={(e) => setConfig(prev => ({
                        ...prev,
                        stories_per_test: parseInt(e.target.value)
                      }))}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                  </div>
                </div>

                {/* Test Types */}
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Types</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                      { key: 'include_negative_tests', label: 'Negative Tests', description: 'Test error conditions and invalid inputs' },
                      { key: 'include_edge_cases', label: 'Edge Cases', description: 'Test boundary conditions and extreme scenarios' },
                      { key: 'include_performance_tests', label: 'Performance Tests', description: 'Test system performance and load handling' },
                      { key: 'include_security_tests', label: 'Security Tests', description: 'Test security vulnerabilities and access controls' }
                    ].map((testType) => (
                      <div key={testType.key} className="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg">
                        <input
                          type="checkbox"
                          id={testType.key}
                          checked={config[testType.key as keyof TestGenerationConfig] as boolean}
                          onChange={(e) => setConfig(prev => ({
                            ...prev,
                            [testType.key]: e.target.checked
                          }))}
                          className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <div>
                          <label htmlFor={testType.key} className="text-sm font-medium text-gray-900">
                            {testType.label}
                          </label>
                          <p className="text-sm text-gray-500">{testType.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Generate Button */}
                <div className="text-center">
                  <button
                    onClick={generateTestCases}
                    disabled={isGenerating}
                    className="inline-flex items-center space-x-2 px-8 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-lg shadow-lg hover:from-indigo-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGenerating ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        <span>Generating...</span>
                      </>
                    ) : (
                      <>
                        <PlayIcon className="w-5 h-5" />
                        <span>Generate Test Cases</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Progress Bar */}
                {isGenerating && (
                  <div className="mt-6">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <motion.div
                        className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${generationProgress}%` }}
                        transition={{ duration: 0.3 }}
                      />
                    </div>
                    <p className="text-center text-sm text-gray-600 mt-2">
                      {generationProgress}% Complete
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'results' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Generated Test Cases
                </h2>
                <div className="text-sm text-gray-500">
                  {testCases.length} test cases generated
                </div>
              </div>

              <div className="space-y-6">
                {testCases.map((testCase, index) => (
                  <motion.div
                    key={testCase.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {testCase.name}
                        </h3>
                        <p className="text-gray-600">{testCase.description}</p>
                      </div>
                      <div className="flex space-x-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTestTypeColor(testCase.test_type)}`}>
                          {testCase.test_type}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(testCase.priority)}`}>
                          {testCase.priority}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getComplexityColor(testCase.complexity)}`}>
                          {testCase.complexity}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Prerequisites</h4>
                        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                          {testCase.prerequisites.map((prereq, i) => (
                            <li key={i}>{prereq}</li>
                          ))}
                        </ul>
                      </div>

                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Expected Results</h4>
                        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                          {testCase.expected_results.map((result, i) => (
                            <li key={i}>{result}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="mt-4">
                      <h4 className="font-medium text-gray-900 mb-2">Test Steps</h4>
                      <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
                        {testCase.steps.map((step, i) => (
                          <li key={i}>{step}</li>
                        ))}
                      </ol>
                    </div>

                    <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                      <span>Story ID: {testCase.story_id}</span>
                      <span>Duration: {testCase.estimated_duration}s</span>
                      <span>Risk: {testCase.risk_level}</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'stats' && stats && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Generation Statistics
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gradient-to-r from-green-400 to-green-600 text-white p-6 rounded-lg">
                  <div className="text-3xl font-bold">{stats.total_tests_generated}</div>
                  <div className="text-sm opacity-90">Total Tests Generated</div>
                </div>
                <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6 rounded-lg">
                  <div className="text-3xl font-bold">{stats.total_stories_processed}</div>
                  <div className="text-sm opacity-90">Stories Processed</div>
                </div>
                <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white p-6 rounded-lg">
                  <div className="text-3xl font-bold">{stats.average_tests_per_story.toFixed(1)}</div>
                  <div className="text-sm opacity-90">Avg Tests per Story</div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Type Distribution</h3>
                <div className="space-y-3">
                  {Object.entries(stats.test_type_distribution).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between">
                      <span className="capitalize text-gray-700">{type.replace('_', ' ')}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-indigo-500 h-2 rounded-full"
                            style={{ width: `${(count / stats.total_tests_generated) * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-900">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default TestGenerator; 