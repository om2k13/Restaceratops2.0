// API service for communicating with the Restaceratops backend
import axios, { AxiosError } from 'axios';
import type { AxiosInstance, AxiosResponse } from 'axios';

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
  private axiosInstance: AxiosInstance;

  constructor(baseUrl: string = API_BASE_URL) {
    this.axiosInstance = axios.create({
      baseURL: baseUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for logging
    this.axiosInstance.interceptors.request.use(
      (config) => {
        console.log(`🌐 Making API request to: ${config.baseURL}${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for logging
    this.axiosInstance.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`✅ API success for ${response.config.url}:`, response.data);
        return response;
      },
      (error: AxiosError) => {
        console.error(`❌ API error for ${error.config?.url}:`, error.response?.data);
        return Promise.reject(error);
      }
    );
  }

  private async request<T>(endpoint: string, options: any = {}): Promise<T> {
    try {
      const response = await this.axiosInstance.request({
        url: endpoint,
        ...options,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
      }
      throw error;
    }
  }

  async healthCheck(): Promise<{ status: string; timestamp: string; ai_system: string; websocket_connections: number; active_executions: number }> {
    return this.request('/health');
  }

  async sendChatMessage(message: { message: string }): Promise<ChatResponse> {
    return this.request('/api/chat', {
      method: 'POST',
      data: message,
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
      data: {
        test_file: request.test_files[0],
        options: {
          parallel: request.parallel,
          timeout: request.timeout
        }
      },
    });
  }

  async runSingleUrlTest(request: { method: string; url: string }): Promise<{
    execution_id: string;
    status: string;
    response_time: number;
    response_code: number;
    response_body: string;
    error?: string;
  }> {
    return this.request('/api/tests/single-url', {
      method: 'POST',
      data: request,
    });
  }

  async uploadFile(file: File): Promise<{ status: string; message: string; filename: string; file_path: string }> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await this.axiosInstance.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
      }
      throw error;
    }
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
      const wsUrl = this.axiosInstance.defaults.baseURL?.replace('http', 'ws') + '/ws';
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
        
        if (status.status === 'completed' || status.status === 'failed') {
          isPolling = false;
          return;
        }
        
        setTimeout(poll, interval);
      } catch (error) {
        console.error('Polling error:', error);
        isPolling = false;
      }
    };
    
    poll();
    
    // Return cleanup function
    return () => {
      isPolling = false;
    };
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService; 