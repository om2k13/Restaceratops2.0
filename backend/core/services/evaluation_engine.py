#!/usr/bin/env python3
"""
🦖 Advanced Evaluation Engine for Restaceratops
Comprehensive test result evaluation with AI-powered analysis
"""

import asyncio
import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import statistics
from collections import defaultdict

log = logging.getLogger("restaceratops.evaluation_engine")

class EvaluationMetric(Enum):
    """Evaluation metrics"""
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    ACCURACY = "accuracy"
    CONTEXT_RELEVANCE = "context_relevance"
    HALLUCINATION_SCORE = "hallucination_score"
    FAITHFULNESS_SCORE = "faithfulness_score"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"

class EvaluationLevel(Enum):
    """Evaluation levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class EvaluationResult:
    """Evaluation result structure"""
    test_id: str
    test_name: str
    evaluation_metrics: Dict[str, float]
    evaluation_level: EvaluationLevel
    context_analysis: Dict[str, Any]
    hallucination_detection: Dict[str, Any]
    faithfulness_evaluation: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    evaluation_timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestExecutionResult:
    """Test execution result structure"""
    test_id: str
    test_name: str
    status: str
    execution_time: float
    response_time: float
    actual_results: Dict[str, Any]
    expected_results: Dict[str, Any]
    assertions: List[Dict[str, Any]]
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EvaluationConfig:
    """Configuration for evaluation"""
    enable_context_analysis: bool = True
    enable_hallucination_detection: bool = True
    enable_faithfulness_evaluation: bool = True
    enable_completeness_check: bool = True
    enable_consistency_check: bool = True
    confidence_threshold: float = 0.8
    context_relevance_threshold: float = 0.7
    hallucination_threshold: float = 0.3
    faithfulness_threshold: float = 0.8

class AdvancedEvaluationEngine:
    """Advanced evaluation engine with AI-powered analysis"""
    
    def __init__(self, chat_interface=None):
        self.chat_interface = chat_interface
        self.evaluation_history: List[Dict[str, Any]] = []
        self.metric_weights = self._load_metric_weights()
        self.context_templates = self._load_context_templates()
        
    def _load_metric_weights(self) -> Dict[str, float]:
        """Load weights for different evaluation metrics"""
        return {
            "precision": 0.25,
            "recall": 0.25,
            "f1_score": 0.20,
            "accuracy": 0.15,
            "context_relevance": 0.10,
            "hallucination_score": 0.05
        }
    
    def _load_context_templates(self) -> Dict[str, str]:
        """Load context analysis templates"""
        return {
            "user_story": """
            Analyze the test result against the user story context:
            
            User Story: {story_summary}
            Acceptance Criteria: {acceptance_criteria}
            
            Test Result: {test_result}
            Expected Outcome: {expected_outcome}
            
            Evaluate:
            1. Relevance to user story objectives
            2. Coverage of acceptance criteria
            3. Business value alignment
            4. User experience impact
            """,
            
            "technical_requirements": """
            Analyze the test result against technical requirements:
            
            Technical Requirements: {requirements}
            Test Result: {test_result}
            Expected Outcome: {expected_outcome}
            
            Evaluate:
            1. Technical accuracy
            2. Performance compliance
            3. Security considerations
            4. Scalability impact
            """,
            
            "business_rules": """
            Analyze the test result against business rules:
            
            Business Rules: {business_rules}
            Test Result: {test_result}
            Expected Outcome: {expected_outcome}
            
            Evaluate:
            1. Rule compliance
            2. Business logic accuracy
            3. Data integrity
            4. Regulatory compliance
            """
        }
    
    async def evaluate_test_results(
        self, 
        execution_results: List[TestExecutionResult],
        config: EvaluationConfig
    ) -> List[EvaluationResult]:
        """Evaluate test execution results comprehensively"""
        
        log.info(f"Evaluating {len(execution_results)} test results")
        
        evaluation_results = []
        
        for result in execution_results:
            try:
                evaluation = await self._evaluate_single_test(result, config)
                evaluation_results.append(evaluation)
            except Exception as e:
                log.error(f"Failed to evaluate test {result.test_id}: {e}")
                # Create fallback evaluation
                evaluation = self._create_fallback_evaluation(result)
                evaluation_results.append(evaluation)
        
        # Log evaluation
        self.evaluation_history.append({
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(execution_results),
            "evaluated_tests": len(evaluation_results),
            "average_confidence": statistics.mean([e.confidence_score for e in evaluation_results]),
            "evaluation_levels": self._count_evaluation_levels(evaluation_results)
        })
        
        log.info(f"Completed evaluation of {len(evaluation_results)} tests")
        return evaluation_results
    
    async def _evaluate_single_test(
        self, 
        result: TestExecutionResult, 
        config: EvaluationConfig
    ) -> EvaluationResult:
        """Evaluate a single test result"""
        
        # Calculate basic metrics
        metrics = await self._calculate_basic_metrics(result)
        
        # Context analysis
        context_analysis = {}
        if config.enable_context_analysis:
            context_analysis = await self._analyze_context(result)
        
        # Hallucination detection
        hallucination_detection = {}
        if config.enable_hallucination_detection:
            hallucination_detection = await self._detect_hallucinations(result)
        
        # Faithfulness evaluation
        faithfulness_evaluation = {}
        if config.enable_faithfulness_evaluation:
            faithfulness_evaluation = await self._evaluate_faithfulness(result)
        
        # Completeness check
        completeness_score = 1.0
        if config.enable_completeness_check:
            completeness_score = self._check_completeness(result)
        
        # Consistency check
        consistency_score = 1.0
        if config.enable_consistency_check:
            consistency_score = self._check_consistency(result)
        
        # Update metrics with additional scores
        metrics.update({
            "completeness": completeness_score,
            "consistency": consistency_score
        })
        
        # Calculate overall confidence score
        confidence_score = self._calculate_confidence_score(metrics, config)
        
        # Determine evaluation level
        evaluation_level = self._determine_evaluation_level(metrics, config)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, context_analysis, hallucination_detection)
        
        return EvaluationResult(
            test_id=result.test_id,
            test_name=result.test_name,
            evaluation_metrics=metrics,
            evaluation_level=evaluation_level,
            context_analysis=context_analysis,
            hallucination_detection=hallucination_detection,
            faithfulness_evaluation=faithfulness_evaluation,
            recommendations=recommendations,
            confidence_score=confidence_score,
            evaluation_timestamp=datetime.now()
        )
    
    async def _calculate_basic_metrics(self, result: TestExecutionResult) -> Dict[str, float]:
        """Calculate basic evaluation metrics"""
        
        metrics = {}
        
        # Calculate precision, recall, F1 score based on assertions
        if result.assertions:
            total_assertions = len(result.assertions)
            passed_assertions = sum(1 for assertion in result.assertions if assertion.get('passed', False))
            
            metrics['precision'] = passed_assertions / total_assertions if total_assertions > 0 else 0.0
            metrics['recall'] = passed_assertions / total_assertions if total_assertions > 0 else 0.0
            metrics['f1_score'] = metrics['precision'] if metrics['precision'] > 0 else 0.0
            metrics['accuracy'] = passed_assertions / total_assertions if total_assertions > 0 else 0.0
        else:
            # Fallback metrics based on test status
            if result.status == 'passed':
                metrics['precision'] = 1.0
                metrics['recall'] = 1.0
                metrics['f1_score'] = 1.0
                metrics['accuracy'] = 1.0
            else:
                metrics['precision'] = 0.0
                metrics['recall'] = 0.0
                metrics['f1_score'] = 0.0
                metrics['accuracy'] = 0.0
        
        # Performance metrics
        metrics['execution_efficiency'] = self._calculate_execution_efficiency(result)
        metrics['response_quality'] = self._calculate_response_quality(result)
        
        return metrics
    
    def _calculate_execution_efficiency(self, result: TestExecutionResult) -> float:
        """Calculate execution efficiency score"""
        # Base efficiency on execution time and response time
        if result.execution_time <= 1.0 and result.response_time <= 100:
            return 1.0
        elif result.execution_time <= 5.0 and result.response_time <= 500:
            return 0.8
        elif result.execution_time <= 10.0 and result.response_time <= 1000:
            return 0.6
        else:
            return 0.4
    
    def _calculate_response_quality(self, result: TestExecutionResult) -> float:
        """Calculate response quality score"""
        # Analyze actual vs expected results
        if not result.actual_results or not result.expected_results:
            return 0.5
        
        # Simple comparison - in real implementation, this would be more sophisticated
        actual_keys = set(result.actual_results.keys())
        expected_keys = set(result.expected_results.keys())
        
        if not expected_keys:
            return 0.5
        
        # Calculate overlap
        overlap = len(actual_keys.intersection(expected_keys))
        coverage = overlap / len(expected_keys)
        
        return min(coverage, 1.0)
    
    async def _analyze_context(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Analyze test result context"""
        
        if not self.chat_interface:
            return self._create_fallback_context_analysis(result)
        
        try:
            # Extract context from test metadata
            context_data = result.metadata.get('context', {})
            
            # Create context analysis prompt
            prompt = f"""
            Analyze the test result context and relevance:
            
            Test Name: {result.test_name}
            Test Status: {result.status}
            Actual Results: {json.dumps(result.actual_results, indent=2)}
            Expected Results: {json.dumps(result.expected_results, indent=2)}
            Context: {json.dumps(context_data, indent=2)}
            
            Provide analysis in JSON format:
            {{
                "relevance_score": 0.0-1.0,
                "business_alignment": 0.0-1.0,
                "user_experience_impact": "low|medium|high",
                "technical_accuracy": 0.0-1.0,
                "context_coverage": 0.0-1.0,
                "improvement_areas": ["area1", "area2"],
                "strengths": ["strength1", "strength2"]
            }}
            """
            
            response = await self.chat_interface.handle_message(prompt)
            
            # Parse JSON response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            else:
                return self._create_fallback_context_analysis(result)
                
        except Exception as e:
            log.error(f"Failed to analyze context: {e}")
            return self._create_fallback_context_analysis(result)
    
    def _create_fallback_context_analysis(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Create fallback context analysis"""
        return {
            "relevance_score": 0.7,
            "business_alignment": 0.7,
            "user_experience_impact": "medium",
            "technical_accuracy": 0.7,
            "context_coverage": 0.7,
            "improvement_areas": ["Enhanced context analysis needed"],
            "strengths": ["Basic test execution completed"]
        }
    
    async def _detect_hallucinations(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Detect hallucinations in test results"""
        
        if not self.chat_interface:
            return self._create_fallback_hallucination_detection(result)
        
        try:
            prompt = f"""
            Detect potential hallucinations in the test result:
            
            Test Name: {result.test_name}
            Actual Results: {json.dumps(result.actual_results, indent=2)}
            Expected Results: {json.dumps(result.expected_results, indent=2)}
            
            Analyze for:
            1. Inconsistent or contradictory information
            2. Information not present in expected results
            3. Exaggerated or unrealistic claims
            4. Contextual inconsistencies
            
            Provide analysis in JSON format:
            {{
                "hallucination_score": 0.0-1.0,
                "detected_hallucinations": ["hallucination1", "hallucination2"],
                "confidence_level": "low|medium|high",
                "risk_assessment": "low|medium|high",
                "mitigation_suggestions": ["suggestion1", "suggestion2"]
            }}
            """
            
            response = await self.chat_interface.handle_message(prompt)
            
            # Parse JSON response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                detection = json.loads(json_match.group())
                return detection
            else:
                return self._create_fallback_hallucination_detection(result)
                
        except Exception as e:
            log.error(f"Failed to detect hallucinations: {e}")
            return self._create_fallback_hallucination_detection(result)
    
    def _create_fallback_hallucination_detection(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Create fallback hallucination detection"""
        return {
            "hallucination_score": 0.1,
            "detected_hallucinations": [],
            "confidence_level": "medium",
            "risk_assessment": "low",
            "mitigation_suggestions": ["Enhanced hallucination detection needed"]
        }
    
    async def _evaluate_faithfulness(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Evaluate faithfulness of test results"""
        
        if not self.chat_interface:
            return self._create_fallback_faithfulness_evaluation(result)
        
        try:
            prompt = f"""
            Evaluate the faithfulness of the test result:
            
            Test Name: {result.test_name}
            Actual Results: {json.dumps(result.actual_results, indent=2)}
            Expected Results: {json.dumps(result.expected_results, indent=2)}
            
            Analyze faithfulness in terms of:
            1. Adherence to expected outcomes
            2. Consistency with test objectives
            3. Reliability of results
            4. Trustworthiness of execution
            
            Provide analysis in JSON format:
            {{
                "faithfulness_score": 0.0-1.0,
                "adherence_level": "low|medium|high",
                "consistency_score": 0.0-1.0,
                "reliability_score": 0.0-1.0,
                "trustworthiness": "low|medium|high",
                "faithfulness_issues": ["issue1", "issue2"],
                "improvement_recommendations": ["rec1", "rec2"]
            }}
            """
            
            response = await self.chat_interface.handle_message(prompt)
            
            # Parse JSON response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                evaluation = json.loads(json_match.group())
                return evaluation
            else:
                return self._create_fallback_faithfulness_evaluation(result)
                
        except Exception as e:
            log.error(f"Failed to evaluate faithfulness: {e}")
            return self._create_fallback_faithfulness_evaluation(result)
    
    def _create_fallback_faithfulness_evaluation(self, result: TestExecutionResult) -> Dict[str, Any]:
        """Create fallback faithfulness evaluation"""
        return {
            "faithfulness_score": 0.8,
            "adherence_level": "medium",
            "consistency_score": 0.8,
            "reliability_score": 0.8,
            "trustworthiness": "medium",
            "faithfulness_issues": [],
            "improvement_recommendations": ["Enhanced faithfulness evaluation needed"]
        }
    
    def _check_completeness(self, result: TestExecutionResult) -> float:
        """Check completeness of test results"""
        # Analyze if all expected results are present
        if not result.expected_results:
            return 1.0
        
        actual_keys = set(result.actual_results.keys())
        expected_keys = set(result.expected_results.keys())
        
        if not expected_keys:
            return 1.0
        
        # Calculate completeness
        completeness = len(actual_keys.intersection(expected_keys)) / len(expected_keys)
        return min(completeness, 1.0)
    
    def _check_consistency(self, result: TestExecutionResult) -> float:
        """Check consistency of test results"""
        # Analyze consistency between actual and expected results
        if not result.actual_results or not result.expected_results:
            return 0.5
        
        # Simple consistency check - in real implementation, this would be more sophisticated
        consistency_score = 0.8  # Default score
        
        # Check for obvious inconsistencies
        for key in result.actual_results:
            if key in result.expected_results:
                actual_value = result.actual_results[key]
                expected_value = result.expected_results[key]
                
                # Type consistency check
                if type(actual_value) != type(expected_value):
                    consistency_score -= 0.1
                
                # Value consistency check (simplified)
                if actual_value != expected_value and result.status == 'passed':
                    consistency_score -= 0.2
        
        return max(consistency_score, 0.0)
    
    def _calculate_confidence_score(self, metrics: Dict[str, float], config: EvaluationConfig) -> float:
        """Calculate overall confidence score"""
        
        # Weighted average of metrics
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, weight in self.metric_weights.items():
            if metric in metrics:
                weighted_sum += metrics[metric] * weight
                total_weight += weight
        
        # Add additional metrics
        if 'completeness' in metrics:
            weighted_sum += metrics['completeness'] * 0.1
            total_weight += 0.1
        
        if 'consistency' in metrics:
            weighted_sum += metrics['consistency'] * 0.1
            total_weight += 0.1
        
        if total_weight > 0:
            confidence_score = weighted_sum / total_weight
        else:
            confidence_score = 0.5
        
        return min(confidence_score, 1.0)
    
    def _determine_evaluation_level(self, metrics: Dict[str, float], config: EvaluationConfig) -> EvaluationLevel:
        """Determine evaluation level based on metrics"""
        
        # Calculate average score
        scores = [
            metrics.get('precision', 0.0),
            metrics.get('recall', 0.0),
            metrics.get('f1_score', 0.0),
            metrics.get('accuracy', 0.0),
            metrics.get('completeness', 0.0),
            metrics.get('consistency', 0.0)
        ]
        
        avg_score = statistics.mean(scores)
        
        if avg_score >= 0.9:
            return EvaluationLevel.EXCELLENT
        elif avg_score >= 0.8:
            return EvaluationLevel.GOOD
        elif avg_score >= 0.7:
            return EvaluationLevel.FAIR
        elif avg_score >= 0.6:
            return EvaluationLevel.POOR
        else:
            return EvaluationLevel.CRITICAL
    
    def _generate_recommendations(
        self, 
        metrics: Dict[str, float], 
        context_analysis: Dict[str, Any],
        hallucination_detection: Dict[str, Any]
    ) -> List[str]:
        """Generate improvement recommendations"""
        
        recommendations = []
        
        # Metric-based recommendations
        if metrics.get('precision', 1.0) < 0.8:
            recommendations.append("Improve test precision by refining assertions")
        
        if metrics.get('recall', 1.0) < 0.8:
            recommendations.append("Enhance test coverage to improve recall")
        
        if metrics.get('f1_score', 1.0) < 0.8:
            recommendations.append("Balance precision and recall for better F1 score")
        
        if metrics.get('completeness', 1.0) < 0.8:
            recommendations.append("Ensure all expected results are validated")
        
        if metrics.get('consistency', 1.0) < 0.8:
            recommendations.append("Check for consistency between actual and expected results")
        
        # Context-based recommendations
        if context_analysis.get('relevance_score', 1.0) < 0.7:
            recommendations.append("Improve test relevance to business objectives")
        
        if context_analysis.get('business_alignment', 1.0) < 0.7:
            recommendations.append("Better align tests with business requirements")
        
        # Hallucination-based recommendations
        if hallucination_detection.get('hallucination_score', 0.0) > 0.3:
            recommendations.append("Address potential hallucinations in test results")
        
        if not recommendations:
            recommendations.append("Test evaluation is within acceptable parameters")
        
        return recommendations
    
    def _create_fallback_evaluation(self, result: TestExecutionResult) -> EvaluationResult:
        """Create fallback evaluation when analysis fails"""
        
        metrics = {
            "precision": 0.5,
            "recall": 0.5,
            "f1_score": 0.5,
            "accuracy": 0.5,
            "completeness": 0.5,
            "consistency": 0.5,
            "execution_efficiency": 0.5,
            "response_quality": 0.5
        }
        
        return EvaluationResult(
            test_id=result.test_id,
            test_name=result.test_name,
            evaluation_metrics=metrics,
            evaluation_level=EvaluationLevel.FAIR,
            context_analysis=self._create_fallback_context_analysis(result),
            hallucination_detection=self._create_fallback_hallucination_detection(result),
            faithfulness_evaluation=self._create_fallback_faithfulness_evaluation(result),
            recommendations=["Enhanced evaluation analysis needed"],
            confidence_score=0.5,
            evaluation_timestamp=datetime.now()
        )
    
    def _count_evaluation_levels(self, evaluations: List[EvaluationResult]) -> Dict[str, int]:
        """Count evaluation levels"""
        counts = defaultdict(int)
        for evaluation in evaluations:
            counts[evaluation.evaluation_level.value] += 1
        return dict(counts)
    
    def get_evaluation_stats(self) -> Dict[str, Any]:
        """Get evaluation statistics"""
        if not self.evaluation_history:
            return {}
        
        total_evaluations = sum(entry["total_tests"] for entry in self.evaluation_history)
        total_evaluated = sum(entry["evaluated_tests"] for entry in self.evaluation_history)
        
        avg_confidence = statistics.mean(entry["average_confidence"] for entry in self.evaluation_history)
        
        # Aggregate evaluation levels
        all_levels = defaultdict(int)
        for entry in self.evaluation_history:
            for level, count in entry.get("evaluation_levels", {}).items():
                all_levels[level] += count
        
        return {
            "total_evaluations": total_evaluations,
            "total_evaluated": total_evaluated,
            "evaluation_success_rate": (total_evaluated / total_evaluations * 100) if total_evaluations > 0 else 0,
            "average_confidence": avg_confidence,
            "evaluation_level_distribution": dict(all_levels),
            "evaluation_history": self.evaluation_history
        } 