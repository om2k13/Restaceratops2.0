#!/usr/bin/env python3
"""
🦖 Enhanced Chat Interface for Restaceratops
Advanced AI-powered API testing agent with vector store, RAG, and multi-model support
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import openai
from backend.core.services.runner import run_suite
from backend.core.services.dsl_loader import load_tests
from backend.core.agents.enhanced_ai_system import get_enhanced_ai_system
from backend.core.agents.openrouter_ai_system import get_openrouter_ai_system
from backend.core.agents.gemini_ai_system import get_gemini_ai_system

log = logging.getLogger("agent.enhanced_chat_interface")

class EnhancedRestaceratopsChat:
    """Enhanced conversational interface for Restaceratops API testing agent with advanced AI capabilities."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        # Initialize OpenRouter AI system (primary - free models)
        self.openrouter_ai = get_openrouter_ai_system()
        
        # Initialize Gemini AI system (backup - free tier)
        self.gemini_ai = get_gemini_ai_system()
        
        # Initialize enhanced AI system (fallback)
        self.enhanced_ai = get_enhanced_ai_system(api_key)
        
        # Initialize system
        self.initialized = False
        
        log.info("Enhanced Restaceratops Chat initialized with OpenRouter AI (primary) + Gemini (backup) - Free models only")
        
    async def initialize(self):
        """Initialize the enhanced AI system."""
        if not self.initialized:
            # The new enhanced AI system doesn't need explicit initialization
            # Just mark as initialized
            self.initialized = True
            log.info("Enhanced AI system initialized with OpenRouter + fallback support")
    
    def _extract_api_info(self, user_input: str) -> Dict:
        """Extract API information from user input."""
        info = {}
        
        # Look for URLs
        import re
        urls = re.findall(r'https?://[^\s]+', user_input)
        if urls:
            info['base_url'] = urls[0]
        
        # Look for common API patterns
        if 'health' in user_input.lower():
            info['endpoints'] = ['/health']
        if 'auth' in user_input.lower() or 'login' in user_input.lower():
            info['endpoints'] = ['/auth/login']
        if 'user' in user_input.lower():
            info['endpoints'] = ['/users']
        
        return info
    
    async def handle_message(self, user_input: str) -> str:
        """Handle user input and return a response using OpenRouter AI system."""
        # Initialize system if not already done
        if not self.initialized:
            await self.initialize()
        
        user_input_lower = user_input.lower().strip()
        
        # Check for simple greetings first (before API testing commands)
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            try:
                # Try OpenRouter AI first
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                # Fallback to Gemini AI if OpenRouter fails
                if self.gemini_ai.is_initialized:
                    try:
                        return await self.gemini_ai.handle_conversation(user_input)
                    except Exception as e2:
                        # Fall back to enhanced fallback system if both fail
                        return self.enhanced_ai._get_fallback_response(user_input)
                else:
                    # Fall back to enhanced fallback system if both fail
                    return self.enhanced_ai._get_fallback_response(user_input)
        
        # Check for specific API testing commands
        elif any(word in user_input_lower for word in ['test my api', 'test api', 'run test']):
            return await self._handle_api_testing(user_input)
        
        # Check for test creation requests
        elif any(word in user_input_lower for word in ['create test', 'generate test', 'make test']):
            return await self._handle_test_creation(user_input)
        
        # Check for status/report requests
        elif any(word in user_input_lower for word in ['status', 'report', 'results', 'how did']):
            return await self._handle_status_request(user_input)
        
        # Check for help requests
        elif any(word in user_input_lower for word in ['help', 'what can you do', 'how to use']):
            return await self._handle_help_request(user_input)
        
        # Check for debugging requests
        elif any(word in user_input_lower for word in ['debug', 'troubleshoot', 'fix', 'issue', 'problem', 'error']):
            return await self._handle_debug_request(user_input)
        
        # Check for detailed report requests
        elif any(word in user_input_lower for word in ['detailed report', 'comprehensive report', 'full report', 'complete report']):
            return await self._handle_detailed_report_request(user_input)
        
        # Check for system info requests
        elif any(word in user_input_lower for word in ['system info', 'system status', 'system configuration']):
            return await self._handle_system_info_request(user_input)
        
        # Default: general conversation
        else:
            try:
                # Try OpenRouter AI first for general conversation
                return await self.openrouter_ai.handle_conversation(user_input)
            except Exception as e:
                # Fallback to Gemini AI if OpenRouter fails
                if self.gemini_ai.is_initialized:
                    try:
                        return await self.gemini_ai.handle_conversation(user_input)
                    except Exception as e2:
                        # Fall back to enhanced fallback system if both fail
                        return self.enhanced_ai._get_fallback_response(user_input)
                else:
                    # Fall back to enhanced fallback system if both fail
                    return self.enhanced_ai._get_fallback_response(user_input)
    
    async def _handle_api_testing(self, user_input: str) -> str:
        """Handle API testing requests."""
        api_info = self._extract_api_info(user_input)
        base_url = api_info.get('base_url', 'https://your-api.com')
        
        if not base_url or base_url == 'https://your-api.com':
            return """❌ I couldn't find a valid API URL in your message.

Please provide a URL like:
• test api https://api.example.com
• test api https://jsonplaceholder.typicode.com/posts
• test api https://dog.ceo/api/breeds/image/random

I'll then test the specific endpoints and give you detailed results!"""
        
        try:
            # Actually test the API endpoints
            import requests
            import time
            from urllib.parse import urljoin
            
            results = []
            test_endpoints = self._get_test_endpoints(base_url)
            
            for endpoint in test_endpoints:
                try:
                    full_url = urljoin(base_url, endpoint)
                    start_time = time.time()
                    response = requests.get(full_url, timeout=10)
                    response_time = time.time() - start_time
                    
                    status = "✅" if response.status_code < 400 else "⚠️"
                    results.append({
                        'endpoint': endpoint,
                        'url': full_url,
                        'status_code': response.status_code,
                        'response_time': round(response_time, 2),
                        'status': status,
                        'content_length': len(response.content)
                    })
                except requests.exceptions.RequestException as e:
                    results.append({
                        'endpoint': endpoint,
                        'url': full_url,
                        'status_code': 'ERROR',
                        'response_time': 0,
                        'status': '❌',
                        'error': str(e)
                    })
            
            # Generate unique response based on actual results
            successful_tests = [r for r in results if r['status'] == '✅']
            failed_tests = [r for r in results if r['status'] in ['⚠️', '❌']]
            
            response = f"""🔍 **API Test Results for {base_url}**

**Test Summary:**
• Total endpoints tested: {len(results)}
• ✅ Successful: {len(successful_tests)}
• ⚠️/❌ Issues: {len(failed_tests)}

**Detailed Results:**
"""
            
            for result in results:
                if result['status'] == '✅':
                    response += f"• {result['status']} {result['endpoint']} - {result['status_code']} ({result['response_time']}s, {result['content_length']} bytes)\n"
                elif result['status'] == '⚠️':
                    response += f"• {result['status']} {result['endpoint']} - {result['status_code']} (unexpected status)\n"
                else:
                    response += f"• {result['status']} {result['endpoint']} - {result.get('error', 'Connection failed')}\n"
            
            if len(successful_tests) == len(results):
                response += f"\n🎉 **All tests passed!** Your API at {base_url} is working perfectly!"
            elif len(successful_tests) > len(failed_tests):
                response += f"\n⚠️ **Most tests passed** but there are some issues to address."
            else:
                response += f"\n❌ **Multiple issues found** with your API at {base_url}."
            
            response += f"""

**Next Steps:**
• Run specific endpoint tests
• Check authentication requirements
• Review API documentation
• Test with different parameters

Would you like me to test specific endpoints or help debug any issues?"""
            
            return response
                
        except Exception as e:
            return f"""❌ Sorry, I encountered an error while testing your API.

**Error:** {str(e)}

**Troubleshooting:**
• Make sure your API is running
• Check if the URL is correct
• Verify network connectivity
• Ensure proper authentication

Would you like me to help you troubleshoot this?"""
    
    def _get_test_endpoints(self, base_url: str) -> list:
        """Get appropriate test endpoints based on the API URL."""
        # Common API endpoints to test
        common_endpoints = ['', '/', '/health', '/status', '/api', '/docs', '/swagger']
        
        # API-specific endpoints based on URL patterns
        if 'dog.ceo' in base_url:
            return ['', '/breeds/image/random', '/breeds/list/all', '/breeds/hound/images']
        elif 'cat-fact' in base_url:
            return ['', '/facts', '/facts/random', '/breeds']
        elif 'jsonplaceholder' in base_url:
            return ['', '/posts', '/users', '/comments', '/albums']
        elif 'api.github.com' in base_url:
            return ['', '/user', '/repos', '/rate_limit']
        elif 'httpbin.org' in base_url:
            return ['', '/get', '/post', '/put', '/delete', '/status/200', '/status/404']
        else:
            # For unknown APIs, test common endpoints
            return common_endpoints
    
    async def _handle_test_creation(self, user_input: str) -> str:
        """Handle test creation requests."""
        api_info = self._extract_api_info(user_input)
        base_url = api_info.get('base_url', 'https://your-api.com')
        
        try:
            # Try OpenRouter AI first for test generation
            test_yaml = await self.openrouter_ai.generate_api_tests(
                base_url,
                f"Create tests for: {user_input}"
            )
            
            # Clean the YAML output - remove markdown formatting if present
            if test_yaml.startswith('```yaml'):
                # Remove markdown code block
                test_yaml = test_yaml.replace('```yaml', '').replace('```', '').strip()
            
            # Remove any explanatory text after the YAML
            if '**Requirements:**' in test_yaml:
                test_yaml = test_yaml.split('**Requirements:**')[0].strip()
            
            # Save to file
            test_file = Path("tests/generated_openrouter.yml")
            test_file.parent.mkdir(exist_ok=True)
            test_file.write_text(test_yaml)
            
            return f"""✅ Test cases generated successfully!

I've created comprehensive test cases for your API at {base_url}.

**Generated Tests:**
• Saved to: `tests/generated_openrouter.yml`
• Includes multiple test scenarios
• Covers various HTTP methods
• Includes error handling

**What's Included:**
• Health check tests
• Authentication flows
• CRUD operations
• Error scenarios
• Performance validation

Would you like me to:
• Run these tests now?
• Generate additional test cases?
• Show you the test contents?"""
            
        except Exception as e:
            return f"""❌ Sorry, I encountered an error while generating tests.

**Error:** {str(e)}

**Fallback Response:**
I can still help you create basic test cases manually. Would you like me to:
• Show you a test template?
• Help you write tests step by step?
• Explain how to structure your tests?"""
    
    async def _handle_status_request(self, user_input: str) -> str:
        """Handle status and report requests."""
        try:
            # Check for recent test files and generate actual status
            import os
            from pathlib import Path
            from datetime import datetime
            
            # Look for test reports and results
            test_files = []
            report_files = []
            
            # Check for test files
            if os.path.exists("tests"):
                test_files = [f for f in os.listdir("tests") if f.endswith(('.yml', '.yaml', '.json'))]
            
            # Check for report files
            if os.path.exists("data/reports"):
                report_files = [f for f in os.listdir("data/reports") if f.endswith(('.html', '.xml', '.json'))]
            
            # Check for recent test results
            recent_tests = []
            if os.path.exists("data/report.xml"):
                recent_tests.append("JUnit XML report (data/report.xml)")
            if os.path.exists("data/reports/test_report.html"):
                recent_tests.append("HTML report (data/reports/test_report.html)")
            
            # Get system stats
            system_stats = self.get_system_stats()
            
            # Generate dynamic status report
            status_report = f"""📊 **Current System Status Report**

**System Information:**
• AI Providers: {len(system_stats.get('ai_providers', []))}
• Primary Provider: {system_stats.get('primary_provider', 'Unknown')}
• Fallback Provider: {system_stats.get('fallback_provider', 'Unknown')}

**Available Test Files:**
"""
            
            if test_files:
                for file in test_files[:5]:  # Show first 5 files
                    status_report += f"• {file}\n"
            else:
                status_report += "• No test files found\n"
            
            status_report += f"""
**Available Reports:**
"""
            
            if recent_tests:
                for report in recent_tests:
                    status_report += f"• {report}\n"
            else:
                status_report += "• No recent reports found\n"
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_report += f"""
**Last Updated:** {timestamp}

**Quick Actions:**
• Run API tests: "test api https://your-api.com"
• Generate test cases: "create tests for my API"
• View detailed results: "show detailed report"
• Get system info: "system status"

**Available Commands:**
• "test api [url]" - Test specific API endpoints
• "create tests" - Generate new test cases
• "show reports" - View available reports
• "debug issues" - Get troubleshooting help
• "system info" - Show system configuration"""
            
            return status_report
            
        except Exception as e:
            return f"""📊 **Status Report** (Fallback)

**System Status:** Operational
**Last Check:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Available Actions:**
• Test APIs: "test api [url]"
• Generate tests: "create tests"
• Get help: "help"

**Error Details:** {str(e)}"""
    
    async def _handle_help_request(self, user_input: str) -> str:
        """Handle help requests."""
        try:
            # Get system stats for context
            system_stats = self.get_system_stats()
            
            # Check what's available
            import os
            has_tests = os.path.exists("tests") and len(os.listdir("tests")) > 0
            has_reports = os.path.exists("data/reports") and len(os.listdir("data/reports")) > 0
            
            help_text = f"""🦖 **Restaceratops AI Testing Assistant - Help Guide**

**System Status:**
• AI Providers: {len(system_stats.get('ai_providers', []))} available
• Primary: {system_stats.get('primary_provider', 'Unknown')}
• Fallback: {system_stats.get('fallback_provider', 'Unknown')}

**📋 Available Commands:**

**🔍 API Testing:**
• "test api https://your-api.com" - Test specific API endpoints
• "test api https://api.example.com/health" - Test health endpoint
• "test api https://jsonplaceholder.typicode.com/posts" - Test specific endpoint

**📝 Test Generation:**
• "create tests for my API" - Generate test cases
• "create tests for authentication" - Generate auth tests
• "create tests for user endpoints" - Generate user-related tests

**📊 Reports & Status:**
• "show status" - Current system status
• "show detailed report" - Comprehensive test report
• "show test results" - Latest test results
• "debug issues" - Troubleshooting help

**🛠️ Advanced Features:**
• "generate openapi tests" - Create tests from OpenAPI spec
• "performance test" - Run performance benchmarks
• "security test" - Run security-focused tests
• "load test" - Run load testing scenarios

**📁 File Management:**
• "list test files" - Show available test files
• "show reports" - List available reports
• "export results" - Export test results

**❓ Help & Support:**
• "help" - Show this help message
• "system info" - Show system configuration
• "troubleshoot" - Get debugging assistance

**💡 Quick Examples:**
```
test api https://dog.ceo/api/
create tests for https://api.github.com
show status
debug connection issues
```

**🔧 Current System:**
• Test Files: {'Available' if has_tests else 'None found'}
• Reports: {'Available' if has_reports else 'None found'}
• Status: Operational

**Need specific help?** Try:
• "help api testing" - API testing guide
• "help test generation" - Test creation guide
• "help troubleshooting" - Debugging guide"""
            
            return help_text
            
        except Exception as e:
            return f"""🦖 **Help Guide** (Fallback)

**Quick Commands:**
• "test api [url]" - Test API endpoints
• "create tests" - Generate test cases
• "show status" - System status
• "debug issues" - Troubleshooting

**Error Details:** {str(e)}"""
    
    async def _handle_debug_request(self, user_input: str) -> str:
        """Handle debugging and troubleshooting requests."""
        try:
            import os
            import psutil
            from datetime import datetime
            
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Check for common issues
            issues = []
            warnings = []
            
            # Check disk space
            if disk.percent > 90:
                issues.append(f"⚠️ Low disk space: {disk.percent}% used")
            elif disk.percent > 70:
                warnings.append(f"📊 Disk usage: {disk.percent}%")
            
            # Check memory
            if memory.percent > 90:
                issues.append(f"⚠️ High memory usage: {memory.percent}%")
            elif memory.percent > 70:
                warnings.append(f"📊 Memory usage: {memory.percent}%")
            
            # Check for test files
            if not os.path.exists("tests"):
                warnings.append("📁 No tests directory found")
            
            # Check for reports
            if not os.path.exists("data/reports"):
                warnings.append("📊 No reports directory found")
            
            # Get system stats
            system_stats = self.get_system_stats()
            
            debug_report = f"""🔧 **System Debug Report**

**System Health:**
• CPU Usage: {cpu_percent}%
• Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
• Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)

**AI System Status:**
• Primary Provider: {system_stats.get('primary_provider', 'Unknown')}
• Fallback Provider: {system_stats.get('fallback_provider', 'Unknown')}
• Available Providers: {len(system_stats.get('ai_providers', []))}

**Issues Found:**
"""
            
            if issues:
                for issue in issues:
                    debug_report += f"• {issue}\n"
            else:
                debug_report += "• ✅ No critical issues detected\n"
            
            debug_report += f"""
**Warnings:**
"""
            
            if warnings:
                for warning in warnings:
                    debug_report += f"• {warning}\n"
            else:
                debug_report += "• ✅ No warnings\n"
            
            debug_report += f"""
**Troubleshooting Steps:**
1. **API Testing Issues:**
   • Verify API URLs are correct
   • Check network connectivity
   • Ensure APIs are running

2. **System Performance:**
   • Restart the application if needed
   • Check available disk space
   • Monitor memory usage

3. **AI Provider Issues:**
   • Check API key configuration
   • Verify internet connectivity
   • Try fallback providers

**Quick Fixes:**
• "restart system" - Restart the application
• "clear cache" - Clear temporary files
• "check connectivity" - Test network connections
• "test ai providers" - Verify AI system status

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
            
            return debug_report
            
        except Exception as e:
            return f"""🔧 **Debug Report** (Fallback)

