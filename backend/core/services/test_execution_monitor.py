#!/usr/bin/env python3
"""
🦖 Advanced Test Execution Monitor for Restaceratops
Real-time test execution monitoring with performance metrics and comprehensive reporting
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics
from collections import defaultdict, deque

log = logging.getLogger("restaceratops.test_execution_monitor")

class ExecutionStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

class PerformanceLevel(Enum):
    """Performance level indicators"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class ExecutionMetrics:
    """Test execution metrics"""
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0
    timeout_tests: int = 0
    
    total_duration: float = 0.0
    average_duration: float = 0.0
    min_duration: float = 0.0
    max_duration: float = 0.0
    
    total_response_time: float = 0.0
    average_response_time: float = 0.0
    min_response_time: float = 0.0
    max_response_time: float = 0.0
    
    success_rate: float = 0.0
    failure_rate: float = 0.0
    
    performance_level: PerformanceLevel = PerformanceLevel.GOOD
    bottlenecks: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class TestExecutionEvent:
    """Test execution event"""
    test_id: str
    test_name: str
    status: ExecutionStatus
    timestamp: datetime
    duration: float = 0.0
    response_time: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionSession:
    """Test execution session"""
    session_id: str
    name: str
    description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    metrics: ExecutionMetrics = field(default_factory=ExecutionMetrics)
    events: List[TestExecutionEvent] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

