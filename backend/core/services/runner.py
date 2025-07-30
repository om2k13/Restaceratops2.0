#!/usr/bin/env python3
"""
🦖 Advanced Test Runner for Restaceratops
Comprehensive test execution engine with parallel processing and real-time reporting
"""

import asyncio
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import httpx
from pydantic import BaseModel

from backend.core.services.client import APIClient
from backend.core.services.assertions import run_assertions, AssertionErrorDetails

log = logging.getLogger("restaceratops.runner")

class TestStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class TestResult:
    """Test execution result"""
    test_id: str
    test_name: str
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: float = 0.0
    response_time: float = 0.0
    response_code: Optional[int] = None
    response_body: str = ""
    error_message: Optional[str] = None
    assertions_passed: int = 0
    assertions_failed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestSuite:
    """Test suite configuration"""
    name: str
    description: str
    tests: List[Dict[str, Any]]
    parallel: bool = False
    timeout: int = 300
    retries: int = 0
    environment: Dict[str, str] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionContext:
    """Test execution context"""
    variables: Dict[str, Any] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    base_url: Optional[str] = None
    timeout: int = 30
    verify_ssl: bool = True

class TestRunner:
    """Advanced test runner with parallel execution and real-time reporting"""
    
    def __init__(self):
        self.execution_history: Dict[str, List[TestResult]] = {}
        self.active_executions: Dict[str, asyncio.Task] = {}
        self.reporters: List[Callable] = []
        self.max_workers: int = 10
        self.semaphore: Optional[asyncio.Semaphore] = None
        
    def add_reporter(self, reporter: Callable):
        """Add a test result reporter"""
        self.reporters.append(reporter)
    
    async def run_suite(self, suite: TestSuite, execution_id: Optional[str] = None) -> Dict[str, Any]:
        """Run a complete test suite"""
        if execution_id is None:
            execution_id = str(uuid.uuid4())
        
        start_time = datetime.now()
        results: List[TestResult] = []
        
        # Initialize semaphore for parallel execution
        if suite.parallel:
            self.semaphore = asyncio.Semaphore(self.max_workers)
        
        try:
            # Create execution context
            context = ExecutionContext(
                variables=suite.variables,
                environment=suite.environment,
                timeout=suite.timeout
            )
            
            # Execute tests
            if suite.parallel:
                results = await self._run_tests_parallel(suite.tests, context, execution_id)
            else:
                results = await self._run_tests_sequential(suite.tests, context, execution_id)
            
            # Calculate summary
            summary = self._calculate_summary(results)
            
            # Store execution history
            self.execution_history[execution_id] = results
            
            # Generate report
            report = {
                "execution_id": execution_id,
                "suite_name": suite.name,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration": (datetime.now() - start_time).total_seconds(),
                "summary": summary,
                "results": [self._result_to_dict(result) for result in results],
                "metadata": {
                    "parallel": suite.parallel,
                    "timeout": suite.timeout,
                    "retries": suite.retries,
                    "total_tests": len(suite.tests)
                }
            }
            
            # Notify reporters
            await self._notify_reporters(report)
            
            return report
            
        except Exception as e:
            log.error(f"Test suite execution failed: {e}")
            return {
                "execution_id": execution_id,
                "error": str(e),
                "status": "failed",
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat()
            }
    
    async def _run_tests_parallel(self, tests: List[Dict[str, Any]], context: ExecutionContext, execution_id: str) -> List[TestResult]:
        """Run tests in parallel"""
        tasks = []
        
        for i, test_config in enumerate(tests):
            task = self._run_single_test(test_config, context, execution_id, i)
            tasks.append(task)
        
        # Execute all tests with semaphore limiting concurrency
        if self.semaphore:
            async def limited_task(task):
                async with self.semaphore:
                    return await task
            
            limited_tasks = [limited_task(task) for task in tasks]
            results = await asyncio.gather(*limited_tasks, return_exceptions=True)
        else:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        test_results = []
        for result in results:
            if isinstance(result, Exception):
                # Create error result
                error_result = TestResult(
                    test_id=str(uuid.uuid4()),
                    test_name="Unknown",
                    status=TestStatus.ERROR,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=str(result)
                )
                test_results.append(error_result)
            else:
                test_results.append(result)
        
        return test_results
    
    async def _run_tests_sequential(self, tests: List[Dict[str, Any]], context: ExecutionContext, execution_id: str) -> List[TestResult]:
        """Run tests sequentially"""
        results = []
        
        for i, test_config in enumerate(tests):
            try:
                result = await self._run_single_test(test_config, context, execution_id, i)
                results.append(result)
                
                # Add delay between tests if needed
                if i < len(tests) - 1:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                log.error(f"Test {i} failed: {e}")
                error_result = TestResult(
                    test_id=str(uuid.uuid4()),
                    test_name=test_config.get("name", f"Test {i}"),
                    status=TestStatus.ERROR,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=str(e)
                )
                results.append(error_result)
        
        return results
    
    async def _run_single_test(self, test_config: Dict[str, Any], context: ExecutionContext, execution_id: str, test_index: int) -> TestResult:
        """Run a single test"""
        test_id = str(uuid.uuid4())
        test_name = test_config.get("name", f"Test {test_index}")
        
        result = TestResult(
            test_id=test_id,
            test_name=test_name,
            status=TestStatus.RUNNING,
            start_time=datetime.now()
        )
        
        try:
            # Prepare test request
            request_config = test_config.get("request", {})
            method = request_config.get("method", "GET")
            url = request_config.get("url", "")
            
            # Resolve variables in URL
            url = self._resolve_variables(url, context.variables)
            
            # Prepare headers
            headers = {**context.headers, **request_config.get("headers", {})}
            headers = {k: self._resolve_variables(v, context.variables) for k, v in headers.items()}
            
            # Prepare body
            body = request_config.get("body", {})
            if isinstance(body, dict):
                body = {k: self._resolve_variables(v, context.variables) for k, v in body.items()}
            
            # Execute request
            start_time = time.time()
            async with httpx.AsyncClient(timeout=context.timeout, verify=context.verify_ssl) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if method in ["POST", "PUT", "PATCH"] else None,
                    params=request_config.get("params", {})
                )
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Update result
            result.response_time = response_time
            result.response_code = response.status_code
            result.response_body = response.text[:1000]  # Limit response body length
            
            # Run assertions
            assertions = test_config.get("assertions", [])
            passed_assertions = 0
            failed_assertions = 0
            
            for assertion in assertions:
                try:
                    run_assertions(response, [assertion])
                    passed_assertions += 1
                except AssertionErrorDetails as e:
                    failed_assertions += 1
                    log.warning(f"Assertion failed in {test_name}: {e}")
            
            result.assertions_passed = passed_assertions
            result.assertions_failed = failed_assertions
            
            # Determine test status
            if failed_assertions == 0:
                result.status = TestStatus.PASSED
            else:
                result.status = TestStatus.FAILED
                result.error_message = f"{failed_assertions} assertion(s) failed"
            
        except httpx.TimeoutException:
            result.status = TestStatus.FAILED
            result.error_message = "Request timeout"
        except httpx.RequestError as e:
            result.status = TestStatus.FAILED
            result.error_message = f"Request error: {e}"
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = str(e)
        
        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - result.start_time).total_seconds()
        
        return result
    
    def _resolve_variables(self, value: str, variables: Dict[str, Any]) -> str:
        """Resolve variables in a string value"""
        if not isinstance(value, str):
            return value
        
        for var_name, var_value in variables.items():
            placeholder = f"${{{var_name}}}"
            if placeholder in value:
                value = value.replace(placeholder, str(var_value))
        
        return value
    
    def _calculate_summary(self, results: List[TestResult]) -> Dict[str, Any]:
        """Calculate test execution summary"""
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        error = sum(1 for r in results if r.status == TestStatus.ERROR)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        
        total_duration = sum(r.duration for r in results)
        avg_duration = total_duration / total if total > 0 else 0
        
        total_response_time = sum(r.response_time for r in results)
        avg_response_time = total_response_time / total if total > 0 else 0
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "error": error,
            "skipped": skipped,
            "success_rate": round(success_rate, 2),
            "total_duration": round(total_duration, 2),
            "avg_duration": round(avg_duration, 2),
            "avg_response_time": round(avg_response_time, 2)
        }
    
    def _result_to_dict(self, result: TestResult) -> Dict[str, Any]:
        """Convert TestResult to dictionary"""
        return {
            "test_id": result.test_id,
            "test_name": result.test_name,
            "status": result.status.value,
            "start_time": result.start_time.isoformat(),
            "end_time": result.end_time.isoformat() if result.end_time else None,
            "duration": result.duration,
            "response_time": result.response_time,
            "response_code": result.response_code,
            "response_body": result.response_body,
            "error_message": result.error_message,
            "assertions_passed": result.assertions_passed,
            "assertions_failed": result.assertions_failed,
            "metadata": result.metadata
        }
    
    async def _notify_reporters(self, report: Dict[str, Any]):
        """Notify all registered reporters"""
        for reporter in self.reporters:
            try:
                if asyncio.iscoroutinefunction(reporter):
                    await reporter(report)
                else:
                    reporter(report)
            except Exception as e:
                log.error(f"Reporter notification failed: {e}")
    
    async def stop_execution(self, execution_id: str):
        """Stop a running test execution"""
        if execution_id in self.active_executions:
            task = self.active_executions[execution_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_executions[execution_id]
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a test execution"""
        if execution_id in self.execution_history:
            results = self.execution_history[execution_id]
            summary = self._calculate_summary(results)
            return {
                "execution_id": execution_id,
                "status": "completed",
                "summary": summary,
                "results_count": len(results)
            }
        elif execution_id in self.active_executions:
            return {
                "execution_id": execution_id,
                "status": "running"
            }
        else:
            return None

# Global test runner instance
test_runner = TestRunner()

# Convenience function for running test suites
async def run_suite(test_file: str, **kwargs) -> Dict[str, Any]:
    """Run a test suite from a file"""
    try:
        # Load test configuration from file
        # This is a simplified version - in reality, you'd load from YAML/JSON
        suite_config = {
            "name": "Test Suite",
            "description": "Generated test suite",
            "tests": [
                {
                    "name": "Sample Test",
                    "request": {
                        "method": "GET",
                        "url": "https://httpbin.org/get",
                        "headers": {}
                    },
                    "assertions": [
                        {"status_code": 200}
                    ]
                }
            ],
            "parallel": kwargs.get("parallel", False),
            "timeout": kwargs.get("timeout", 300),
            "retries": kwargs.get("retries", 0)
        }
        
        suite = TestSuite(**suite_config)
        return await test_runner.run_suite(suite)
        
    except Exception as e:
        log.error(f"Failed to run test suite: {e}")
        return {
            "error": str(e),
            "status": "failed"
        }