**Basic System Check:**
• Status: Operational
• Error: {str(e)}

**Common Solutions:**
• Restart the application
• Check network connectivity
• Verify API configurations
• Clear cache and temporary files"""
    
    async def _handle_detailed_report_request(self, user_input: str) -> str:
        """Handle detailed report requests."""
        try:
            import os
            from datetime import datetime
            
            # Get comprehensive system information
            system_stats = self.get_system_stats()
            
            # Check for test files and reports
            test_files = []
            report_files = []
            
            if os.path.exists("tests"):
                test_files = [f for f in os.listdir("tests") if f.endswith(('.yml', '.yaml', '.json'))]
            
            if os.path.exists("data/reports"):
                report_files = [f for f in os.listdir("data/reports") if f.endswith(('.html', '.xml', '.json'))]
            
            # Generate detailed report
            detailed_report = f"""📊 **Comprehensive System Report**

**System Information:**
• Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• AI Providers: {len(system_stats.get('ai_providers', []))}
• Primary Provider: {system_stats.get('primary_provider', 'Unknown')}
• Fallback Provider: {system_stats.get('fallback_provider', 'Unknown')}

**Test Infrastructure:**
• Test Files: {len(test_files)} found
• Report Files: {len(report_files)} found
• Test Directory: {'✅ Available' if os.path.exists('tests') else '❌ Missing'}
• Reports Directory: {'✅ Available' if os.path.exists('data/reports') else '❌ Missing'}

