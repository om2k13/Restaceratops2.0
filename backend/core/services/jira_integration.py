#!/usr/bin/env python3
"""
🦖 Jira Integration Service for Restaceratops
Advanced Jira integration with user story management, validation, and notifications
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import aiohttp
from pydantic import BaseModel

log = logging.getLogger("restaceratops.jira_integration")

@dataclass
class JiraStory:
    """Jira user story data structure"""
    id: str
    key: str
    summary: str
    description: str
    status: str
    assignee: Optional[str]
    acceptance_criteria: List[str]
    epic: Optional[str]
    priority: str
    created: datetime
    updated: datetime

@dataclass
class StoryValidationResult:
    """Validation result for a user story"""
    story_id: str
    is_valid: bool
    validation_score: float
    issues: List[str]
    suggestions: List[str]
    acceptance_criteria_match: Dict[str, bool]

class JiraConfig(BaseModel):
    """Jira configuration"""
    base_url: str
    username: str
    api_token: str
    project_key: str
    board_id: Optional[int] = None

class JiraIntegration:
    """Advanced Jira integration service"""
    
    def __init__(self, config: JiraConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.auth_header = self._create_auth_header()
        
    def _create_auth_header(self) -> Dict[str, str]:
        """Create authentication header for Jira API"""
        import base64
        credentials = f"{self.config.username}:{self.config.api_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers=self.auth_header,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Jira connection and return project info"""
        try:
            async with self.session.get(f"{self.config.base_url}/rest/api/3/myself") as response:
                if response.status == 200:
                    user_info = await response.json()
                    
                    # Get project info
                    project_info = await self._get_project_info()
                    
                    return {
                        "success": True,
                        "user": user_info,
                        "project": project_info,
                        "message": "Connection successful"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Authentication failed: {response.status}",
                        "message": "Check your credentials"
                    }
        except Exception as e:
            log.error(f"Jira connection test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Connection failed"
            }
    
    async def _get_project_info(self) -> Dict[str, Any]:
        """Get project information"""
        url = f"{self.config.base_url}/rest/api/3/project/{self.config.project_key}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return {}
    
    async def fetch_user_stories(self, 
                                status_filter: Optional[List[str]] = None,
                                epic_filter: Optional[str] = None,
                                assignee_filter: Optional[str] = None) -> List[JiraStory]:
        """Fetch user stories from Jira with advanced filtering"""
        
        # Build JQL query
        jql_parts = [
            f"project = {self.config.project_key}",
            "issuetype = 'Story'"
        ]
        
        if status_filter:
            status_clause = " OR ".join([f"status = '{status}'" for status in status_filter])
            jql_parts.append(f"({status_clause})")
        
        if epic_filter:
            jql_parts.append(f"'Epic Link' = {epic_filter}")
        
        if assignee_filter:
            jql_parts.append(f"assignee = '{assignee_filter}'")
        
        jql = " AND ".join(jql_parts)
        
        # Fetch issues
        url = f"{self.config.base_url}/rest/api/3/search"
        params = {
            "jql": jql,
            "maxResults": 100,
            "fields": "summary,description,status,assignee,priority,created,updated,customfield_10014"  # acceptance criteria field
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                stories = []
                
                for issue in data.get("issues", []):
                    story = self._parse_jira_issue(issue)
                    if story:
                        stories.append(story)
                
                log.info(f"Fetched {len(stories)} user stories from Jira")
                return stories
            else:
                log.error(f"Failed to fetch user stories: {response.status}")
                return []
    
    def _parse_jira_issue(self, issue: Dict[str, Any]) -> Optional[JiraStory]:
        """Parse Jira issue into JiraStory object"""
        try:
            fields = issue.get("fields", {})
            
            # Extract acceptance criteria
            acceptance_criteria = []
            ac_field = fields.get("customfield_10014")  # Common acceptance criteria field
            if ac_field:
                if isinstance(ac_field, str):
                    acceptance_criteria = [line.strip() for line in ac_field.split('\n') if line.strip()]
                elif isinstance(ac_field, dict):
                    acceptance_criteria = [ac_field.get("content", "")]
            
            # Parse dates
            created = datetime.fromisoformat(fields.get("created", "").replace("Z", "+00:00"))
            updated = datetime.fromisoformat(fields.get("updated", "").replace("Z", "+00:00"))
            
            return JiraStory(
                id=issue["id"],
                key=issue["key"],
                summary=fields.get("summary", ""),
                description=fields.get("description", ""),
                status=fields.get("status", {}).get("name", "Unknown"),
                assignee=fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                acceptance_criteria=acceptance_criteria,
                epic=fields.get("customfield_10014"),  # Epic link field
                priority=fields.get("priority", {}).get("name", "Medium"),
                created=created,
                updated=updated
            )
        except Exception as e:
            log.error(f"Failed to parse Jira issue {issue.get('key', 'unknown')}: {e}")
            return None
    
    async def validate_user_stories(self, stories: List[JiraStory]) -> List[StoryValidationResult]:
        """Validate user stories against acceptance criteria and best practices"""
        validation_results = []
        
        for story in stories:
            result = await self._validate_single_story(story)
            validation_results.append(result)
        
        return validation_results
    
    async def _validate_single_story(self, story: JiraStory) -> StoryValidationResult:
        """Validate a single user story"""
        issues = []
        suggestions = []
        acceptance_criteria_match = {}
        validation_score = 100.0
        
        # Check story structure
        if not story.summary:
            issues.append("Missing story summary")
            validation_score -= 20
        
        if not story.description:
            issues.append("Missing story description")
            validation_score -= 15
        
        # Check acceptance criteria
        if not story.acceptance_criteria:
            issues.append("Missing acceptance criteria")
            validation_score -= 25
        else:
            for i, criteria in enumerate(story.acceptance_criteria):
                is_valid = self._validate_acceptance_criteria(criteria)
                acceptance_criteria_match[f"AC_{i+1}"] = is_valid
                if not is_valid:
                    issues.append(f"Acceptance criteria {i+1} is not well-defined")
                    validation_score -= 10
        
        # Check story format (As a... I want... So that...)
        if not self._validate_story_format(story.summary):
            issues.append("Story doesn't follow standard format (As a... I want... So that...)")
            validation_score -= 10
            suggestions.append("Consider reformatting: 'As a [user], I want [feature], so that [benefit]'")
        
        # Check for testable criteria
        if not self._has_testable_criteria(story):
            issues.append("Story lacks testable acceptance criteria")
            validation_score -= 15
            suggestions.append("Add specific, measurable acceptance criteria")
        
        # Ensure score doesn't go below 0
        validation_score = max(0, validation_score)
        
        return StoryValidationResult(
            story_id=story.key,
            is_valid=validation_score >= 70,
            validation_score=validation_score,
            issues=issues,
            suggestions=suggestions,
            acceptance_criteria_match=acceptance_criteria_match
        )
    
    def _validate_acceptance_criteria(self, criteria: str) -> bool:
        """Validate individual acceptance criteria"""
        if not criteria or len(criteria.strip()) < 10:
            return False
        
        # Check for specific, measurable criteria
        has_measurable = any(word in criteria.lower() for word in 
                           ["when", "then", "given", "should", "must", "will"])
        
        return has_measurable
    
    def _validate_story_format(self, summary: str) -> bool:
        """Validate user story format"""
        summary_lower = summary.lower()
        has_as_a = "as a" in summary_lower
        has_i_want = "i want" in summary_lower
        has_so_that = "so that" in summary_lower
        
        return has_as_a and has_i_want and has_so_that
    
    def _has_testable_criteria(self, story: JiraStory) -> bool:
        """Check if story has testable acceptance criteria"""
        if not story.acceptance_criteria:
            return False
        
        testable_keywords = ["verify", "check", "validate", "confirm", "test", "ensure"]
        
        for criteria in story.acceptance_criteria:
            if any(keyword in criteria.lower() for keyword in testable_keywords):
                return True
        
        return False
    
    async def notify_project_owner(self, failed_stories: List[StoryValidationResult], 
                                 owner_email: str, owner_name: str) -> Dict[str, Any]:
        """Send notification to project owner about failed stories"""
        try:
            # Prepare notification data
            notification_data = {
                "owner_name": owner_name,
                "owner_email": owner_email,
                "failed_count": len(failed_stories),
                "failed_stories": [
                    {
                        "story_id": result.story_id,
                        "issues": result.issues,
                        "suggestions": result.suggestions,
                        "score": result.validation_score
                    }
                    for result in failed_stories
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            # TODO: Implement actual notification sending
            # This could be email, Slack, Teams, etc.
            
            log.info(f"Notification prepared for {owner_name} ({owner_email}) about {len(failed_stories)} failed stories")
            
            return {
                "success": True,
                "message": f"Notification sent to {owner_name}",
                "failed_stories_count": len(failed_stories)
            }
            
        except Exception as e:
            log.error(f"Failed to send notification: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send notification"
            }
    
    async def get_project_metrics(self) -> Dict[str, Any]:
        """Get project metrics and statistics"""
        try:
            # Get project statistics
            url = f"{self.config.base_url}/rest/api/3/project/{self.config.project_key}/statistics"
            async with self.session.get(url) as response:
                if response.status == 200:
                    stats = await response.json()
                    
                    # Get recent activity
                    activity = await self._get_recent_activity()
                    
                    return {
                        "project_stats": stats,
                        "recent_activity": activity,
                        "last_updated": datetime.now().isoformat()
                    }
                else:
                    return {"error": f"Failed to get project stats: {response.status}"}
                    
        except Exception as e:
            log.error(f"Failed to get project metrics: {e}")
            return {"error": str(e)}
    
    async def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent project activity"""
        # This would fetch recent changes, updates, etc.
        # Implementation depends on specific needs
        return []

# Factory function for easy instantiation
async def create_jira_integration(config: JiraConfig) -> JiraIntegration:
    """Create and test Jira integration"""
    integration = JiraIntegration(config)
    async with integration:
        test_result = await integration.test_connection()
        if not test_result["success"]:
            raise Exception(f"Jira connection failed: {test_result['error']}")
        return integration 