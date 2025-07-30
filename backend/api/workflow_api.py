#!/usr/bin/env python3
"""
🦖 Workflow API Endpoints for Restaceratops
Advanced API endpoints for workflow management and test case generation
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import asyncio
import logging
import time

from backend.core.services.workflow_manager import WorkflowManager, WorkflowStep
from backend.core.services.jira_integration import JiraIntegration, JiraConfig, JiraStory
from backend.core.services.test_generator import AdvancedTestGenerator, TestGenerationConfig, TestType
from backend.core.services.test_data_generator import SmartTestDataGenerator, DataCategory
from backend.core.services.test_execution_monitor import TestExecutionMonitor, ExecutionStatus
from backend.core.services.evaluation_engine import AdvancedEvaluationEngine, EvaluationConfig, TestExecutionResult
from backend.core.agents.enhanced_chat_interface import EnhancedRestaceratopsChat

log = logging.getLogger("restaceratops.workflow_api")

router = APIRouter(prefix="/api/workflow", tags=["workflow"])

# Request/Response Models
class ConnectivityRequest(BaseModel):
    application_url: str
    jira_config: Dict[str, str]

class UserStorySelectionRequest(BaseModel):
    selected_stories: List[str]
    filters: Optional[Dict[str, Any]] = None

class TestGenerationRequest(BaseModel):
    stories_per_test: int = 3
    include_negative_tests: bool = True
    include_edge_cases: bool = True
    include_performance_tests: bool = False
    include_security_tests: bool = False
    test_data_generation: bool = True
    complexity_distribution: Optional[Dict[str, float]] = None
    priority_distribution: Optional[Dict[str, float]] = None

class TestDataGenerationRequest(BaseModel):
    data_categories: List[str] = ["valid", "invalid", "boundary"]
    validation_enabled: bool = True
    template_override: Optional[Dict[str, Any]] = None

class TestExecutionRequest(BaseModel):
    test_cases: List[Dict[str, Any]]
    execution_mode: str = "parallel"  # parallel, sequential
    timeout: int = 300  # seconds
    monitor_enabled: bool = True

class EvaluationRequest(BaseModel):
    execution_results: Dict[str, Any]
    evaluation_criteria: Optional[Dict[str, Any]] = None

# Global instances
workflow_manager = WorkflowManager()
test_execution_monitor = TestExecutionMonitor()
evaluation_engine = AdvancedEvaluationEngine()

@router.post("/start")
async def start_workflow():
    """Start a new workflow session"""
    try:
        result = await workflow_manager.start_workflow()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        log.error(f"Failed to start workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_workflow_status():
    """Get current workflow status and progress"""
    try:
        summary = await workflow_manager.get_workflow_summary()
        current_step_info = await workflow_manager.get_current_step_info()
        
        return JSONResponse(content={
            "summary": summary,
            "current_step": current_step_info
        }, status_code=200)
    except Exception as e:
        log.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/connectivity")
async def execute_connectivity_step(request: ConnectivityRequest):
    """Execute the connectivity step"""
    try:
        step_data = {
            "application_url": request.application_url,
            "jira_config": request.jira_config
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        log.error(f"Connectivity step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/user-story-selection")
async def execute_user_story_selection_step(request: UserStorySelectionRequest):
    """Execute the user story selection step"""
    try:
        step_data = {
            "selected_stories": request.selected_stories,
            "filters": request.filters or {}
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        log.error(f"User story selection step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/review-validate")
async def execute_review_validate_step():
    """Execute the review and validate step"""
    try:
        # Get stories from previous step
        stories_data = workflow_manager.state.step_data.get("user_story_selection", {})
        selected_stories = stories_data.get("selected_stories", [])
        
        # Create Jira integration
        jira_config_data = workflow_manager.state.step_data.get("connectivity", {}).get("jira_config", {})
        jira_config = JiraConfig(**jira_config_data)
        
        async with JiraIntegration(jira_config) as jira:
            # Fetch stories from Jira
            stories = await jira.fetch_user_stories()
            
            # Filter selected stories
            selected_jira_stories = [s for s in stories if s.key in selected_stories]
            
            # Validate stories
            validation_results = await jira.validate_user_stories(selected_jira_stories)
            
            step_data = {
                "validation_results": {
                    "stories": [vars(story) for story in selected_jira_stories],
                    "validation": [vars(result) for result in validation_results]
                }
            }
            
            result = await workflow_manager.execute_current_step(step_data)
            return JSONResponse(content=result, status_code=200)
            
    except Exception as e:
        log.error(f"Review validate step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/generate-test-cases")
async def execute_generate_test_cases_step(request: TestGenerationRequest):
    """Execute the test case generation step using advanced AI-powered generator"""
    try:
        # Get validated stories from previous step
        validation_data = workflow_manager.state.step_data.get("review_validate", {})
        validation_results = validation_data.get("validation_results", {})
        
        # Filter valid stories
        valid_stories = []
        for story, validation in zip(validation_results.get("stories", []), validation_results.get("validation", [])):
            if validation.get("is_valid", False):
                valid_stories.append(story)
        
        # Initialize advanced test generator
        chat_interface = EnhancedRestaceratopsChat()
        await chat_interface.initialize()
        test_generator = AdvancedTestGenerator(chat_interface)
        
        # Configure test generation
        test_types = [TestType.POSITIVE]
        if request.include_negative_tests:
            test_types.append(TestType.NEGATIVE)
        if request.include_edge_cases:
            test_types.append(TestType.EDGE_CASE)
        if request.include_performance_tests:
            test_types.append(TestType.PERFORMANCE)
        if request.include_security_tests:
            test_types.append(TestType.SECURITY)
        
        config = TestGenerationConfig(
            test_types=test_types,
            max_tests_per_story=request.stories_per_test,
            include_negative_tests=request.include_negative_tests,
            include_edge_cases=request.include_edge_cases,
            include_performance_tests=request.include_performance_tests,
            include_security_tests=request.include_security_tests,
            complexity_distribution=request.complexity_distribution or {
                "low": 0.3,
                "medium": 0.5,
                "high": 0.2
            },
            priority_distribution=request.priority_distribution or {
                "critical": 0.1,
                "high": 0.3,
                "medium": 0.4,
                "low": 0.2
            }
        )
        
        # Generate test cases for each story
        all_test_cases = []
        for story in valid_stories:
            story_test_cases = await test_generator.generate_test_cases_for_story(story, config)
            all_test_cases.extend(story_test_cases)
        
        # Convert to dictionary format for API response
        test_cases_dict = []
        for test_case in all_test_cases:
            test_cases_dict.append({
                "id": test_case.id,
                "name": test_case.name,
                "description": test_case.description,
                "test_type": test_case.test_type.value,
                "priority": test_case.priority.value,
                "story_id": test_case.story_id,
                "prerequisites": test_case.prerequisites,
                "steps": test_case.steps,
                "test_data": test_case.test_data,
                "expected_results": test_case.expected_results,
                "assertions": test_case.assertions,
                "tags": test_case.tags,
                "estimated_duration": test_case.estimated_duration,
                "complexity": test_case.complexity,
                "risk_level": test_case.risk_level,
                "created_at": test_case.created_at.isoformat(),
                "metadata": test_case.metadata
            })
        
        step_data = {
            "test_cases": test_cases_dict,
            "generation_config": {
                "stories_per_test": request.stories_per_test,
                "include_negative_tests": request.include_negative_tests,
                "include_edge_cases": request.include_edge_cases,
                "include_performance_tests": request.include_performance_tests,
                "include_security_tests": request.include_security_tests,
                "complexity_distribution": config.complexity_distribution,
                "priority_distribution": config.priority_distribution
            },
            "generation_stats": test_generator.get_generation_stats()
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        log.error(f"Test case generation step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/generate-test-data")
async def execute_generate_test_data_step(request: TestDataGenerationRequest):
    """Execute the test data generation step using advanced smart data generator"""
    try:
        # Get test cases from previous step
        test_cases_data = workflow_manager.state.step_data.get("generate_test_cases", {})
        test_cases = test_cases_data.get("test_cases", [])
        
        # Initialize smart test data generator
        data_generator = SmartTestDataGenerator()
        
        # Convert data categories to enum values
        data_categories = []
        for category in request.data_categories:
            if category == "valid":
                data_categories.append(DataCategory.VALID)
            elif category == "invalid":
                data_categories.append(DataCategory.INVALID)
            elif category == "boundary":
                data_categories.append(DataCategory.BOUNDARY)
            elif category == "edge_case":
                data_categories.append(DataCategory.EDGE_CASE)
            elif category == "performance":
                data_categories.append(DataCategory.PERFORMANCE)
            elif category == "security":
                data_categories.append(DataCategory.SECURITY)
        
        # Generate test data for each test case and category
        generated_data_sets = {}
        for test_case in test_cases:
            test_case_id = test_case.get("id", "unknown")
            generated_data_sets[test_case_id] = {}
            
            for category in data_categories:
                try:
                    data_set = await data_generator.generate_test_data_for_case(
                        test_case, 
                        category
                    )
                    
                    generated_data_sets[test_case_id][category.value] = {
                        "id": data_set.id,
                        "name": data_set.name,
                        "description": data_set.description,
                        "data_category": data_set.data_category.value,
                        "generated_data": data_set.generated_data,
                        "validation_results": data_set.validation_results,
                        "metadata": data_set.metadata,
                        "created_at": data_set.created_at.isoformat()
                    }
                except Exception as e:
                    log.error(f"Failed to generate data for test case {test_case_id}, category {category.value}: {e}")
                    generated_data_sets[test_case_id][category.value] = {
                        "error": str(e),
                        "generated_data": {},
                        "validation_results": {}
                    }
        
        step_data = {
            "test_data": generated_data_sets,
            "generation_config": {
                "data_categories": request.data_categories,
                "validation_enabled": request.validation_enabled,
                "template_override": request.template_override
            },
            "generation_stats": data_generator.get_generation_stats()
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        log.error(f"Test data generation step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/execute-test")
async def execute_test_step(request: TestExecutionRequest):
    """Execute the test execution step with advanced monitoring"""
    try:
        # Get test data from previous step
        test_data = workflow_manager.state.step_data.get("generate_test_data", {}).get("test_data", {})
        
        # Start execution session if monitoring is enabled
        session_id = None
        if request.monitor_enabled:
            session_id = f"session_{int(time.time())}"
            await test_execution_monitor.start_session(
                session_id=session_id,
                name=f"Test Execution - {len(request.test_cases)} tests",
                description=f"Executing {len(request.test_cases)} test cases in {request.execution_mode} mode",
                configuration={
                    "execution_mode": request.execution_mode,
                    "timeout": request.timeout,
                    "test_count": len(request.test_cases)
                },
                tags=["workflow", "test_execution"]
            )
        
        # Execute tests with monitoring
        execution_results = await execute_test_cases_with_monitoring(
            request.test_cases,
            test_data,
            request.execution_mode,
            request.timeout,
            session_id
        )
        
        # End session if monitoring was enabled
        if session_id and request.monitor_enabled:
            final_status = ExecutionStatus.PASSED if execution_results.get("success_rate", 0) >= 80 else ExecutionStatus.FAILED
            await test_execution_monitor.end_session(session_id, final_status)
        
        step_data = {
            "execution_results": execution_results,
            "session_id": session_id
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        log.error(f"Test execution step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/step/evaluate-test-results")
async def execute_evaluate_test_results_step(request: EvaluationRequest):
    """Execute the test result evaluation step"""
    try:
        # Get execution results from previous step
        execution_results = workflow_manager.state.step_data.get("execute_test", {}).get("execution_results", {})
        
        # Evaluate results
        evaluation_results = await evaluate_test_results(
            execution_results,
            request.evaluation_criteria
        )
        
        step_data = {
            "evaluation_results": evaluation_results
        }
        
        result = await workflow_manager.execute_current_step(step_data)
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        log.error(f"Test result evaluation step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_workflow():
    """Reset the workflow to initial state"""
    try:
        result = await workflow_manager.reset_workflow()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        log.error(f"Failed to reset workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
async def generate_test_cases_for_story(
    story: Dict[str, Any], 
    cases_per_story: int,
    include_negative: bool,
    include_edge_cases: bool,
    chat_interface: EnhancedRestaceratopsChat
) -> List[Dict[str, Any]]:
    """Generate test cases for a specific user story"""
    
    prompt = f"""
    Generate {cases_per_story} comprehensive test cases for the following user story:
    
    Story ID: {story.get('key', 'Unknown')}
    Summary: {story.get('summary', '')}
    Description: {story.get('description', '')}
    Acceptance Criteria: {story.get('acceptance_criteria', [])}
    
    Requirements:
    - Include positive test cases
    - Include negative test cases: {include_negative}
    - Include edge cases: {include_edge_cases}
    - Each test case should have: description, steps, expected result, test data
    - Make test cases specific and measurable
    
    Return the test cases in JSON format.
    """
    
    try:
        response = await chat_interface.handle_message(prompt)
        # Parse response and extract test cases
        # This is a simplified version - in reality, you'd parse the AI response
        test_cases = [
            {
                "id": f"TC-{story.get('key', 'UNK')}-{i+1}",
                "story_id": story.get('key', 'Unknown'),
                "description": f"Test case {i+1} for {story.get('key', 'Unknown')}",
                "steps": [
                    "Step 1: Setup test environment",
                    "Step 2: Execute test scenario",
                    "Step 3: Verify results"
                ],
                "expected_result": "Expected outcome based on acceptance criteria",
                "test_data": {
                    "input_data": "Sample input data",
                    "expected_output": "Expected output data"
                },
                "type": "positive" if i == 0 else ("negative" if i == 1 else "edge_case")
            }
            for i in range(cases_per_story)
        ]
        
        return test_cases
        
    except Exception as e:
        log.error(f"Failed to generate test cases for story {story.get('key', 'Unknown')}: {e}")
        return []

async def generate_test_data_for_cases(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate test data for test cases"""
    test_data = {}
    
    for test_case in test_cases:
        test_case_id = test_case.get("id", "unknown")
        
        # Generate appropriate test data based on test case type
        if test_case.get("type") == "positive":
            test_data[test_case_id] = {
                "input_data": "Valid input data",
                "expected_output": "Expected successful output",
                "environment": "Normal conditions"
            }
        elif test_case.get("type") == "negative":
            test_data[test_case_id] = {
                "input_data": "Invalid input data",
                "expected_output": "Error message or failure response",
                "environment": "Error conditions"
            }
        else:  # edge_case
            test_data[test_case_id] = {
                "input_data": "Boundary or extreme input data",
                "expected_output": "Expected behavior at boundaries",
                "environment": "Edge conditions"
            }
    
    return test_data