**Available Test Files:**
"""
            
            if test_files:
                for file in test_files:
                    file_path = os.path.join("tests", file)
                    file_size = os.path.getsize(file_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")
                    detailed_report += f"• {file} ({file_size} bytes, modified: {modified})\n"
            else:
                detailed_report += "• No test files found\n"
            
            detailed_report += f"""
**Available Reports:**
"""
            
            if report_files:
                for file in report_files:
                    file_path = os.path.join("data/reports", file)
                    file_size = os.path.getsize(file_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")
                    detailed_report += f"• {file} ({file_size} bytes, modified: {modified})\n"
            else:
                detailed_report += "• No report files found\n"
            
            detailed_report += f"""
**AI System Details:**
"""
            
            # Add AI provider details
            if 'openrouter' in system_stats:
                openrouter = system_stats['openrouter']
                detailed_report += f"• OpenRouter: {openrouter.get('total_models', 0)} models, {openrouter.get('working_models', 0)} working\n"
            
            if 'enhanced_ai' in system_stats:
                enhanced = system_stats['enhanced_ai']
                detailed_report += f"• Enhanced AI: {enhanced.get('total_providers', 0)} providers, {enhanced.get('working_providers', 0)} working\n"
            
            detailed_report += f"""
**Recent Activity:**
• Last API Test: {'Available' if os.path.exists('data/report.xml') else 'None'}
• Last Report Generated: {'Available' if report_files else 'None'}
• System Uptime: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Recommendations:**
• Run API tests to generate fresh data
• Create test cases for your APIs
• Monitor system performance
• Review generated reports

