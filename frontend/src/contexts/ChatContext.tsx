import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ChatMessage {
  id: string;
  message: string;
  response: string;
  timestamp: string;
  isUser: boolean;
}

interface ChatContextType {
  messages: ChatMessage[];
  inputMessage: string;
  isLoading: boolean;
  error: string | null;
  setMessages: (messages: ChatMessage[]) => void;
  setInputMessage: (message: string) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  addMessage: (message: ChatMessage) => void;
  clearChat: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      message: '',
      response: `🦖 Welcome to Restaceratops AI Assistant!

I'm here to help you with API testing. I can:

✅ Generate test cases from OpenAPI specifications
✅ Help debug API issues
✅ Explain testing concepts
✅ Provide testing best practices
✅ Analyze test results

How can I help you today?`,
      timestamp: new Date().toISOString(),
      isUser: false
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addMessage = (message: ChatMessage) => {
    setMessages(prev => [...prev, message]);
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        message: '',
        response: `🦖 Welcome to Restaceratops AI Assistant!

I'm here to help you with API testing. I can:

✅ Generate test cases from OpenAPI specifications
✅ Help debug API issues
✅ Explain testing concepts
✅ Provide testing best practices
✅ Analyze test results

How can I help you today?`,
        timestamp: new Date().toISOString(),
        isUser: false
      }
    ]);
    setInputMessage('');
    setError(null);
  };

  const value: ChatContextType = {
    messages,
    inputMessage,
    isLoading,
    error,
    setMessages,
    setInputMessage,
    setIsLoading,
    setError,
    addMessage,
    clearChat
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}; 