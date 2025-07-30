import React, { useState, useEffect } from 'react';
import { 
  FaServer, FaCodeBranch, FaShieldAlt, FaChartLine, 
  FaCog, FaPlus, FaPlay, FaEye, FaEdit, FaTrash,
  FaGithub, FaGitlab, FaJenkins, FaMicrosoft, FaCircle, FaCode,
  FaDesktop, FaMobile, FaGlobe, FaCloud, FaMicrochip,
  FaBell, FaEnvelope, FaSlack, FaWebhook, FaCheckCircle,
  FaExclamationTriangle, FaTimesCircle, FaInfoCircle
} from 'react-icons/fa';

interface PlatformConfig {
  name: string;
  type: string;
  base_url: string;
  timeout: number;
  retry_attempts: number;
}

interface CICDConfig {
  name: string;
  type: string;
  project_id: string;
  branch: string;
  trigger_on_push: boolean;
  trigger_on_pr: boolean;
}

interface MonitoringConfig {
  name: string;
  enabled: boolean;
  health_check_interval: number;
  notification_channels: string[];
  performance_thresholds: Record<string, number>;
}

interface SecurityConfig {
  name: string;
  rbac_enabled: boolean;
  audit_logging: boolean;
  encryption_enabled: boolean;
  session_timeout: number;
  compliance_standards: string[];
}

interface AuditLog {
  timestamp: string;
  user_id: string;
  action: string;
  resource: string;
  details: any;
  ip_address?: string;
  user_agent?: string;
  success: boolean;
}

interface SystemStatus {
  platforms: { count: number; names: string[] };
  cicd: { count: number; names: string[] };
  monitoring: { count: number; enabled: number };
  security: { count: number; audit_logs: number; active_sessions: number };
  performance: { metrics_count: number };
}

const EnterpriseDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [platforms, setPlatforms] = useState<PlatformConfig[]>([]);
  const [cicdConfigs, setCicdConfigs] = useState<CICDConfig[]>([]);
  const [monitoringConfigs, setMonitoringConfigs] = useState<MonitoringConfig[]>([]);
  const [securityConfigs, setSecurityConfigs] = useState<SecurityConfig[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [sessionToken, setSessionToken] = useState('');

  // Mock data for demonstration
  const mockPlatforms: PlatformConfig[] = [
    { name: 'Web App', type: 'web', base_url: 'https://app.example.com', timeout: 30, retry_attempts: 3 },
    { name: 'API Service', type: 'api', base_url: 'https://api.example.com', timeout: 30, retry_attempts: 3 },
    { name: 'Mobile App', type: 'mobile', base_url: 'https://mobile.example.com', timeout: 30, retry_attempts: 3 }
  ];

  const mockCICDConfigs: CICDConfig[] = [
    { name: 'GitHub Actions', type: 'github_actions', project_id: 'restaceratops', branch: 'main', trigger_on_push: true, trigger_on_pr: true },
    { name: 'Jenkins Pipeline', type: 'jenkins', project_id: 'restaceratops-jenkins', branch: 'develop', trigger_on_push: true, trigger_on_pr: false }
  ];

  const mockMonitoringConfigs: MonitoringConfig[] = [
    { 
      name: 'Production Monitoring', 
      enabled: true, 
      health_check_interval: 60,
      notification_channels: ['email', 'slack'],
      performance_thresholds: { response_time: 2.0, error_rate: 0.05, availability: 0.99 }
    },
    { 
      name: 'Development Monitoring', 
      enabled: true, 
      health_check_interval: 120,
      notification_channels: ['slack'],
      performance_thresholds: { response_time: 5.0, error_rate: 0.1, availability: 0.95 }
    }
  ];

  const mockSecurityConfigs: SecurityConfig[] = [
    {
      name: 'Production Security',
      rbac_enabled: true,
      audit_logging: true,
      encryption_enabled: true,
      session_timeout: 3600,
      compliance_standards: ['SOC2', 'GDPR', 'ISO27001']
    }
  ];

  const mockAuditLogs: AuditLog[] = [
    {
      timestamp: '2024-01-15T10:30:00Z',
      user_id: 'admin',
      action: 'login',
      resource: 'auth',
      details: { ip: '192.168.1.100' },
      ip_address: '192.168.1.100',
      success: true
    },
    {
      timestamp: '2024-01-15T10:25:00Z',
      user_id: 'developer',
      action: 'add_platform_config',
      resource: 'platform:web-app',
      details: { config: { type: 'web', base_url: 'https://app.example.com' } },
      success: true
    },
    {
      timestamp: '2024-01-15T10:20:00Z',
      user_id: 'developer',
      action: 'trigger_cicd_pipeline',
      resource: 'cicd:github-actions',
      details: { event_type: 'push', branch: 'main' },
      success: true
    }
  ];

  const mockSystemStatus: SystemStatus = {
    platforms: { count: 3, names: ['Web App', 'API Service', 'Mobile App'] },
    cicd: { count: 2, names: ['GitHub Actions', 'Jenkins Pipeline'] },
    monitoring: { count: 2, enabled: 2 },
    security: { count: 1, audit_logs: 150, active_sessions: 5 },
    performance: { metrics_count: 1250 }
  };

  useEffect(() => {
    // Simulate API calls
    const loadData = async () => {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setPlatforms(mockPlatforms);
      setCicdConfigs(mockCICDConfigs);
      setMonitoringConfigs(mockMonitoringConfigs);
      setSecurityConfigs(mockSecurityConfigs);
      setAuditLogs(mockAuditLogs);
      setSystemStatus(mockSystemStatus);
      setLoading(false);
    };

    loadData();
  }, []);

  const getPlatformIcon = (type: string) => {
    switch (type) {
      case 'web': return <FaGlobe className="text-blue-500" />;
      case 'mobile': return <FaMobile className="text-green-500" />;
      case 'api': return <FaMicrochip className="text-purple-500" />;
      case 'desktop': return <FaDesktop className="text-orange-500" />;
      case 'cloud': return <FaCloud className="text-indigo-500" />;
      default: return <FaServer className="text-gray-500" />;
    }
  };

  const getCICDIcon = (type: string) => {
    switch (type) {
      case 'github_actions': return <FaGithub className="text-gray-800" />;
      case 'gitlab_ci': return <FaGitlab className="text-orange-500" />;
      case 'jenkins': return <FaJenkins className="text-red-500" />;
      case 'azure_devops': return <FaMicrosoft className="text-blue-600" />;
      case 'circleci': return <FaCircle className="text-green-600" />;
      case 'travis_ci': return <FaCode className="text-blue-500" />;
      default: return <FaCodeBranch className="text-gray-500" />;
    }
  };

  const getStatusIcon = (success: boolean) => {
    return success ? 
      <FaCheckCircle className="text-green-500" /> : 
      <FaTimesCircle className="text-red-500" />;
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <FaTimesCircle className="text-red-500" />;
      case 'warning': return <FaExclamationTriangle className="text-yellow-500" />;
      case 'info': return <FaInfoCircle className="text-blue-500" />;
      default: return <FaInfoCircle className="text-gray-500" />;
    }
  };

  const renderOverview = () => (
    <div className="space-y-6">
      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100">Platforms</p>
              <p className="text-3xl font-bold">{systemStatus?.platforms.count || 0}</p>
            </div>
            <FaServer className="text-4xl text-blue-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">CI/CD Pipelines</p>
              <p className="text-3xl font-bold">{systemStatus?.cicd.count || 0}</p>
            </div>
            <FaCodeBranch className="text-4xl text-green-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">Monitoring</p>
              <p className="text-3xl font-bold">{systemStatus?.monitoring.enabled || 0}</p>
            </div>
            <FaChartLine className="text-4xl text-purple-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-red-100">Security</p>
              <p className="text-3xl font-bold">{systemStatus?.security.count || 0}</p>
            </div>
            <FaShieldAlt className="text-4xl text-red-200" />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            onClick={() => { setModalType('platform'); setShowAddModal(true); }}
            className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
          >
            <FaPlus className="mr-2 text-blue-500" />
            Add Platform
          </button>
          <button 
            onClick={() => { setModalType('cicd'); setShowAddModal(true); }}
            className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors"
          >
            <FaPlus className="mr-2 text-green-500" />
            Add CI/CD
          </button>
          <button 
            onClick={() => { setModalType('monitoring'); setShowAddModal(true); }}
            className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors"
          >
            <FaPlus className="mr-2 text-purple-500" />
            Add Monitoring
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {auditLogs.slice(0, 5).map((log, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                {getStatusIcon(log.success)}
                <div>
                  <p className="font-medium">{log.action}</p>
                  <p className="text-sm text-gray-600">{log.resource} by {log.user_id}</p>
                </div>
              </div>
              <span className="text-sm text-gray-500">
                {new Date(log.timestamp).toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderPlatforms = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Platform Management</h2>
        <button 
          onClick={() => { setModalType('platform'); setShowAddModal(true); }}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          <FaPlus className="inline mr-2" />
          Add Platform
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {platforms.map((platform, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getPlatformIcon(platform.type)}
                <h3 className="text-lg font-semibold">{platform.name}</h3>
              </div>
              <div className="flex space-x-2">
                <button className="text-blue-500 hover:text-blue-700">
                  <FaEye />
                </button>
                <button className="text-green-500 hover:text-green-700">
                  <FaEdit />
                </button>
                <button className="text-red-500 hover:text-red-700">
                  <FaTrash />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Type:</span> {platform.type}</p>
              <p><span className="font-medium">URL:</span> {platform.base_url}</p>
              <p><span className="font-medium">Timeout:</span> {platform.timeout}s</p>
              <p><span className="font-medium">Retries:</span> {platform.retry_attempts}</p>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 bg-green-500 text-white py-2 px-3 rounded text-sm hover:bg-green-600 transition-colors">
                <FaPlay className="inline mr-1" />
                Test
              </button>
              <button className="flex-1 bg-blue-500 text-white py-2 px-3 rounded text-sm hover:bg-blue-600 transition-colors">
                <FaCog className="inline mr-1" />
                Configure
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCICD = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">CI/CD Integration</h2>
        <button 
          onClick={() => { setModalType('cicd'); setShowAddModal(true); }}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
        >
          <FaPlus className="inline mr-2" />
          Add CI/CD
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {cicdConfigs.map((config, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getCICDIcon(config.type)}
                <h3 className="text-lg font-semibold">{config.name}</h3>
              </div>
              <div className="flex space-x-2">
                <button className="text-blue-500 hover:text-blue-700">
                  <FaEye />
                </button>
                <button className="text-green-500 hover:text-green-700">
                  <FaEdit />
                </button>
                <button className="text-red-500 hover:text-red-700">
                  <FaTrash />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Type:</span> {config.type}</p>
              <p><span className="font-medium">Project:</span> {config.project_id}</p>
              <p><span className="font-medium">Branch:</span> {config.branch}</p>
              <p><span className="font-medium">Push Trigger:</span> {config.trigger_on_push ? 'Yes' : 'No'}</p>
              <p><span className="font-medium">PR Trigger:</span> {config.trigger_on_pr ? 'Yes' : 'No'}</p>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 bg-green-500 text-white py-2 px-3 rounded text-sm hover:bg-green-600 transition-colors">
                <FaPlay className="inline mr-1" />
                Trigger
              </button>
              <button className="flex-1 bg-blue-500 text-white py-2 px-3 rounded text-sm hover:bg-blue-600 transition-colors">
                <FaCog className="inline mr-1" />
                Configure
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderMonitoring = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Monitoring & Alerts</h2>
        <button 
          onClick={() => { setModalType('monitoring'); setShowAddModal(true); }}
          className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition-colors"
        >
          <FaPlus className="inline mr-2" />
          Add Monitoring
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {monitoringConfigs.map((config, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <FaChartLine className="text-purple-500" />
                <h3 className="text-lg font-semibold">{config.name}</h3>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  config.enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {config.enabled ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="flex space-x-2">
                <button className="text-blue-500 hover:text-blue-700">
                  <FaEye />
                </button>
                <button className="text-green-500 hover:text-green-700">
                  <FaEdit />
                </button>
                <button className="text-red-500 hover:text-red-700">
                  <FaTrash />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Status:</span> {config.enabled ? 'Enabled' : 'Disabled'}</p>
              <p><span className="font-medium">Check Interval:</span> {config.health_check_interval}s</p>
              <p><span className="font-medium">Channels:</span> {config.notification_channels.join(', ')}</p>
            </div>

            <div className="mt-4">
              <h4 className="font-medium mb-2">Thresholds:</h4>
              <div className="space-y-1 text-sm">
                {Object.entries(config.performance_thresholds).map(([key, value]) => (
                  <p key={key}><span className="font-medium">{key}:</span> {value}</p>
                ))}
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 bg-green-500 text-white py-2 px-3 rounded text-sm hover:bg-green-600 transition-colors">
                <FaBell className="inline mr-1" />
                Test Alert
              </button>
              <button className="flex-1 bg-blue-500 text-white py-2 px-3 rounded text-sm hover:bg-blue-600 transition-colors">
                <FaCog className="inline mr-1" />
                Configure
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderSecurity = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Security & Compliance</h2>
        <button 
          onClick={() => { setModalType('security'); setShowAddModal(true); }}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
        >
          <FaPlus className="inline mr-2" />
          Add Security Config
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {securityConfigs.map((config, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <FaShieldAlt className="text-red-500" />
                <h3 className="text-lg font-semibold">{config.name}</h3>
              </div>
              <div className="flex space-x-2">
                <button className="text-blue-500 hover:text-blue-700">
                  <FaEye />
                </button>
                <button className="text-green-500 hover:text-green-700">
                  <FaEdit />
                </button>
                <button className="text-red-500 hover:text-red-700">
                  <FaTrash />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">RBAC:</span> {config.rbac_enabled ? 'Enabled' : 'Disabled'}</p>
              <p><span className="font-medium">Audit Logging:</span> {config.audit_logging ? 'Enabled' : 'Disabled'}</p>
              <p><span className="font-medium">Encryption:</span> {config.encryption_enabled ? 'Enabled' : 'Disabled'}</p>
              <p><span className="font-medium">Session Timeout:</span> {config.session_timeout}s</p>
            </div>

            <div className="mt-4">
              <h4 className="font-medium mb-2">Compliance Standards:</h4>
              <div className="flex flex-wrap gap-2">
                {config.compliance_standards.map((standard, idx) => (
                  <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                    {standard}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 bg-green-500 text-white py-2 px-3 rounded text-sm hover:bg-green-600 transition-colors">
                <FaShieldAlt className="inline mr-1" />
                Security Scan
              </button>
              <button className="flex-1 bg-blue-500 text-white py-2 px-3 rounded text-sm hover:bg-blue-600 transition-colors">
                <FaCog className="inline mr-1" />
                Configure
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Audit Logs */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Audit Logs</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2">Timestamp</th>
                <th className="text-left py-2">User</th>
                <th className="text-left py-2">Action</th>
                <th className="text-left py-2">Resource</th>
                <th className="text-left py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.map((log, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="py-2 text-sm">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="py-2 text-sm">{log.user_id}</td>
                  <td className="py-2 text-sm">{log.action}</td>
                  <td className="py-2 text-sm">{log.resource}</td>
                  <td className="py-2">
                    {getStatusIcon(log.success)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverview();
      case 'platforms':
        return renderPlatforms();
      case 'cicd':
        return renderCICD();
      case 'monitoring':
        return renderMonitoring();
      case 'security':
        return renderSecurity();
      default:
        return renderOverview();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Enterprise Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage multi-platform testing, CI/CD integration, monitoring, and security</p>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: FaChartLine },
              { id: 'platforms', label: 'Platforms', icon: FaServer },
              { id: 'cicd', label: 'CI/CD', icon: FaCodeBranch },
              { id: 'monitoring', label: 'Monitoring', icon: FaBell },
              { id: 'security', label: 'Security', icon: FaShieldAlt }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-md p-6">
          {renderContent()}
        </div>
      </div>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">
              Add {modalType.charAt(0).toUpperCase() + modalType.slice(1)}
            </h3>
            <p className="text-gray-600 mb-4">
              This feature will be implemented in the next iteration.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EnterpriseDashboard; 