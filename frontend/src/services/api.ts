// API service for communicating with the Restaceratops backend

const API_BASE_URL = import.meta.env.PROD 
  ? import.meta.env.VITE_REACT_APP_API_BASE_URL || 'https://restaceratops.onrender.com'
  : 'http://localhost:8000';

export interface ChatMessage {
  message: string;
}

export interface ChatResponse {
  response: string;
  timestamp: string;
}

export interface TestResult {
  test_name: string;
  status: string;
  response_time: number;
  response_code: number;
  response_body: string;
  error?: string;
}

export interface DashboardStats {
  total_tests: number;
  success_rate: number;
  avg_response_time: number;
  running_tests: number;
  recent_results: TestResult[];
}

export interface TestSpecification {
  name: string;
  description: string;
  tests: any[];
}

export interface TestExecutionRequest {
  test_files: string[];
  parallel?: boolean;
  timeout?: number;
}

export interface TestExecutionStatus {
  execution_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  total_tests: number;
  completed_tests: number;
  passed_tests: number;
  failed_tests: number;
  start_time: string;
  end_time?: string;
  results: any[];
  test_files: string[];
  error?: string;
}

export interface SystemStats {
  ai_system: any;
  timestamp: string;
  active_executions: number;
  total_executions: number;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    console.log(`🌐 Making API request to: ${url}`);
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      console.log(`📡 Response status: ${response.status} for ${endpoint}`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error(`❌ API error for ${endpoint}:`, errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`✅ API success for ${endpoint}:`, data);
      return data;
    } catch (error) {
      console.error(`❌ API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async healthCheck(): Promise<{ status: string; timestamp: string; ai_system: string; websocket_connections: number; active_executions: number }> {
    return this.request('/health');
  }

  async sendChatMessage(message: { message: string }): Promise<ChatResponse> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify(message),
    });
  }

  async getDashboardStats(): Promise<DashboardStats> {
    return this.request('/api/dashboard');
  }

  async getTestSpecifications(): Promise<{ test_specifications: any[]; count: number }> {
    return this.request('/api/tests');
  }

  async getTestSpecification(testFile: string): Promise<{ name: string; tests: any[] }> {
    return this.request(`/api/tests/${encodeURIComponent(testFile)}`);
  }

  async runTests(request: TestExecutionRequest): Promise<{
    execution_id: string;
    status: string;
    total_tests: number;
    passed_tests: number;
    failed_tests: number;
    success_rate: number;
    avg_response_time: number;
    results: any[];
    test_file: string;
    timestamp: string;
  }> {
    return this.request('/api/tests/run', {
      method: 'POST',
      body: JSON.stringify({
        test_file: request.test_files[0],
        options: {
          parallel: request.parallel,
          timeout: request.timeout
        }
      }),
    });
  }

  async getExecutionStatus(executionId: string): Promise<TestExecutionStatus> {
    return this.request(`/api/tests/status`);
  }

  async getSystemStats(): Promise<SystemStats> {
    return this.request('/api/system/stats');
  }

  // WebSocket connection helper
  createWebSocketConnection(): WebSocket | null {
    try {
      const wsUrl = this.baseUrl.replace('http', 'ws') + '/ws';
      return new WebSocket(wsUrl);
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      return null;
    }
  }

  // Poll execution status (fallback for non-WebSocket scenarios)
  async pollExecutionStatus(executionId: string, onUpdate: (status: TestExecutionStatus) => void, interval: number = 1000): Promise<() => void> {
    let isPolling = true;
    
    const poll = async () => {
      if (!isPolling) return;
      
      try {
        const status = await this.getExecutionStatus(executionId);
        onUpdate(status);
        
        // Stop polling if execution is complete
        if (status.status === 'completed' || status.status === 'failed') {
          isPolling = false;
          return;
        }
      } catch (error) {
        console.error('Failed to poll execution status:', error);
        isPolling = false;
        return;
      }
      
      // Schedule next poll
      setTimeout(poll, interval);
    };
    
    // Start polling
    poll();
    
    // Return function to stop polling
    return () => {
      isPolling = false;
    };
  }
}

export const apiService = new ApiService();
export default ApiService; 