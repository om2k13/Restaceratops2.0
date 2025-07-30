import { useState, useEffect } from 'react';
// import { apiService } from '../services/api';

interface Settings {
  general: {
    theme: 'light' | 'dark' | 'auto';
    language: string;
    timezone: string;
    notifications: boolean;
  };
  ai: {
    model: string;
    temperature: number;
    maxTokens: number;
    enableRAG: boolean;
    enableVectorDB: boolean;
  };
  testing: {
    defaultTimeout: number;
    retryAttempts: number;
    parallelExecution: boolean;
    saveResults: boolean;
    autoExport: boolean;
  };
  api: {
    baseUrl: string;
    apiKey: string;
    enableWebSocket: boolean;
    connectionTimeout: number;
  };
}

const Settings = () => {
  const [settings, setSettings] = useState<Settings>({
    general: {
      theme: 'light',
      language: 'en',
      timezone: 'UTC',
      notifications: true,
    },
    ai: {
      model: 'gpt-4o-mini',
      temperature: 0.7,
      maxTokens: 1000,
      enableRAG: true,
      enableVectorDB: true,
    },
    testing: {
      defaultTimeout: 30000,
      retryAttempts: 3,
      parallelExecution: true,
      saveResults: true,
      autoExport: false,
    },
    api: {
      baseUrl: 'http://localhost:8000',
      apiKey: '',
      enableWebSocket: true,
      connectionTimeout: 5000,
    },
  });

  const [activeTab, setActiveTab] = useState<'general' | 'ai' | 'testing' | 'api'>('general');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Load settings from localStorage or API
    const loadSettings = () => {
      const savedSettings = localStorage.getItem('restaceratops-settings');
      if (savedSettings) {
        try {
          const parsed = JSON.parse(savedSettings);
          setSettings(prev => ({ ...prev, ...parsed }));
        } catch (error) {
          console.error('Failed to load settings:', error);
        }
      }
    };

    loadSettings();
  }, []);

  const saveSettings = async () => {
    setSaving(true);
    setSaved(false);

    try {
      // Save to localStorage
      localStorage.setItem('restaceratops-settings', JSON.stringify(settings));
      
      // In a real implementation, you would also save to the backend
      // await apiService.updateSettings(settings);
      
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      
      // Apply theme immediately if changed
      if (settings.general.theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setSaving(false);
    }
  };

  const updateSetting = (section: keyof Settings, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value,
      },
    }));
  };

  const resetSettings = () => {
    if (confirm('Are you sure you want to reset all settings to default values?')) {
      setSettings({
        general: {
          theme: 'light',
          language: 'en',
          timezone: 'UTC',
          notifications: true,
        },
        ai: {
          model: 'gpt-4o-mini',
          temperature: 0.7,
          maxTokens: 1000,
          enableRAG: true,
          enableVectorDB: true,
        },
        testing: {
          defaultTimeout: 30000,
          retryAttempts: 3,
          parallelExecution: true,
          saveResults: true,
          autoExport: false,
        },
        api: {
          baseUrl: 'http://localhost:8000',
          apiKey: '',
          enableWebSocket: true,
          connectionTimeout: 5000,
        },
      });
    }
  };

  const tabs = [
    { id: 'general', name: 'General', icon: '⚙️' },
    { id: 'ai', name: 'AI Settings', icon: '🤖' },
    { id: 'testing', name: 'Testing', icon: '🧪' },
    { id: 'api', name: 'API Configuration', icon: '🔗' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-sm text-gray-600 mt-1">
            Configure your Restaceratops experience
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={resetSettings}
            className="btn-secondary"
          >
            Reset to Default
          </button>
          <button
            onClick={saveSettings}
            disabled={saving}
            className="btn-primary"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>

      {saved && (
        <div className="bg-success-50 border border-success-200 text-success-800 px-4 py-3 rounded-lg">
          Settings saved successfully!
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Settings Content */}
      <div className="card">
        {activeTab === 'general' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">General Settings</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Theme
                </label>
                <select
                  value={settings.general.theme}
                  onChange={(e) => updateSetting('general', 'theme', e.target.value)}
                  className="input-field"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="auto">Auto (System)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Language
                </label>
                <select
                  value={settings.general.language}
                  onChange={(e) => updateSetting('general', 'language', e.target.value)}
                  className="input-field"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="ja">Japanese</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Timezone
                </label>
                <select
                  value={settings.general.timezone}
                  onChange={(e) => updateSetting('general', 'timezone', e.target.value)}
                  className="input-field"
                >
                  <option value="UTC">UTC</option>
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                  <option value="Europe/London">London</option>
                  <option value="Europe/Paris">Paris</option>
                  <option value="Asia/Tokyo">Tokyo</option>
                </select>
              </div>

              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.general.notifications}
                    onChange={(e) => updateSetting('general', 'notifications', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Enable Notifications</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">AI Settings</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  AI Model
                </label>
                <select
                  value={settings.ai.model}
                  onChange={(e) => updateSetting('ai', 'model', e.target.value)}
                  className="input-field"
                >
                  <option value="gpt-4o-mini">GPT-4o Mini (Fast)</option>
                  <option value="gpt-4o">GPT-4o (Advanced)</option>
                  <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Legacy)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Temperature: {settings.ai.temperature}
                </label>
                <input
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  value={settings.ai.temperature}
                  onChange={(e) => updateSetting('ai', 'temperature', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Focused (0)</span>
                  <span>Balanced (1)</span>
                  <span>Creative (2)</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Tokens
                </label>
                <input
                  type="number"
                  value={settings.ai.maxTokens}
                  onChange={(e) => updateSetting('ai', 'maxTokens', parseInt(e.target.value))}
                  min="100"
                  max="4000"
                  className="input-field"
                />
              </div>

              <div className="space-y-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.ai.enableRAG}
                    onChange={(e) => updateSetting('ai', 'enableRAG', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Enable RAG (Retrieval Augmented Generation)</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.ai.enableVectorDB}
                    onChange={(e) => updateSetting('ai', 'enableVectorDB', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Enable Vector Database</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'testing' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">Testing Configuration</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Timeout (ms)
                </label>
                <input
                  type="number"
                  value={settings.testing.defaultTimeout}
                  onChange={(e) => updateSetting('testing', 'defaultTimeout', parseInt(e.target.value))}
                  min="1000"
                  max="300000"
                  step="1000"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Retry Attempts
                </label>
                <input
                  type="number"
                  value={settings.testing.retryAttempts}
                  onChange={(e) => updateSetting('testing', 'retryAttempts', parseInt(e.target.value))}
                  min="0"
                  max="10"
                  className="input-field"
                />
              </div>

              <div className="space-y-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.testing.parallelExecution}
                    onChange={(e) => updateSetting('testing', 'parallelExecution', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Enable Parallel Test Execution</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.testing.saveResults}
                    onChange={(e) => updateSetting('testing', 'saveResults', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Save Test Results</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.testing.autoExport}
                    onChange={(e) => updateSetting('testing', 'autoExport', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Auto-export Results</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'api' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">API Configuration</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Backend API URL
                </label>
                <input
                  type="url"
                  value={settings.api.baseUrl}
                  onChange={(e) => updateSetting('api', 'baseUrl', e.target.value)}
                  placeholder="http://localhost:8000"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Key (Optional)
                </label>
                <input
                  type="password"
                  value={settings.api.apiKey}
                  onChange={(e) => updateSetting('api', 'apiKey', e.target.value)}
                  placeholder="Enter your API key"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Connection Timeout (ms)
                </label>
                <input
                  type="number"
                  value={settings.api.connectionTimeout}
                  onChange={(e) => updateSetting('api', 'connectionTimeout', parseInt(e.target.value))}
                  min="1000"
                  max="30000"
                  step="1000"
                  className="input-field"
                />
              </div>

              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.api.enableWebSocket}
                    onChange={(e) => updateSetting('api', 'enableWebSocket', e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Enable WebSocket (Real-time)</span>
                </label>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="text-sm font-medium text-blue-900 mb-2">Connection Status</h4>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-blue-700">Connected to backend at {settings.api.baseUrl}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings; 