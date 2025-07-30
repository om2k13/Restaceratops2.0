#!/usr/bin/env python3
"""
🦖 Advanced Test Case Generator for Restaceratops
AI-powered test case generation with multiple test types and intelligent analysis
"""

import asyncio
import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import openai
from pydantic import BaseModel

from backend.core.agents.enhanced_chat_interface import EnhancedRestaceratopsChat

log = logging.getLogger("restaceratops.test_generator")

class TestType(Enum):
    """Test case types"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    EDGE_CASE = "edge_case"
    BOUNDARY = "boundary"
    PERFORMANCE = "performance"
    SECURITY = "security"
    INTEGRATION = "integration"
    REGRESSION = "regression"

class TestPriority(Enum):
    """Test priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class TestCase:
    """Generated test case structure"""
    id: str
    name: str
    description: str
    test_type: TestType
    priority: TestPriority
    story_id: str
    prerequisites: List[str]
    steps: List[str]
    test_data: Dict[str, Any]
    expected_results: List[str]
    assertions: List[Dict[str, Any]]
    tags: List[str]
    estimated_duration: int  # seconds
    complexity: str  # low, medium, high
    risk_level: str  # low, medium, high
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestGenerationConfig:
    """Configuration for test generation"""
    test_types: List[TestType]
    max_tests_per_story: int = 5
    include_negative_tests: bool = True
    include_edge_cases: bool = True
    include_performance_tests: bool = False
    include_security_tests: bool = False
    complexity_distribution: Dict[str, float] = field(default_factory=lambda: {
        "low": 0.3,
        "medium": 0.5,
        "high": 0.2
    })
    priority_distribution: Dict[str, float] = field(default_factory=lambda: {
        "critical": 0.1,
        "high": 0.3,
        "medium": 0.4,
        "low": 0.2
    })