**Export Options:**
• JSON format: Available
• HTML format: Available
• XML format: Available
• CSV format: Available"""
            
            return detailed_report
            
        except Exception as e:
            return f"""📊 **Detailed Report** (Fallback)

**Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status:** Operational
**Error:** {str(e)}

**Available Data:**
• System status
• Basic configuration
• Error logs (if any)"""
    
    async def _handle_system_info_request(self, user_input: str) -> str:
        """Handle system information requests."""
        try:
            import os
            import platform
            from datetime import datetime
            
            # Get system information
            system_info = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'python_version': platform.python_version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'working_directory': os.getcwd(),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Get system stats
            system_stats = self.get_system_stats()
            
            system_info_text = f"""🖥️ **System Information**

**Platform Details:**
• Operating System: {system_info['platform']} {system_info['platform_version']}
• Python Version: {system_info['python_version']}
• Architecture: {system_info['architecture']}
• Processor: {system_info['processor']}

**Application Details:**
• Working Directory: {system_info['working_directory']}
• Current Time: {system_info['timestamp']}

**AI Configuration:**
• Primary Provider: {system_stats.get('primary_provider', 'Unknown')}
• Fallback Provider: {system_stats.get('fallback_provider', 'Unknown')}
• Total AI Providers: {len(system_stats.get('ai_providers', []))}

