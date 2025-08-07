import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, test, expect, vi } from 'vitest';
import App from '../App';

// Mock the components to avoid complex dependencies
vi.mock('../pages/ChatInterface', () => ({ default: () => <div data-testid="chat-interface">Chat Interface</div> }));
vi.mock('../pages/Dashboard', () => ({ default: () => <div data-testid="dashboard">Dashboard</div> }));
vi.mock('../pages/Reports', () => ({ default: () => <div data-testid="reports">Reports</div> }));
vi.mock('../pages/Settings', () => ({ default: () => <div data-testid="settings">Settings</div> }));
vi.mock('../pages/TestBuilder', () => ({ default: () => <div data-testid="test-builder">Test Builder</div> }));
vi.mock('../pages/TestRunner', () => ({ default: () => <div data-testid="test-runner">Test Runner</div> }));
vi.mock('../pages/WorkflowInterface', () => ({ default: () => <div data-testid="workflow-interface">Workflow Interface</div> }));
vi.mock('../pages/TestGenerator', () => ({ default: () => <div data-testid="test-generator">Test Generator</div> }));
vi.mock('../pages/TestMonitor', () => ({ default: () => <div data-testid="test-monitor">Test Monitor</div> }));
vi.mock('../pages/AnalyticsDashboard', () => ({ default: () => <div data-testid="analytics-dashboard">Analytics Dashboard</div> }));
vi.mock('../pages/EnterpriseDashboard', () => ({ default: () => <div data-testid="enterprise-dashboard">Enterprise Dashboard</div> }));

describe('App Component', () => {
  test('renders the main navigation', () => {
    render(<App />);
    
    // Check for main navigation items (using more specific selectors)
    expect(screen.getByRole('link', { name: 'Dashboard' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'AI Chat' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Workflow' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Test Generator' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Test Monitor' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Analytics' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Enterprise' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Test Builder' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Test Runner' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Reports' })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Settings' })).toBeInTheDocument();
  });

  test('renders the app title', () => {
    render(<App />);
    expect(screen.getByText('Restaceratops')).toBeInTheDocument();
    expect(screen.getByText('AI Testing Platform')).toBeInTheDocument();
  });

  test('renders user section', () => {
    render(<App />);
    expect(screen.getByText('User')).toBeInTheDocument();
    expect(screen.getByText('user@example.com')).toBeInTheDocument();
  });
}); 