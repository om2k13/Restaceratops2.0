// WebSocket service for real-time communication with the Restaceratops backend

export interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export interface ChatResponse {
  type: 'chat_response';
  response: string;
  timestamp: string;
}

export interface DashboardUpdate {
  type: 'dashboard_update';
  data: any;
}

export interface TestCompleted {
  type: 'test_completed';
  data: any;
}

export interface PongMessage {
  type: 'pong';
  timestamp: string;
}

type MessageHandler = (message: WebSocketMessage) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private messageHandlers: Map<string, MessageHandler[]> = new Map();
  private isConnecting = false;
  private pingInterval: NodeJS.Timeout | null = null;

  private url: string;
  
  constructor(url: string) {
    this.url = url;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        reject(new Error('Connection already in progress'));
        return;
      }

      this.isConnecting = true;

      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.isConnecting = false;
          this.reconnectAttempts = 0;
          this.startPingInterval();
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.ws.onclose = (event) => {
          console.log('WebSocket disconnected:', event.code, event.reason);
          this.isConnecting = false;
          this.stopPingInterval();
          
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.scheduleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.isConnecting = false;
          reject(error);
        };

      } catch (error) {
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  disconnect(): void {
    this.stopPingInterval();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private scheduleReconnect(): void {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    setTimeout(() => {
              if (this.ws && this.ws.readyState !== WebSocket.OPEN) {
          console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          this.connect().catch((error) => console.error(error));
        }
    }, delay);
  }

  private startPingInterval(): void {
    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.send({ type: 'ping' });
      }
    }, 30000); // Send ping every 30 seconds
  }

  private stopPingInterval(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  send(message: WebSocketMessage): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  subscribeToMessageType(type: string, handler: MessageHandler): () => void {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      handlers.push(handler);
    }

    // Return unsubscribe function
    return () => {
      const handlers = this.messageHandlers.get(type);
      if (handlers) {
        const index = handlers.indexOf(handler);
        if (index > -1) {
          handlers.splice(index, 1);
        }
      }
    };
  }

  private handleMessage(message: WebSocketMessage): void {
    const handlers = this.messageHandlers.get(message.type);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message);
        } catch (error) {
          console.error('Error in message handler:', error);
        }
      });
    }
  }

  // Convenience methods for specific message types
  subscribeToChatResponses(handler: (message: ChatResponse) => void): () => void {
    return this.subscribeToMessageType('chat_response', (msg) => handler(msg as ChatResponse));
  }

  subscribeToDashboardUpdates(handler: (message: DashboardUpdate) => void): () => void {
    return this.subscribeToMessageType('dashboard_update', (msg) => handler(msg as DashboardUpdate));
  }

  subscribeToTestCompleted(handler: (message: TestCompleted) => void): () => void {
    return this.subscribeToMessageType('test_completed', (msg) => handler(msg as TestCompleted));
  }

  subscribeToPong(handler: (message: PongMessage) => void): () => void {
    return this.subscribeToMessageType('pong', (msg) => handler(msg as PongMessage));
  }

  // Send chat message
  sendChatMessage(message: string): void {
    this.send({ type: 'chat', message });
  }

  // Subscribe to dashboard updates
  subscribeToDashboard(): void {
    this.send({ type: 'subscribe_dashboard' });
  }

  // Get connection status
  getConnectionStatus(): 'connecting' | 'connected' | 'disconnected' {
    if (this.isConnecting) return 'connecting';
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return 'connected';
    return 'disconnected';
  }
}

// Create and export a singleton instance
export const websocketService = new WebSocketService('ws://localhost:8000/ws');

// Export the class for testing or custom instances
export default WebSocketService; 