class TestExecutionMonitor:
    """Advanced test execution monitor with real-time monitoring"""
    
    def __init__(self):
        self.active_sessions: Dict[str, ExecutionSession] = {}
        self.completed_sessions: Dict[str, ExecutionSession] = {}
        self.event_listeners: List[Callable] = []
        self.performance_thresholds = self._load_performance_thresholds()
        self.metrics_history: deque = deque(maxlen=1000)  # Keep last 1000 metrics
        
    def _load_performance_thresholds(self) -> Dict[str, float]:
        """Load performance thresholds for different metrics"""
        return {
            "excellent_response_time": 100.0,  # ms
            "good_response_time": 300.0,       # ms
            "fair_response_time": 500.0,       # ms
            "poor_response_time": 1000.0,      # ms
            
            "excellent_duration": 30.0,        # seconds
            "good_duration": 60.0,             # seconds
            "fair_duration": 120.0,            # seconds
            "poor_duration": 300.0,            # seconds
            
            "excellent_success_rate": 95.0,    # percentage
            "good_success_rate": 90.0,         # percentage
            "fair_success_rate": 80.0,         # percentage
            "poor_success_rate": 70.0,         # percentage
        }
    
    async def start_session(
        self, 
        session_id: str, 
        name: str, 
        description: str = "",
        configuration: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> ExecutionSession:
        """Start a new test execution session"""
        
        session = ExecutionSession(
            session_id=session_id,
            name=name,
            description=description,
            start_time=datetime.now(),
            status=ExecutionStatus.RUNNING,
            configuration=configuration or {},
            tags=tags or []
        )
        
        self.active_sessions[session_id] = session
        log.info(f"Started test execution session: {session_id} - {name}")
        
        # Notify listeners
        await self._notify_listeners("session_started", session)
        
        return session
    
    async def end_session(self, session_id: str, status: ExecutionStatus = ExecutionStatus.PASSED) -> ExecutionSession:
        """End a test execution session"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.end_time = datetime.now()
        session.status = status
        
        # Calculate final metrics
        session.metrics = await self._calculate_session_metrics(session)
        
        # Move to completed sessions
        self.completed_sessions[session_id] = session
        del self.active_sessions[session_id]
        
        # Store metrics in history
        self.metrics_history.append({
            "session_id": session_id,
            "metrics": session.metrics,
            "timestamp": datetime.now().isoformat()
        })
        
        log.info(f"Ended test execution session: {session_id} - Status: {status.value}")
        
        # Notify listeners
        await self._notify_listeners("session_ended", session)
        
        return session
    
    async def record_test_event(
        self, 
        session_id: str, 
        test_id: str, 
        test_name: str, 
        status: ExecutionStatus,
        duration: float = 0.0,
        response_time: float = 0.0,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TestExecutionEvent:
        """Record a test execution event"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        event = TestExecutionEvent(
            test_id=test_id,
            test_name=test_name,
            status=status,
            timestamp=datetime.now(),
            duration=duration,
            response_time=response_time,
            error_message=error_message,
            metadata=metadata or {}
        )
        
        session.events.append(event)
        
        # Update real-time metrics
        await self._update_session_metrics(session)
        
        log.debug(f"Recorded test event: {test_id} - {status.value}")
        
        # Notify listeners
        await self._notify_listeners("test_event", event, session)
        
        return event
    
    async def _update_session_metrics(self, session: ExecutionSession):
        """Update session metrics in real-time"""
        if not session.events:
            return
        
        # Calculate basic counts
        total_tests = len(session.events)
        passed_tests = sum(1 for e in session.events if e.status == ExecutionStatus.PASSED)
        failed_tests = sum(1 for e in session.events if e.status == ExecutionStatus.FAILED)
        skipped_tests = sum(1 for e in session.events if e.status == ExecutionStatus.SKIPPED)
        error_tests = sum(1 for e in session.events if e.status == ExecutionStatus.ERROR)
        timeout_tests = sum(1 for e in session.events if e.status == ExecutionStatus.TIMEOUT)
        
        # Calculate duration metrics
        durations = [e.duration for e in session.events if e.duration > 0]
        response_times = [e.response_time for e in session.events if e.response_time > 0]
        
        total_duration = sum(durations)
        total_response_time = sum(response_times)
        
        # Update metrics
        session.metrics.total_tests = total_tests
        session.metrics.passed_tests = passed_tests
        session.metrics.failed_tests = failed_tests
        session.metrics.skipped_tests = skipped_tests
        session.metrics.error_tests = error_tests
        session.metrics.timeout_tests = timeout_tests
        
        session.metrics.total_duration = total_duration
        session.metrics.total_response_time = total_response_time
        
        if durations:
            session.metrics.average_duration = statistics.mean(durations)
            session.metrics.min_duration = min(durations)
            session.metrics.max_duration = max(durations)
        
        if response_times:
            session.metrics.average_response_time = statistics.mean(response_times)
            session.metrics.min_response_time = min(response_times)
            session.metrics.max_response_time = max(response_times)
        
        # Calculate rates
        if total_tests > 0:
            session.metrics.success_rate = (passed_tests / total_tests) * 100
            session.metrics.failure_rate = ((failed_tests + error_tests + timeout_tests) / total_tests) * 100
        
        # Determine performance level
        session.metrics.performance_level = self._determine_performance_level(session.metrics)
        
        # Identify bottlenecks
        session.metrics.bottlenecks = self._identify_bottlenecks(session.events)
        
        # Generate recommendations
        session.metrics.recommendations = self._generate_recommendations(session.metrics)
    
    async def _calculate_session_metrics(self, session: ExecutionSession) -> ExecutionMetrics:
        """Calculate final metrics for a session"""
        await self._update_session_metrics(session)
        return session.metrics
    
    def _determine_performance_level(self, metrics: ExecutionMetrics) -> PerformanceLevel:
        """Determine performance level based on metrics"""
        
        # Check response time
        if metrics.average_response_time <= self.performance_thresholds["excellent_response_time"]:
            response_level = PerformanceLevel.EXCELLENT
        elif metrics.average_response_time <= self.performance_thresholds["good_response_time"]:
            response_level = PerformanceLevel.GOOD
        elif metrics.average_response_time <= self.performance_thresholds["fair_response_time"]:
            response_level = PerformanceLevel.FAIR
        elif metrics.average_response_time <= self.performance_thresholds["poor_response_time"]:
            response_level = PerformanceLevel.POOR
        else:
            response_level = PerformanceLevel.CRITICAL
        
        # Check duration
        if metrics.average_duration <= self.performance_thresholds["excellent_duration"]:
            duration_level = PerformanceLevel.EXCELLENT
        elif metrics.average_duration <= self.performance_thresholds["good_duration"]:
            duration_level = PerformanceLevel.GOOD
        elif metrics.average_duration <= self.performance_thresholds["fair_duration"]:
            duration_level = PerformanceLevel.FAIR
        elif metrics.average_duration <= self.performance_thresholds["poor_duration"]:
            duration_level = PerformanceLevel.POOR
        else:
            duration_level = PerformanceLevel.CRITICAL
        
        # Check success rate
        if metrics.success_rate >= self.performance_thresholds["excellent_success_rate"]:
            success_level = PerformanceLevel.EXCELLENT
        elif metrics.success_rate >= self.performance_thresholds["good_success_rate"]:
            success_level = PerformanceLevel.GOOD
        elif metrics.success_rate >= self.performance_thresholds["fair_success_rate"]:
            success_level = PerformanceLevel.FAIR
        elif metrics.success_rate >= self.performance_thresholds["poor_success_rate"]:
            success_level = PerformanceLevel.POOR
        else:
            success_level = PerformanceLevel.CRITICAL
        
        # Return the worst level among all metrics
        levels = [response_level, duration_level, success_level]
        worst_level = max(levels, key=lambda x: x.value)
        
        return worst_level
    
    def _identify_bottlenecks(self, events: List[TestExecutionEvent]) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        if not events:
            return bottlenecks
        
        # Check for slow tests
        slow_tests = [e for e in events if e.duration > self.performance_thresholds["poor_duration"]]
        if slow_tests:
            slow_test_names = [e.test_name for e in slow_tests[:3]]  # Top 3 slowest
            bottlenecks.append(f"Slow tests detected: {', '.join(slow_test_names)}")
        
        # Check for high response times
        high_response_tests = [e for e in events if e.response_time > self.performance_thresholds["poor_response_time"]]
        if high_response_tests:
            high_response_names = [e.test_name for e in high_response_tests[:3]]  # Top 3 highest
            bottlenecks.append(f"High response time tests: {', '.join(high_response_names)}")
        
        # Check for frequent failures
        failed_tests = [e for e in events if e.status in [ExecutionStatus.FAILED, ExecutionStatus.ERROR]]
        if len(failed_tests) > len(events) * 0.2:  # More than 20% failures
            bottlenecks.append("High failure rate detected")
        
        # Check for timeouts
        timeout_tests = [e for e in events if e.status == ExecutionStatus.TIMEOUT]
        if timeout_tests:
            bottlenecks.append(f"Timeout issues detected in {len(timeout_tests)} tests")
        
        return bottlenecks
    
    def _generate_recommendations(self, metrics: ExecutionMetrics) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Response time recommendations
        if metrics.average_response_time > self.performance_thresholds["poor_response_time"]:
            recommendations.append("Consider optimizing API response times")
            recommendations.append("Review network latency and server performance")
        
        # Duration recommendations
        if metrics.average_duration > self.performance_thresholds["poor_duration"]:
            recommendations.append("Consider parallel test execution")
            recommendations.append("Review test setup and teardown efficiency")
        
        # Success rate recommendations
        if metrics.success_rate < self.performance_thresholds["poor_success_rate"]:
            recommendations.append("Investigate and fix failing tests")
            recommendations.append("Review test data and environment setup")
        
        # General recommendations
        if metrics.failed_tests > 0:
            recommendations.append("Implement better error handling in tests")
        
        if metrics.timeout_tests > 0:
            recommendations.append("Increase timeout values or optimize slow operations")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable ranges")
        
        return recommendations
    
    def add_event_listener(self, listener: Callable):
        """Add an event listener for real-time updates"""
        self.event_listeners.append(listener)
    
    async def _notify_listeners(self, event_type: str, data: Any, session: Optional[ExecutionSession] = None):
        """Notify all event listeners"""
        for listener in self.event_listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(event_type, data, session)
                else:
                    listener(event_type, data, session)
            except Exception as e:
                log.error(f"Error in event listener: {e}")
    
    def get_session(self, session_id: str) -> Optional[ExecutionSession]:
        """Get a session by ID"""
        return self.active_sessions.get(session_id) or self.completed_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[ExecutionSession]:
        """Get all active sessions"""
        return list(self.active_sessions.values())
    
    def get_completed_sessions(self) -> List[ExecutionSession]:
        """Get all completed sessions"""
        return list(self.completed_sessions.values())
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
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
                "skipped_tests": session.metrics.skipped_tests,
                "error_tests": session.metrics.error_tests,
                "timeout_tests": session.metrics.timeout_tests,
                "success_rate": session.metrics.success_rate,
                "failure_rate": session.metrics.failure_rate,
                "average_duration": session.metrics.average_duration,
                "average_response_time": session.metrics.average_response_time,
                "performance_level": session.metrics.performance_level.value,
                "bottlenecks": session.metrics.bottlenecks,
                "recommendations": session.metrics.recommendations
            },
            "tags": session.tags,
            "configuration": session.configuration
        }
    
    def get_performance_report(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a detailed performance report for a session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Group events by status
        events_by_status = defaultdict(list)
        for event in session.events:
            events_by_status[event.status.value].append(event)
        
        # Calculate performance trends
        performance_trends = self._calculate_performance_trends(session.events)
        
        # Identify top performers and issues
        top_performers = self._identify_top_performers(session.events)
        problematic_tests = self._identify_problematic_tests(session.events)
        
        return {
            "session_id": session_id,
            "session_name": session.name,
            "overall_metrics": {
                "total_tests": session.metrics.total_tests,
                "success_rate": session.metrics.success_rate,
                "performance_level": session.metrics.performance_level.value,
                "total_duration": session.metrics.total_duration,
                "average_duration": session.metrics.average_duration,
                "average_response_time": session.metrics.average_response_time
            },
            "status_breakdown": {
                status: {
                    "count": len(events),
                    "percentage": (len(events) / session.metrics.total_tests * 100) if session.metrics.total_tests > 0 else 0,
                    "average_duration": statistics.mean([e.duration for e in events]) if events else 0,
                    "average_response_time": statistics.mean([e.response_time for e in events]) if events else 0
                }
                for status, events in events_by_status.items()
            },
            "performance_trends": performance_trends,
            "top_performers": top_performers,
            "problematic_tests": problematic_tests,
            "bottlenecks": session.metrics.bottlenecks,
            "recommendations": session.metrics.recommendations,
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_performance_trends(self, events: List[TestExecutionEvent]) -> Dict[str, Any]:
        """Calculate performance trends over time"""
        if not events:
            return {}
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda x: x.timestamp)
        
        # Calculate moving averages
        window_size = min(10, len(sorted_events))
        durations = [e.duration for e in sorted_events]
        response_times = [e.response_time for e in sorted_events]
        
        moving_avg_duration = []
        moving_avg_response = []
        
        for i in range(window_size, len(sorted_events)):
            moving_avg_duration.append(statistics.mean(durations[i-window_size:i]))
            moving_avg_response.append(statistics.mean(response_times[i-window_size:i]))
        
        return {
            "moving_average_duration": moving_avg_duration,
            "moving_average_response_time": moving_avg_response,
            "trend_direction": "improving" if len(moving_avg_duration) > 1 and moving_avg_duration[-1] < moving_avg_duration[0] else "stable"
        }
    
    def _identify_top_performers(self, events: List[TestExecutionEvent]) -> List[Dict[str, Any]]:
        """Identify top performing tests"""
        if not events:
            return []
        
        # Filter passed tests and sort by duration
        passed_events = [e for e in events if e.status == ExecutionStatus.PASSED]
        passed_events.sort(key=lambda x: x.duration)
        
        return [
            {
                "test_name": e.test_name,
                "duration": e.duration,
                "response_time": e.response_time,
                "rank": i + 1
            }
            for i, e in enumerate(passed_events[:5])  # Top 5
        ]
    
    def _identify_problematic_tests(self, events: List[TestExecutionEvent]) -> List[Dict[str, Any]]:
        """Identify problematic tests"""
        if not events:
            return []
        
        # Group by test name and analyze
        test_analysis = defaultdict(lambda: {
            "total_runs": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "timeouts": 0,
            "total_duration": 0.0,
            "total_response_time": 0.0
        })
        
        for event in events:
            analysis = test_analysis[event.test_name]
            analysis["total_runs"] += 1
            analysis["total_duration"] += event.duration
            analysis["total_response_time"] += event.response_time
            
            if event.status == ExecutionStatus.PASSED:
                analysis["passed"] += 1
            elif event.status == ExecutionStatus.FAILED:
                analysis["failed"] += 1
            elif event.status == ExecutionStatus.ERROR:
                analysis["errors"] += 1
            elif event.status == ExecutionStatus.TIMEOUT:
                analysis["timeouts"] += 1
        
        # Identify problematic tests
        problematic = []
        for test_name, analysis in test_analysis.items():
            if (analysis["failed"] > 0 or analysis["errors"] > 0 or 
                analysis["timeouts"] > 0 or 
                analysis["total_duration"] / analysis["total_runs"] > self.performance_thresholds["poor_duration"]):
                
                problematic.append({
                    "test_name": test_name,
                    "total_runs": analysis["total_runs"],
                    "success_rate": (analysis["passed"] / analysis["total_runs"]) * 100,
                    "average_duration": analysis["total_duration"] / analysis["total_runs"],
                    "average_response_time": analysis["total_response_time"] / analysis["total_runs"],
                    "issues": {
                        "failures": analysis["failed"],
                        "errors": analysis["errors"],
                        "timeouts": analysis["timeouts"]
                    }
                })
        
        # Sort by severity (lowest success rate first)
        problematic.sort(key=lambda x: x["success_rate"])
        
        return problematic[:10]  # Top 10 problematic tests
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global statistics across all sessions"""
        all_sessions = list(self.active_sessions.values()) + list(self.completed_sessions.values())
        
        if not all_sessions:
            return {}
        
        total_sessions = len(all_sessions)
        completed_sessions = len(self.completed_sessions)
        active_sessions = len(self.active_sessions)
        
        # Aggregate metrics
        total_tests = sum(s.metrics.total_tests for s in all_sessions)
        total_passed = sum(s.metrics.passed_tests for s in all_sessions)
        total_failed = sum(s.metrics.failed_tests for s in all_sessions)
        
        # Calculate averages
        avg_success_rate = statistics.mean([s.metrics.success_rate for s in all_sessions if s.metrics.total_tests > 0])
        avg_duration = statistics.mean([s.metrics.average_duration for s in all_sessions if s.metrics.average_duration > 0])
        avg_response_time = statistics.mean([s.metrics.average_response_time for s in all_sessions if s.metrics.average_response_time > 0])
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "active_sessions": active_sessions,
            "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
            
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "overall_success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            
            "average_success_rate": avg_success_rate,
            "average_duration": avg_duration,
            "average_response_time": avg_response_time,
            
            "recent_metrics": list(self.metrics_history)[-10:] if self.metrics_history else []
        } 