async def execute_test_cases_with_monitoring(
    test_cases: List[Dict[str, Any]],
    test_data: Dict[str, Any],
    execution_mode: str,
    timeout: int,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute test cases"""
    results = {
        "total_tests": len(test_cases),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "execution_time": 0,
        "results": []
    }
    
    start_time = asyncio.get_event_loop().time()
    
    if execution_mode == "parallel":
        # Execute tests in parallel
        tasks = []
        for test_case in test_cases:
            task = execute_single_test_case(test_case, test_data.get(test_case.get("id", ""), {}))
            tasks.append(task)
        
        test_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in test_results:
            if isinstance(result, Exception):
                results["failed"] += 1
                results["results"].append({
                    "test_id": "unknown",
                    "status": "failed",
                    "error": str(result)
                })
            else:
                if result["status"] == "passed":
                    results["passed"] += 1
                elif result["status"] == "failed":
                    results["failed"] += 1
                else:
                    results["skipped"] += 1
                results["results"].append(result)
    else:
        # Execute tests sequentially
        for test_case in test_cases:
            result = await execute_single_test_case(test_case, test_data.get(test_case.get("id", ""), {}))
            if result["status"] == "passed":
                results["passed"] += 1
            elif result["status"] == "failed":
                results["failed"] += 1
            else:
                results["skipped"] += 1
            results["results"].append(result)
    
    results["execution_time"] = asyncio.get_event_loop().time() - start_time
    
    return results

async def execute_single_test_case(test_case: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single test case"""
    try:
        # Simulate test execution
        await asyncio.sleep(0.1)  # Simulate test execution time
        
        # Randomly determine test result (in real implementation, this would be actual test execution)
        import random
        status = random.choice(["passed", "failed", "skipped"])
        
        return {
            "test_id": test_case.get("id", "unknown"),
            "status": status,
            "execution_time": 0.1,
            "message": f"Test {status}",
            "details": {
                "steps_executed": len(test_case.get("steps", [])),
                "data_used": test_data
            }
        }
        
    except Exception as e:
        return {
            "test_id": test_case.get("id", "unknown"),
            "status": "failed",
            "error": str(e),
            "execution_time": 0
        }

async def evaluate_test_results(
    execution_results: Dict[str, Any],
    evaluation_criteria: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Evaluate test execution results"""
    
    total_tests = execution_results.get("total_tests", 0)
    passed_tests = execution_results.get("passed", 0)
    failed_tests = execution_results.get("failed", 0)
    skipped_tests = execution_results.get("skipped", 0)
    
    # Calculate metrics
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    fail_rate = (failed_tests / total_tests * 100) if total_tests > 0 else 0
    skip_rate = (skipped_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Determine overall status
    if pass_rate >= 90:
        overall_status = "excellent"
    elif pass_rate >= 80:
        overall_status = "good"
    elif pass_rate >= 70:
        overall_status = "fair"
    else:
        overall_status = "poor"
    
    evaluation = {
        "metrics": {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": skipped_tests,
            "pass_rate": round(pass_rate, 2),
            "fail_rate": round(fail_rate, 2),
            "skip_rate": round(skip_rate, 2),
            "execution_time": execution_results.get("execution_time", 0)
        },
        "overall_status": overall_status,
        "recommendations": generate_recommendations(pass_rate, failed_tests, execution_results),
        "detailed_results": execution_results.get("results", [])
    }
    
    return evaluation

def generate_recommendations(pass_rate: float, failed_tests: int, execution_results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on test results"""
    recommendations = []
    
    if pass_rate < 80:
        recommendations.append("Consider reviewing and improving test cases with low pass rates")
    
    if failed_tests > 0:
        recommendations.append("Investigate failed tests and fix underlying issues")
    
    if execution_results.get("execution_time", 0) > 60:
        recommendations.append("Consider optimizing test execution for better performance")
    
    if not recommendations:
        recommendations.append("Test execution completed successfully. Consider adding more test coverage for edge cases.")
    
    return recommendations 

# Phase 2: Advanced Test Generation and Monitoring Endpoints

@router.get("/test-generation/stats")
async def get_test_generation_stats():
    """Get test generation statistics"""
    try:
        # Get the latest test generation data
        test_cases_data = workflow_manager.state.step_data.get("generate_test_cases", {})
        generation_stats = test_cases_data.get("generation_stats", {})
        
        return JSONResponse(content=generation_stats, status_code=200)
    except Exception as e:
        log.error(f"Failed to get test generation stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-data/stats")
async def get_test_data_stats():
    """Get test data generation statistics"""
    try:
        # Get the latest test data generation data
        test_data_info = workflow_manager.state.step_data.get("generate_test_data", {})
        generation_stats = test_data_info.get("generation_stats", {})
        
        return JSONResponse(content=generation_stats, status_code=200)
    except Exception as e:
        log.error(f"Failed to get test data stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/sessions")
async def get_execution_sessions():
    """Get all test execution sessions"""
    try:
        active_sessions = test_execution_monitor.get_active_sessions()
        completed_sessions = test_execution_monitor.get_completed_sessions()
        
        return JSONResponse(content={
            "active_sessions": [
                {
                    "session_id": session.session_id,
                    "name": session.name,
                    "description": session.description,
                    "start_time": session.start_time.isoformat(),
                    "status": session.status.value,
                    "metrics": {
                        "total_tests": session.metrics.total_tests,
                        "passed_tests": session.metrics.passed_tests,
                        "failed_tests": session.metrics.failed_tests,
                        "success_rate": session.metrics.success_rate,
                        "performance_level": session.metrics.performance_level.value
                    }
                }
                for session in active_sessions
            ],
            "completed_sessions": [
                {
                    "session_id": session.session_id,
                    "name": session.name,
                    "description": session.description,
                    "start_time": session.start_time.isoformat(),
                    "end_time": session.end_time.isoformat() if session.end_time else None,
                    "status": session.status.value,
                    "duration": (session.end_time - session.start_time).total_seconds() if session.end_time else None,
                    "metrics": {
                        "total_tests": session.metrics.total_tests,
                        "passed_tests": session.metrics.passed_tests,
                        "failed_tests": session.metrics.failed_tests,
                        "success_rate": session.metrics.success_rate,
                        "performance_level": session.metrics.performance_level.value,
                        "bottlenecks": session.metrics.bottlenecks,
                        "recommendations": session.metrics.recommendations
                    }
                }
                for session in completed_sessions
            ]
        }, status_code=200)
    except Exception as e:
        log.error(f"Failed to get execution sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/session/{session_id}")
async def get_execution_session(session_id: str):
    """Get detailed information about a specific execution session"""
    try:
        session_summary = test_execution_monitor.get_session_summary(session_id)
        if not session_summary:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return JSONResponse(content=session_summary, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get execution session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/session/{session_id}/performance")
async def get_execution_performance_report(session_id: str):
    """Get detailed performance report for a session"""
    try:
        performance_report = test_execution_monitor.get_performance_report(session_id)
        if not performance_report:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return JSONResponse(content=performance_report, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Failed to get performance report for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/global-stats")
async def get_global_execution_stats():
    """Get global execution statistics across all sessions"""
    try:
        global_stats = test_execution_monitor.get_global_statistics()
        return JSONResponse(content=global_stats, status_code=200)
    except Exception as e:
        log.error(f"Failed to get global execution stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-generation/generate-custom")
async def generate_custom_test_cases(request: TestGenerationRequest):
    """Generate custom test cases outside of workflow"""
    try:
        # Initialize advanced test generator
        chat_interface = EnhancedRestaceratopsChat()
        await chat_interface.initialize()
        test_generator = AdvancedTestGenerator(chat_interface)
        
        # Configure test generation
        test_types = [TestType.POSITIVE]
        if request.include_negative_tests:
            test_types.append(TestType.NEGATIVE)
        if request.include_edge_cases:
            test_types.append(TestType.EDGE_CASE)
        if request.include_performance_tests:
            test_types.append(TestType.PERFORMANCE)
        if request.include_security_tests:
            test_types.append(TestType.SECURITY)
        
        config = TestGenerationConfig(
            test_types=test_types,
            max_tests_per_story=request.stories_per_test,
            include_negative_tests=request.include_negative_tests,
            include_edge_cases=request.include_edge_cases,
            include_performance_tests=request.include_performance_tests,
            include_security_tests=request.include_security_tests,
            complexity_distribution=request.complexity_distribution or {
                "low": 0.3,
                "medium": 0.5,
                "high": 0.2
            },
            priority_distribution=request.priority_distribution or {
                "critical": 0.1,
                "high": 0.3,
                "medium": 0.4,
                "low": 0.2
            }
        )
        
        # For custom generation, we need sample stories
        sample_stories = [
            {
                "key": "CUSTOM-001",
                "summary": "User authentication functionality",
                "description": "As a user, I want to authenticate with username and password",
                "acceptance_criteria": [
                    "User can enter valid credentials",
                    "System validates credentials",
                    "User is redirected to dashboard on success"
                ]
            }
        ]
        
        # Generate test cases
        all_test_cases = []
        for story in sample_stories:
            story_test_cases = await test_generator.generate_test_cases_for_story(story, config)
            all_test_cases.extend(story_test_cases)
        
        # Convert to dictionary format
        test_cases_dict = []
        for test_case in all_test_cases:
            test_cases_dict.append({
                "id": test_case.id,
                "name": test_case.name,
                "description": test_case.description,
                "test_type": test_case.test_type.value,
                "priority": test_case.priority.value,
                "story_id": test_case.story_id,
                "prerequisites": test_case.prerequisites,
                "steps": test_case.steps,
                "test_data": test_case.test_data,
                "expected_results": test_case.expected_results,
                "assertions": test_case.assertions,
                "tags": test_case.tags,
                "estimated_duration": test_case.estimated_duration,
                "complexity": test_case.complexity,
                "risk_level": test_case.risk_level,
                "created_at": test_case.created_at.isoformat(),
                "metadata": test_case.metadata
            })
        
        return JSONResponse(content={
            "test_cases": test_cases_dict,
            "generation_config": {
                "stories_per_test": request.stories_per_test,
                "include_negative_tests": request.include_negative_tests,
                "include_edge_cases": request.include_edge_cases,
                "include_performance_tests": request.include_performance_tests,
                "include_security_tests": request.include_security_tests,
                "complexity_distribution": config.complexity_distribution,
                "priority_distribution": config.priority_distribution
            },
            "generation_stats": test_generator.get_generation_stats()
        }, status_code=200)
        
    except Exception as e:
        log.error(f"Custom test generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-data/generate-custom")
async def generate_custom_test_data(request: TestDataGenerationRequest):
    """Generate custom test data outside of workflow"""
    try:
        # Initialize smart test data generator
        data_generator = SmartTestDataGenerator()
        
        # Sample test case for custom generation
        sample_test_case = {
            "id": "CUSTOM-TC-001",
            "name": "Sample Test Case",
            "description": "A sample test case for data generation",
            "test_data": {
                "username": "testuser",
                "email": "test@example.com",
                "age": 25
            },
            "steps": [
                "Enter username",
                "Enter email",
                "Enter age",
                "Submit form"
            ],
            "assertions": [
                {"type": "status_code", "value": 200},
                {"type": "response_contains", "value": "success"}
            ]
        }
        
        # Convert data categories to enum values
        data_categories = []
        for category in request.data_categories:
            if category == "valid":
                data_categories.append(DataCategory.VALID)
            elif category == "invalid":
                data_categories.append(DataCategory.INVALID)
            elif category == "boundary":
                data_categories.append(DataCategory.BOUNDARY)
            elif category == "edge_case":
                data_categories.append(DataCategory.EDGE_CASE)
            elif category == "performance":
                data_categories.append(DataCategory.PERFORMANCE)
            elif category == "security":
                data_categories.append(DataCategory.SECURITY)
        
        # Generate test data for each category
        generated_data_sets = {}
        for category in data_categories:
            try:
                data_set = await data_generator.generate_test_data_for_case(
                    sample_test_case, 
                    category
                )
                
                generated_data_sets[category.value] = {
                    "id": data_set.id,
                    "name": data_set.name,
                    "description": data_set.description,
                    "data_category": data_set.data_category.value,
                    "generated_data": data_set.generated_data,
                    "validation_results": data_set.validation_results,
                    "metadata": data_set.metadata,
                    "created_at": data_set.created_at.isoformat()
                }
            except Exception as e:
                log.error(f"Failed to generate data for category {category.value}: {e}")
                generated_data_sets[category.value] = {
                    "error": str(e),
                    "generated_data": {},
                    "validation_results": {}
                }
        
        return JSONResponse(content={
            "test_data": generated_data_sets,
            "generation_config": {
                "data_categories": request.data_categories,
                "validation_enabled": request.validation_enabled,
                "template_override": request.template_override
            },
            "generation_stats": data_generator.get_generation_stats()
        }, status_code=200)
         
    except Exception as e:
        log.error(f"Custom test data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Phase 3: Advanced Evaluation & Analytics Endpoints

@router.get("/evaluation/stats")
async def get_evaluation_stats():
    """Get evaluation statistics"""
    try:
        stats = evaluation_engine.get_evaluation_stats()
        return JSONResponse(content=stats, status_code=200)
    except Exception as e:
        log.error(f"Failed to get evaluation stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evaluation/results")
async def get_evaluation_results():
    """Get recent evaluation results"""
    try:
        # In a real implementation, this would fetch from a database
        # For now, return mock data
        mock_results = [
            {
                "test_id": "TC-001",
                "test_name": "User Authentication Test",
                "evaluation_metrics": {
                    "precision": 0.95,
                    "recall": 0.92,
                    "f1_score": 0.93,
                    "accuracy": 0.94,
                    "completeness": 0.88,
                    "consistency": 0.91
                },
                "evaluation_level": "excellent",
                "confidence_score": 0.92,
                "recommendations": [
                    "Consider adding more edge case scenarios",
                    "Enhance error handling validation"
                ]
            },
            {
                "test_id": "TC-002",
                "test_name": "Data Validation Test",
                "evaluation_metrics": {
                    "precision": 0.87,
                    "recall": 0.85,
                    "f1_score": 0.86,
                    "accuracy": 0.88,
                    "completeness": 0.82,
                    "consistency": 0.89
                },
                "evaluation_level": "good",
                "confidence_score": 0.85,
                "recommendations": [
                    "Improve boundary value testing",
                    "Add more comprehensive data validation checks"
                ]
            }
        ]
        
        return JSONResponse(content={"results": mock_results}, status_code=200)
    except Exception as e:
        log.error(f"Failed to get evaluation results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluation/evaluate")
async def evaluate_test_results(request: EvaluationRequest):
    """Evaluate test execution results"""
    try:
        # Convert execution results to TestExecutionResult objects
        execution_results = []
        for result in request.execution_results.get("results", []):
            execution_result = TestExecutionResult(
                test_id=result.get("test_id", "unknown"),
                test_name=result.get("test_name", "Unknown Test"),
                status=result.get("status", "unknown"),
                execution_time=result.get("execution_time", 0.0),
                response_time=result.get("response_time", 0.0),
                actual_results=result.get("actual_results", {}),
                expected_results=result.get("expected_results", {}),
                assertions=result.get("assertions", []),
                error_message=result.get("error_message"),
                metadata=result.get("metadata", {})
            )
            execution_results.append(execution_result)
        
        # Configure evaluation
        config = EvaluationConfig(
            enable_context_analysis=request.evaluation_criteria.get("enable_context_analysis", True),
            enable_hallucination_detection=request.evaluation_criteria.get("enable_hallucination_detection", True),
            enable_faithfulness_evaluation=request.evaluation_criteria.get("enable_faithfulness_evaluation", True),
            enable_completeness_check=request.evaluation_criteria.get("enable_completeness_check", True),
            enable_consistency_check=request.evaluation_criteria.get("enable_consistency_check", True)
        )
        
        # Evaluate results
        evaluation_results = await evaluation_engine.evaluate_test_results(execution_results, config)
        
        # Convert to dictionary format
        results_dict = []
        for evaluation in evaluation_results:
            results_dict.append({
                "test_id": evaluation.test_id,
                "test_name": evaluation.test_name,
                "evaluation_metrics": evaluation.evaluation_metrics,
                "evaluation_level": evaluation.evaluation_level.value,
                "context_analysis": evaluation.context_analysis,
                "hallucination_detection": evaluation.hallucination_detection,
                "faithfulness_evaluation": evaluation.faithfulness_evaluation,
                "recommendations": evaluation.recommendations,
                "confidence_score": evaluation.confidence_score,
                "evaluation_timestamp": evaluation.evaluation_timestamp.isoformat()
            })
        
        return JSONResponse(content={
            "evaluation_results": results_dict,
            "evaluation_config": {
                "enable_context_analysis": config.enable_context_analysis,
                "enable_hallucination_detection": config.enable_hallucination_detection,
                "enable_faithfulness_evaluation": config.enable_faithfulness_evaluation,
                "enable_completeness_check": config.enable_completeness_check,
                "enable_consistency_check": config.enable_consistency_check
            },
            "evaluation_stats": evaluation_engine.get_evaluation_stats()
        }, status_code=200)
        
    except Exception as e:
        log.error(f"Evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 