**Directory Structure:**
• Tests Directory: {'✅ Available' if os.path.exists('tests') else '❌ Missing'}
• Reports Directory: {'✅ Available' if os.path.exists('data/reports') else '❌ Missing'}
• Data Directory: {'✅ Available' if os.path.exists('data') else '❌ Missing'}
• Vector DB: {'✅ Available' if os.path.exists('vector_db') else '❌ Missing'}

**Environment:**
• Environment Variables: {len(os.environ)} loaded
• Python Path: {len(sys.path)} directories

**Status:** ✅ Operational
**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
            
            return system_info_text
            
        except Exception as e:
            return f"""🖥️ **System Information** (Fallback)

**Status:** Operational
**Error:** {str(e)}
**Time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        openrouter_stats = self.openrouter_ai.get_system_stats()
        enhanced_stats = self.enhanced_ai.get_system_stats()
        gemini_stats = self.gemini_ai.get_system_stats()
        
        return {
            "primary_provider": "OpenRouter",
            "backup_provider": "Gemini AI",
            "fallback_provider": "Enhanced AI System",
            "openrouter": openrouter_stats,
            "gemini_ai": gemini_stats,
            "enhanced_ai": enhanced_stats
        }
    
    async def chat_loop(self):
        """Main chat loop for interactive conversation."""
        print("🦖 Enhanced Restaceratops Chat Interface")
        print("=" * 50)
        print("Talk to me in simple English! I can help you test APIs, create test cases, and more.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🦖 Goodbye! Happy API testing!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🦖 Restaceratops: ", end="", flush=True)
                response = await self.handle_message(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n🦖 Goodbye! Happy API testing!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")

def main():
    """Main entry point for the enhanced chat interface."""
    import argparse
    parser = argparse.ArgumentParser(description="🦖 Enhanced Restaceratops Chat Interface")
    parser.add_argument("--api-key", help="OpenAI API key for fallback features")
    args = parser.parse_args()
    
    # Initialize chat interface
    chat = EnhancedRestaceratopsChat(api_key=args.api_key)
    
    # Start chat loop
    asyncio.run(chat.chat_loop())

if __name__ == "__main__":
    main() 