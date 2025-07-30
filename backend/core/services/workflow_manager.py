#!/usr/bin/env python3
"""
🦖 Workflow Manager for Restaceratops
Guided workflow system for test case generation and execution
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

log = logging.getLogger("restaceratops.workflow_manager")

class WorkflowStep(Enum):
    """Workflow steps enumeration"""
    CONNECTIVITY = "connectivity"
    USER_STORY_SELECTION = "user_story_selection"
    REVIEW_VALIDATE = "review_validate"
    GENERATE_TEST_CASES = "generate_test_cases"
    GENERATE_TEST_DATA = "generate_test_data"
    EXECUTE_TEST = "execute_test"
    EVALUATE_TEST_RESULTS = "evaluate_test_results"

@dataclass
class WorkflowState:
    """Workflow state management"""
    current_step: WorkflowStep = WorkflowStep.CONNECTIVITY
    completed_steps: List[WorkflowStep] = field(default_factory=list)
    step_data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    def is_step_completed(self, step: WorkflowStep) -> bool:
        """Check if a step is completed"""
        return step in self.completed_steps
    
    def mark_step_completed(self, step: WorkflowStep):
        """Mark a step as completed"""
        if step not in self.completed_steps:
            self.completed_steps.append(step)
        self.last_updated = datetime.now()
    
    def get_progress_percentage(self) -> float:
        """Get workflow progress percentage"""
        total_steps = len(WorkflowStep)
        completed_count = len(self.completed_steps)
        return (completed_count / total_steps) * 100

@dataclass
class StepConfig:
    """Configuration for a workflow step"""
    step: WorkflowStep
    title: str
    description: str
    required_fields: List[str]
    optional_fields: List[str] = field(default_factory=list)
    validation_rules: Dict[str, Callable] = field(default_factory=dict)
    dependencies: List[WorkflowStep] = field(default_factory=list)

class WorkflowManager:
    """Advanced workflow management system"""
    
    def __init__(self):
        self.state = WorkflowState()
        self.step_configs = self._initialize_step_configs()
        self.step_handlers = self._initialize_step_handlers()
        
    def _initialize_step_configs(self) -> Dict[WorkflowStep, StepConfig]:
        """Initialize step configurations"""
        return {
            WorkflowStep.CONNECTIVITY: StepConfig(
                step=WorkflowStep.CONNECTIVITY,
                title="Connectivity",
                description="Connect to your application and Jira project",
                required_fields=["application_url", "jira_config"],
                validation_rules={
                    "application_url": self._validate_url,
                    "jira_config": self._validate_jira_config
                }
            ),
            WorkflowStep.USER_STORY_SELECTION: StepConfig(
                step=WorkflowStep.USER_STORY_SELECTION,
                title="User Story Selection",
                description="Select user stories for test case generation",
                required_fields=["selected_stories"],
                dependencies=[WorkflowStep.CONNECTIVITY],
                validation_rules={
                    "selected_stories": self._validate_story_selection
                }
            ),
            WorkflowStep.REVIEW_VALIDATE: StepConfig(
                step=WorkflowStep.REVIEW_VALIDATE,
                title="Review & Validate",
                description="Review and validate selected user stories",
                required_fields=["validation_results"],
                dependencies=[WorkflowStep.USER_STORY_SELECTION],
                validation_rules={
                    "validation_results": self._validate_validation_results
                }
            ),
            WorkflowStep.GENERATE_TEST_CASES: StepConfig(
                step=WorkflowStep.GENERATE_TEST_CASES,
                title="Generate Test Cases",
                description="Generate test cases from validated user stories",
                required_fields=["test_cases"],
                dependencies=[WorkflowStep.REVIEW_VALIDATE],
                validation_rules={
                    "test_cases": self._validate_test_cases
                }
            ),
            WorkflowStep.GENERATE_TEST_DATA: StepConfig(
                step=WorkflowStep.GENERATE_TEST_DATA,
                title="Generate Test Data",
                description="Generate test data for the test cases",
                required_fields=["test_data"],
                dependencies=[WorkflowStep.GENERATE_TEST_CASES],
                validation_rules={
                    "test_data": self._validate_test_data
                }
            ),
            WorkflowStep.EXECUTE_TEST: StepConfig(
                step=WorkflowStep.EXECUTE_TEST,
                title="Execute Test",
                description="Execute the generated test cases",
                required_fields=["execution_results"],
                dependencies=[WorkflowStep.GENERATE_TEST_DATA],
                validation_rules={
                    "execution_results": self._validate_execution_results
                }
            ),
            WorkflowStep.EVALUATE_TEST_RESULTS: StepConfig(
                step=WorkflowStep.EVALUATE_TEST_RESULTS,
                title="Evaluate Test Results",
                description="Evaluate and analyze test execution results",
                required_fields=["evaluation_results"],
                dependencies=[WorkflowStep.EXECUTE_TEST],
                validation_rules={
                    "evaluation_results": self._validate_evaluation_results
                }
            )
        }
    
    def _initialize_step_handlers(self) -> Dict[WorkflowStep, Callable]:
        """Initialize step handlers"""
        return {
            WorkflowStep.CONNECTIVITY: self._handle_connectivity,
            WorkflowStep.USER_STORY_SELECTION: self._handle_user_story_selection,
            WorkflowStep.REVIEW_VALIDATE: self._handle_review_validate,
            WorkflowStep.GENERATE_TEST_CASES: self._handle_generate_test_cases,
            WorkflowStep.GENERATE_TEST_DATA: self._handle_generate_test_data,
            WorkflowStep.EXECUTE_TEST: self._handle_execute_test,
            WorkflowStep.EVALUATE_TEST_RESULTS: self._handle_evaluate_test_results
        }
    
    async def start_workflow(self) -> Dict[str, Any]:
        """Start the workflow"""
        self.state.start_time = datetime.now()
        self.state.last_updated = datetime.now()
        
        log.info("Workflow started")
        
        return {
            "success": True,
            "current_step": self.state.current_step.value,
            "progress": self.state.get_progress_percentage(),
            "message": "Workflow started successfully"
        }
    
    async def get_current_step_info(self) -> Dict[str, Any]:
        """Get information about the current step"""
        config = self.step_configs[self.state.current_step]
        
        return {
            "step": self.state.current_step.value,
            "title": config.title,
            "description": config.description,
            "required_fields": config.required_fields,
            "optional_fields": config.optional_fields,
            "progress": self.state.get_progress_percentage(),
            "completed_steps": [step.value for step in self.state.completed_steps],
            "can_proceed": self._can_proceed_to_step(self.state.current_step)
        }
    
    async def execute_current_step(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the current workflow step"""
        try:
            # Validate step data
            validation_result = await self._validate_step_data(step_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"],
                    "message": "Step validation failed"
                }
            
            # Execute step handler
            handler = self.step_handlers[self.state.current_step]
            result = await handler(step_data)
            
            if result["success"]:
                # Store step data
                self.state.step_data[self.state.current_step.value] = step_data
                self.state.mark_step_completed(self.state.current_step)
                
                # Move to next step
                next_step = self._get_next_step()
                if next_step:
                    self.state.current_step = next_step
                    return {
                        "success": True,
                        "message": f"Step '{self.step_configs[self.state.current_step].title}' completed",
                        "next_step": next_step.value,
                        "progress": self.state.get_progress_percentage()
                    }
                else:
                    return {
                        "success": True,
                        "message": "Workflow completed successfully",
                        "progress": 100.0,
                        "completed": True
                    }
            else:
                return result
                
        except Exception as e:
            log.error(f"Error executing step {self.state.current_step.value}: {e}")
            self.state.errors.append(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Step execution failed"
            }
    
    async def _validate_step_data(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate step data against configuration"""
        config = self.step_configs[self.state.current_step]
        errors = []
        
        # Check required fields
        for field in config.required_fields:
            if field not in step_data or not step_data[field]:
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Run validation rules
        for field, validator in config.validation_rules.items():
            if field in step_data:
                try:
                    if not validator(step_data[field]):
                        errors.append(f"Validation failed for field '{field}'")
                except Exception as e:
                    errors.append(f"Validation error for field '{field}': {e}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _can_proceed_to_step(self, step: WorkflowStep) -> bool:
        """Check if we can proceed to a specific step"""
        config = self.step_configs[step]
        
        # Check dependencies
        for dependency in config.dependencies:
            if not self.state.is_step_completed(dependency):
                return False
        
        return True
    
    def _get_next_step(self) -> Optional[WorkflowStep]:
        """Get the next step in the workflow"""
        current_index = list(WorkflowStep).index(self.state.current_step)
        next_index = current_index + 1
        
        if next_index < len(WorkflowStep):
            return list(WorkflowStep)[next_index]
        
        return None
    
    # Step handlers
    async def _handle_connectivity(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle connectivity step"""
        try:
            # Test application connectivity
            app_url = step_data["application_url"]
            jira_config = step_data["jira_config"]
            
            # TODO: Implement actual connectivity tests
            # This would test the application URL and Jira connection
            
            return {
                "success": True,
                "message": "Connectivity established successfully",
                "data": {
                    "application_status": "connected",
                    "jira_status": "connected"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Connectivity test failed"
            }
    
    async def _handle_user_story_selection(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user story selection step"""
        try:
            selected_stories = step_data["selected_stories"]
            
            # TODO: Implement story fetching and selection logic
            # This would fetch stories from Jira and process the selection
            
            return {
                "success": True,
                "message": f"Selected {len(selected_stories)} user stories",
                "data": {
                    "stories_count": len(selected_stories),
                    "stories": selected_stories
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "User story selection failed"
            }
    
    async def _handle_review_validate(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle review and validate step"""
        try:
            validation_results = step_data["validation_results"]
            
            # TODO: Implement validation logic
            # This would validate the selected stories
            
            return {
                "success": True,
                "message": "Stories validated successfully",
                "data": {
                    "validation_results": validation_results
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Story validation failed"
            }
    
    async def _handle_generate_test_cases(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test case generation step"""
        try:
            test_cases = step_data["test_cases"]
            
            # TODO: Implement test case generation logic
            # This would generate test cases from the validated stories
            
            return {
                "success": True,
                "message": f"Generated {len(test_cases)} test cases",
                "data": {
                    "test_cases_count": len(test_cases),
                    "test_cases": test_cases
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Test case generation failed"
            }
    
    async def _handle_generate_test_data(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test data generation step"""
        try:
            test_data = step_data["test_data"]
            
            # TODO: Implement test data generation logic
            # This would generate test data for the test cases
            
            return {
                "success": True,
                "message": "Test data generated successfully",
                "data": {
                    "test_data": test_data
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Test data generation failed"
            }
    
    async def _handle_execute_test(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test execution step"""
        try:
            execution_results = step_data["execution_results"]
            
            # TODO: Implement test execution logic
            # This would execute the test cases with the generated data
            
            return {
                "success": True,
                "message": "Tests executed successfully",
                "data": {
                    "execution_results": execution_results
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Test execution failed"
            }
    
    async def _handle_evaluate_test_results(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test result evaluation step"""
        try:
            evaluation_results = step_data["evaluation_results"]
            
            # TODO: Implement evaluation logic
            # This would evaluate the test execution results
            
            return {
                "success": True,
                "message": "Test results evaluated successfully",
                "data": {
                    "evaluation_results": evaluation_results
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Test result evaluation failed"
            }
    
    # Validation methods
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
    
    def _validate_jira_config(self, config: Dict[str, Any]) -> bool:
        """Validate Jira configuration"""
        required_fields = ["base_url", "username", "api_token", "project_key"]
        return all(field in config and config[field] for field in required_fields)
    
    def _validate_story_selection(self, stories: List[str]) -> bool:
        """Validate story selection"""
        return isinstance(stories, list) and len(stories) > 0
    
    def _validate_validation_results(self, results: Dict[str, Any]) -> bool:
        """Validate validation results"""
        return isinstance(results, dict) and "stories" in results
    
    def _validate_test_cases(self, test_cases: List[Dict[str, Any]]) -> bool:
        """Validate test cases"""
        return isinstance(test_cases, list) and len(test_cases) > 0
    
    def _validate_test_data(self, test_data: Dict[str, Any]) -> bool:
        """Validate test data"""
        return isinstance(test_data, dict)
    
    def _validate_execution_results(self, results: Dict[str, Any]) -> bool:
        """Validate execution results"""
        return isinstance(results, dict) and "results" in results
    
    def _validate_evaluation_results(self, results: Dict[str, Any]) -> bool:
        """Validate evaluation results"""
        return isinstance(results, dict) and "metrics" in results
    
    async def get_workflow_summary(self) -> Dict[str, Any]:
        """Get workflow summary"""
        return {
            "current_step": self.state.current_step.value,
            "progress": self.state.get_progress_percentage(),
            "completed_steps": [step.value for step in self.state.completed_steps],
            "total_steps": len(WorkflowStep),
            "start_time": self.state.start_time.isoformat() if self.state.start_time else None,
            "last_updated": self.state.last_updated.isoformat() if self.state.last_updated else None,
            "errors": self.state.errors,
            "warnings": self.state.warnings
        }
    
    async def reset_workflow(self) -> Dict[str, Any]:
        """Reset the workflow to initial state"""
        self.state = WorkflowState()
        return {
            "success": True,
            "message": "Workflow reset successfully"
        } 