class AdvancedTestGenerator:
    """Advanced AI-powered test case generator"""
    
    def __init__(self, chat_interface: EnhancedRestaceratopsChat):
        self.chat_interface = chat_interface
        self.test_templates = self._load_test_templates()
        self.generation_history: List[Dict[str, Any]] = []
        
    def _load_test_templates(self) -> Dict[str, str]:
        """Load test case templates for different test types"""
        return {
            "positive": """
            Test Case: {test_name}
            Type: Positive Test
            Priority: {priority}
            Description: {description}
            
            Prerequisites:
            {prerequisites}
            
            Test Steps:
            {steps}
            
            Test Data:
            {test_data}
            
            Expected Results:
            {expected_results}
            
            Assertions:
            {assertions}
            """,
            
            "negative": """
            Test Case: {test_name}
            Type: Negative Test
            Priority: {priority}
            Description: {description}
            
            Prerequisites:
            {prerequisites}
            
            Test Steps:
            {steps}
            
            Test Data (Invalid):
            {test_data}
            
            Expected Results (Error Handling):
            {expected_results}
            
            Assertions:
            {assertions}
            """,
            
            "edge_case": """
            Test Case: {test_name}
            Type: Edge Case Test
            Priority: {priority}
            Description: {description}
            
            Prerequisites:
            {prerequisites}
            
            Test Steps:
            {steps}
            
            Test Data (Boundary Values):
            {test_data}
            
            Expected Results:
            {expected_results}
            
            Assertions:
            {assertions}
            """,
            
            "performance": """
            Test Case: {test_name}
            Type: Performance Test
            Priority: {priority}
            Description: {description}
            
            Prerequisites:
            {prerequisites}
            
            Test Steps:
            {steps}
            
            Test Data (Load Data):
            {test_data}
            
            Expected Results (Performance Metrics):
            {expected_results}
            
            Assertions:
            {assertions}
            """
        }
    
    async def generate_test_cases_for_story(
        self, 
        story: Dict[str, Any], 
        config: TestGenerationConfig
    ) -> List[TestCase]:
        """Generate comprehensive test cases for a user story"""
        
        log.info(f"Generating test cases for story: {story.get('key', 'Unknown')}")
        
        test_cases = []
        story_id = story.get('key', 'UNKNOWN')
        
        # Analyze story for test generation insights
        analysis = await self._analyze_story_for_testing(story)
        
        # Generate different types of test cases
        for test_type in config.test_types:
            if test_type == TestType.POSITIVE:
                positive_tests = await self._generate_positive_tests(story, analysis, config)
                test_cases.extend(positive_tests)
            
            elif test_type == TestType.NEGATIVE and config.include_negative_tests:
                negative_tests = await self._generate_negative_tests(story, analysis, config)
                test_cases.extend(negative_tests)
            
            elif test_type == TestType.EDGE_CASE and config.include_edge_cases:
                edge_tests = await self._generate_edge_case_tests(story, analysis, config)
                test_cases.extend(edge_tests)
            
            elif test_type == TestType.PERFORMANCE and config.include_performance_tests:
                performance_tests = await self._generate_performance_tests(story, analysis, config)
                test_cases.extend(performance_tests)
            
            elif test_type == TestType.SECURITY and config.include_security_tests:
                security_tests = await self._generate_security_tests(story, analysis, config)
                test_cases.extend(security_tests)
        
        # Limit total tests per story
        if len(test_cases) > config.max_tests_per_story:
            test_cases = test_cases[:config.max_tests_per_story]
        
        # Assign IDs and metadata
        for i, test_case in enumerate(test_cases):
            test_case.id = f"TC-{story_id}-{i+1:03d}"
            test_case.story_id = story_id
            test_case.created_at = datetime.now()
        
        # Log generation
        self.generation_history.append({
            "story_id": story_id,
            "generated_tests": len(test_cases),
            "test_types": [tc.test_type.value for tc in test_cases],
            "timestamp": datetime.now().isoformat()
        })
        
        log.info(f"Generated {len(test_cases)} test cases for story {story_id}")
        return test_cases
    
    async def _analyze_story_for_testing(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user story to extract testing insights"""
        
        prompt = f"""
        Analyze the following user story for test case generation:
        
        Story ID: {story.get('key', 'Unknown')}
        Summary: {story.get('summary', '')}
        Description: {story.get('description', '')}
        Acceptance Criteria: {story.get('acceptance_criteria', [])}
        
        Provide a JSON analysis with the following structure:
        {{
            "functional_areas": ["list of functional areas to test"],
            "data_requirements": ["list of data types and requirements"],
            "user_interactions": ["list of user interactions"],
            "business_rules": ["list of business rules"],
            "error_scenarios": ["list of potential error scenarios"],
            "performance_considerations": ["list of performance aspects"],
            "security_considerations": ["list of security aspects"],
            "integration_points": ["list of integration points"],
            "complexity_level": "low|medium|high",
            "risk_areas": ["list of high-risk areas"]
        }}
        
        Focus on identifying testable aspects and potential failure points.
        """
        
        try:
            response = await self.chat_interface.handle_message(prompt)
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            else:
                # Fallback analysis
                return self._create_fallback_analysis(story)
                
        except Exception as e:
            log.error(f"Failed to analyze story: {e}")
            return self._create_fallback_analysis(story)
    
    def _create_fallback_analysis(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback analysis when AI analysis fails"""
        summary = story.get('summary', '').lower()
        description = story.get('description', '').lower()
        
        analysis = {
            "functional_areas": ["user_interface", "data_processing", "validation"],
            "data_requirements": ["input_data", "output_data"],
            "user_interactions": ["user_input", "system_response"],
            "business_rules": ["validation_rules", "business_logic"],
            "error_scenarios": ["invalid_input", "system_error", "timeout"],
            "performance_considerations": ["response_time", "throughput"],
            "security_considerations": ["input_validation", "authentication"],
            "integration_points": ["api_endpoints", "database"],
            "complexity_level": "medium",
            "risk_areas": ["data_validation", "error_handling"]
        }
        
        # Enhance based on story content
        if any(word in summary for word in ["create", "add", "insert"]):
            analysis["functional_areas"].append("data_creation")
        if any(word in summary for word in ["update", "modify", "edit"]):
            analysis["functional_areas"].append("data_modification")
        if any(word in summary for word in ["delete", "remove"]):
            analysis["functional_areas"].append("data_deletion")
        if any(word in summary for word in ["search", "find", "query"]):
            analysis["functional_areas"].append("data_retrieval")
        
        return analysis
    
    async def _generate_positive_tests(self, story: Dict[str, Any], analysis: Dict[str, Any], config: TestGenerationConfig) -> List[TestCase]:
        """Generate positive test cases"""
        
        prompt = f"""
        Generate 2-3 positive test cases for the following user story:
        
        Story: {story.get('summary', '')}
        Description: {story.get('description', '')}
        Acceptance Criteria: {story.get('acceptance_criteria', [])}
        
        Analysis: {json.dumps(analysis, indent=2)}
        
        For each test case, provide:
        1. Test name (descriptive)
        2. Description (what is being tested)
        3. Prerequisites (what needs to be set up)
        4. Test steps (detailed steps)
        5. Test data (valid input data)
        6. Expected results (what should happen)
        7. Assertions (specific checks)
        
        Return as JSON array with this structure:
        [
            {{
                "name": "Test Name",
                "description": "Test description",
                "prerequisites": ["prereq1", "prereq2"],
                "steps": ["step1", "step2", "step3"],
                "test_data": {{"field1": "value1"}},
                "expected_results": ["result1", "result2"],
                "assertions": [
                    {{"type": "status_code", "value": 200}},
                    {{"type": "response_contains", "value": "expected_text"}}
                ]
            }}
        ]
        
        Focus on happy path scenarios and valid user interactions.
        """
        
        try:
            response = await self.chat_interface.handle_message(prompt)
            test_data = self._parse_test_generation_response(response)
            
            test_cases = []
            for i, test in enumerate(test_data):
                test_case = TestCase(
                    id=f"TEMP-{i}",
                    name=test.get("name", f"Positive Test {i+1}"),
                    description=test.get("description", ""),
                    test_type=TestType.POSITIVE,
                    priority=self._assign_priority(config.priority_distribution),
                    story_id=story.get("key", "UNKNOWN"),
                    prerequisites=test.get("prerequisites", []),
                    steps=test.get("steps", []),
                    test_data=test.get("test_data", {}),
                    expected_results=test.get("expected_results", []),
                    assertions=test.get("assertions", []),
                    tags=["positive", "happy-path"],
                    estimated_duration=60,
                    complexity="medium",
                    risk_level="low",
                    created_at=datetime.now()
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            log.error(f"Failed to generate positive tests: {e}")
            return self._create_fallback_positive_tests(story)
    
    async def _generate_negative_tests(self, story: Dict[str, Any], analysis: Dict[str, Any], config: TestGenerationConfig) -> List[TestCase]:
        """Generate negative test cases"""
        
        prompt = f"""
        Generate 2-3 negative test cases for the following user story:
        
        Story: {story.get('summary', '')}
        Description: {story.get('description', '')}
        Acceptance Criteria: {story.get('acceptance_criteria', [])}
        
        Analysis: {json.dumps(analysis, indent=2)}
        
        Focus on:
        - Invalid input data
        - Error conditions
        - Boundary violations
        - Missing required fields
        - Invalid formats
        
        For each test case, provide:
        1. Test name (descriptive)
        2. Description (what error condition is being tested)
        3. Prerequisites (what needs to be set up)
        4. Test steps (detailed steps)
        5. Test data (invalid input data)
        6. Expected results (error messages/behavior)
        7. Assertions (error checks)
        
        Return as JSON array with this structure:
        [
            {{
                "name": "Test Name",
                "description": "Test description",
                "prerequisites": ["prereq1", "prereq2"],
                "steps": ["step1", "step2", "step3"],
                "test_data": {{"field1": "invalid_value"}},
                "expected_results": ["error1", "error2"],
                "assertions": [
                    {{"type": "status_code", "value": 400}},
                    {{"type": "error_message_contains", "value": "error_text"}}
                ]
            }}
        ]
        """
        
        try:
            response = await self.chat_interface.handle_message(prompt)
            test_data = self._parse_test_generation_response(response)
            
            test_cases = []
            for i, test in enumerate(test_data):
                test_case = TestCase(
                    id=f"TEMP-{i}",
                    name=test.get("name", f"Negative Test {i+1}"),
                    description=test.get("description", ""),
                    test_type=TestType.NEGATIVE,
                    priority=self._assign_priority(config.priority_distribution),
                    story_id=story.get("key", "UNKNOWN"),
                    prerequisites=test.get("prerequisites", []),
                    steps=test.get("steps", []),
                    test_data=test.get("test_data", {}),
                    expected_results=test.get("expected_results", []),
                    assertions=test.get("assertions", []),
                    tags=["negative", "error-handling"],
                    estimated_duration=45,
                    complexity="medium",
                    risk_level="medium",
                    created_at=datetime.now()
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            log.error(f"Failed to generate negative tests: {e}")
            return self._create_fallback_negative_tests(story)
    
    async def _generate_edge_case_tests(self, story: Dict[str, Any], analysis: Dict[str, Any], config: TestGenerationConfig) -> List[TestCase]:
        """Generate edge case test cases"""
        
        prompt = f"""
        Generate 1-2 edge case test cases for the following user story:
        
        Story: {story.get('summary', '')}
        Description: {story.get('description', '')}
        Acceptance Criteria: {story.get('acceptance_criteria', [])}
        
        Analysis: {json.dumps(analysis, indent=2)}
        
        Focus on:
        - Boundary values (min, max, null, empty)
        - Extreme data scenarios
        - Unusual user interactions
        - System limits and constraints
        - Edge conditions that might break the system
        
        For each test case, provide:
        1. Test name (descriptive)
        2. Description (what edge case is being tested)
        3. Prerequisites (what needs to be set up)
        4. Test steps (detailed steps)
        5. Test data (edge case data)
        6. Expected results (expected behavior)
        7. Assertions (edge case checks)
        
        Return as JSON array with this structure:
        [
            {{
                "name": "Test Name",
                "description": "Test description",
                "prerequisites": ["prereq1", "prereq2"],
                "steps": ["step1", "step2", "step3"],
                "test_data": {{"field1": "edge_value"}},
                "expected_results": ["result1", "result2"],
                "assertions": [
                    {{"type": "status_code", "value": 200}},
                    {{"type": "response_validation", "value": "expected_behavior"}}
                ]
            }}
        ]
        """
        
        try:
            response = await self.chat_interface.handle_message(prompt)
            test_data = self._parse_test_generation_response(response)
            
            test_cases = []
            for i, test in enumerate(test_data):
                test_case = TestCase(
                    id=f"TEMP-{i}",
                    name=test.get("name", f"Edge Case Test {i+1}"),
                    description=test.get("description", ""),
                    test_type=TestType.EDGE_CASE,
                    priority=self._assign_priority(config.priority_distribution),
                    story_id=story.get("key", "UNKNOWN"),
                    prerequisites=test.get("prerequisites", []),
                    steps=test.get("steps", []),
                    test_data=test.get("test_data", {}),
                    expected_results=test.get("expected_results", []),
                    assertions=test.get("assertions", []),
                    tags=["edge-case", "boundary"],
                    estimated_duration=90,
                    complexity="high",
                    risk_level="high",
                    created_at=datetime.now()
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            log.error(f"Failed to generate edge case tests: {e}")
            return self._create_fallback_edge_case_tests(story)
    
    async def _generate_performance_tests(self, story: Dict[str, Any], analysis: Dict[str, Any], config: TestGenerationConfig) -> List[TestCase]:
        """Generate performance test cases"""
        # Implementation for performance tests
        return []
    
    async def _generate_security_tests(self, story: Dict[str, Any], analysis: Dict[str, Any], config: TestGenerationConfig) -> List[TestCase]:
        """Generate security test cases"""
        # Implementation for security tests
        return []
    
    def _parse_test_generation_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse AI response to extract test case data"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Try to find JSON object
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return [json.loads(json_match.group())]
                else:
                    log.warning("Could not parse JSON from AI response")
                    return []
        except json.JSONDecodeError as e:
            log.error(f"Failed to parse JSON from response: {e}")
            return []
    
    def _assign_priority(self, distribution: Dict[str, float]) -> TestPriority:
        """Assign priority based on distribution"""
        import random
        rand = random.random()
        cumulative = 0
        
        for priority, prob in distribution.items():
            cumulative += prob
            if rand <= cumulative:
                return TestPriority(priority)
        
        return TestPriority.MEDIUM
    
    def _create_fallback_positive_tests(self, story: Dict[str, Any]) -> List[TestCase]:
        """Create fallback positive test cases"""
        return [
            TestCase(
                id="FALLBACK-1",
                name=f"Basic {story.get('summary', 'Functionality')} Test",
                description=f"Basic test for {story.get('summary', 'story functionality')}",
                test_type=TestType.POSITIVE,
                priority=TestPriority.MEDIUM,
                story_id=story.get("key", "UNKNOWN"),
                prerequisites=["System is running", "User is authenticated"],
                steps=[
                    "Navigate to the application",
                    "Perform the required action",
                    "Verify the expected result"
                ],
                test_data={"input": "valid_data"},
                expected_results=["Action completed successfully"],
                assertions=[
                    {"type": "status_code", "value": 200},
                    {"type": "response_contains", "value": "success"}
                ],
                tags=["positive", "fallback"],
                estimated_duration=60,
                complexity="low",
                risk_level="low",
                created_at=datetime.now()
            )
        ]
    
    def _create_fallback_negative_tests(self, story: Dict[str, Any]) -> List[TestCase]:
        """Create fallback negative test cases"""
        return [
            TestCase(
                id="FALLBACK-1",
                name=f"Invalid Input Test for {story.get('summary', 'Functionality')}",
                description=f"Test error handling for {story.get('summary', 'story functionality')}",
                test_type=TestType.NEGATIVE,
                priority=TestPriority.MEDIUM,
                story_id=story.get("key", "UNKNOWN"),
                prerequisites=["System is running", "User is authenticated"],
                steps=[
                    "Navigate to the application",
                    "Enter invalid data",
                    "Submit the form",
                    "Verify error handling"
                ],
                test_data={"input": "invalid_data"},
                expected_results=["Error message displayed", "Form not submitted"],
                assertions=[
                    {"type": "status_code", "value": 400},
                    {"type": "error_message_present", "value": True}
                ],
                tags=["negative", "fallback"],
                estimated_duration=45,
                complexity="low",
                risk_level="medium",
                created_at=datetime.now()
            )
        ]
    
    def _create_fallback_edge_case_tests(self, story: Dict[str, Any]) -> List[TestCase]:
        """Create fallback edge case test cases"""
        return [
            TestCase(
                id="FALLBACK-1",
                name=f"Boundary Test for {story.get('summary', 'Functionality')}",
                description=f"Test boundary conditions for {story.get('summary', 'story functionality')}",
                test_type=TestType.EDGE_CASE,
                priority=TestPriority.HIGH,
                story_id=story.get("key", "UNKNOWN"),
                prerequisites=["System is running", "User is authenticated"],
                steps=[
                    "Navigate to the application",
                    "Enter boundary value data",
                    "Submit the form",
                    "Verify system behavior"
                ],
                test_data={"input": "boundary_value"},
                expected_results=["System handles boundary value correctly"],
                assertions=[
                    {"type": "status_code", "value": 200},
                    {"type": "boundary_handled", "value": True}
                ],
                tags=["edge-case", "fallback"],
                estimated_duration=90,
                complexity="high",
                risk_level="high",
                created_at=datetime.now()
            )
        ]
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get test generation statistics"""
        total_tests = sum(entry["generated_tests"] for entry in self.generation_history)
        total_stories = len(self.generation_history)
        
        test_type_counts = {}
        for entry in self.generation_history:
            for test_type in entry.get("test_types", []):
                test_type_counts[test_type] = test_type_counts.get(test_type, 0) + 1
        
        return {
            "total_tests_generated": total_tests,
            "total_stories_processed": total_stories,
            "average_tests_per_story": total_tests / total_stories if total_stories > 0 else 0,
            "test_type_distribution": test_type_counts,
            "generation_history": self.generation_history
        } 