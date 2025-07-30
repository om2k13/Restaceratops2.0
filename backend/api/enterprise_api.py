"""
Enterprise API for Restaceratops Phase 4
Provides endpoints for multi-platform testing, CI/CD integration, monitoring, and security.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..core.services.enterprise_manager import (
    EnterpriseManager, PlatformConfig, CICDConfig, MonitoringConfig, 
    SecurityConfig, PlatformType, IntegrationType, SecurityLevel,
    enterprise_manager
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/enterprise", tags=["enterprise"])

# Pydantic models for API requests/responses
class PlatformConfigRequest(BaseModel):
    name: str
    platform_type: PlatformType
    base_url: str
    authentication: Dict[str, Any] = {}
    headers: Dict[str, str] = {}
    timeout: int = 30
    retry_attempts: int = 3
    custom_assertions: List[str] = None
    platform_specific_tests: List[str] = None


class CICDConfigRequest(BaseModel):
    name: str
    integration_type: IntegrationType
    webhook_url: str
    api_key: str
    project_id: str
    branch: str = "main"
    trigger_on_push: bool = True
    trigger_on_pr: bool = True
    custom_headers: Dict[str, str] = None


class MonitoringConfigRequest(BaseModel):
    name: str
    enabled: bool = True
    metrics_endpoint: str = None
    alert_webhook: str = None
    health_check_interval: int = 60
    performance_thresholds: Dict[str, float] = None
    notification_channels: List[str] = None


class SecurityConfigRequest(BaseModel):
    name: str
    rbac_enabled: bool = True
    audit_logging: bool = True
    encryption_enabled: bool = True
    session_timeout: int = 3600
    max_login_attempts: int = 5
    password_policy: Dict[str, Any] = None
    compliance_standards: List[str] = None


class AuthenticationRequest(BaseModel):
    username: str
    password: str


class CICDTriggerRequest(BaseModel):
    event_type: str = "push"
    additional_data: Dict[str, Any] = None


class ComplianceReportRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include_audit_logs: bool = True


# Dependency for authentication
async def get_current_user(authorization: str = Header(None)):
    """Get current user from authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    user_data = await enterprise_manager.validate_session(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user_data


# Platform Management Endpoints
@router.post("/platforms")
async def add_platform_config(
    request: PlatformConfigRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a new platform configuration."""
    try:
        config = PlatformConfig(
            platform_type=request.platform_type,
            base_url=request.base_url,
            authentication=request.authentication,
            headers=request.headers,
            timeout=request.timeout,
            retry_attempts=request.retry_attempts,
            custom_assertions=request.custom_assertions,
            platform_specific_tests=request.platform_specific_tests
        )
        
        success = await enterprise_manager.add_platform_config(request.name, config)
        
        if success:
            return {
                "success": True,
                "message": f"Platform configuration '{request.name}' added successfully",
                "platform": {
                    "name": request.name,
                    "type": request.platform_type.value,
                    "base_url": request.base_url
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add platform configuration")
            
    except Exception as e:
        logger.error(f"Error adding platform config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms")
async def list_platforms(current_user: Dict[str, Any] = Depends(get_current_user)):
    """List all available platforms."""
    try:
        platforms = await enterprise_manager.list_platforms()
        platform_details = []
        
        for platform_name in platforms:
            config = await enterprise_manager.get_platform_config(platform_name)
            if config:
                platform_details.append({
                    "name": platform_name,
                    "type": config.platform_type.value,
                    "base_url": config.base_url,
                    "timeout": config.timeout,
                    "retry_attempts": config.retry_attempts
                })
        
        return {
            "success": True,
            "platforms": platform_details,
            "count": len(platform_details)
        }
        
    except Exception as e:
        logger.error(f"Error listing platforms: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms/{platform_name}")
async def get_platform_config(
    platform_name: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get platform configuration by name."""
    try:
        config = await enterprise_manager.get_platform_config(platform_name)
        
        if not config:
            raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")
        
        return {
            "success": True,
            "platform": {
                "name": platform_name,
                "type": config.platform_type.value,
                "base_url": config.base_url,
                "authentication": config.authentication,
                "headers": config.headers,
                "timeout": config.timeout,
                "retry_attempts": config.retry_attempts,
                "custom_assertions": config.custom_assertions,
                "platform_specific_tests": config.platform_specific_tests
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting platform config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# CI/CD Integration Endpoints
@router.post("/cicd")
async def add_cicd_config(
    request: CICDConfigRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a new CI/CD configuration."""
    try:
        config = CICDConfig(
            integration_type=request.integration_type,
            webhook_url=request.webhook_url,
            api_key=request.api_key,
            project_id=request.project_id,
            branch=request.branch,
            trigger_on_push=request.trigger_on_push,
            trigger_on_pr=request.trigger_on_pr,
            custom_headers=request.custom_headers
        )
        
        success = await enterprise_manager.add_cicd_config(request.name, config)
        
        if success:
            return {
                "success": True,
                "message": f"CI/CD configuration '{request.name}' added successfully",
                "cicd": {
                    "name": request.name,
                    "type": request.integration_type.value,
                    "project_id": request.project_id,
                    "branch": request.branch
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add CI/CD configuration")
            
    except Exception as e:
        logger.error(f"Error adding CI/CD config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cicd")
async def list_cicd_configs(current_user: Dict[str, Any] = Depends(get_current_user)):
    """List all CI/CD configurations."""
    try:
        cicd_configs = []
        
        for name, config in enterprise_manager.cicd_configs.items():
            cicd_configs.append({
                "name": name,
                "type": config.integration_type.value,
                "project_id": config.project_id,
                "branch": config.branch,
                "trigger_on_push": config.trigger_on_push,
                "trigger_on_pr": config.trigger_on_pr
            })
        
        return {
            "success": True,
            "cicd_configs": cicd_configs,
            "count": len(cicd_configs)
        }
        
    except Exception as e:
        logger.error(f"Error listing CI/CD configs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cicd/{config_name}/trigger")
async def trigger_cicd_pipeline(
    config_name: str,
    request: CICDTriggerRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Trigger a CI/CD pipeline."""
    try:
        success = await enterprise_manager.trigger_cicd_pipeline(
            config_name, 
            request.event_type
        )
        
        if success:
            return {
                "success": True,
                "message": f"CI/CD pipeline '{config_name}' triggered successfully",
                "event_type": request.event_type,
                "triggered_by": current_user.get("user_id")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to trigger CI/CD pipeline")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering CI/CD pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Monitoring Endpoints
@router.post("/monitoring")
async def add_monitoring_config(
    request: MonitoringConfigRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a new monitoring configuration."""
    try:
        config = MonitoringConfig(
            enabled=request.enabled,
            metrics_endpoint=request.metrics_endpoint,
            alert_webhook=request.alert_webhook,
            health_check_interval=request.health_check_interval,
            performance_thresholds=request.performance_thresholds,
            notification_channels=request.notification_channels
        )
        
        enterprise_manager.monitoring_configs[request.name] = config
        
        return {
            "success": True,
            "message": f"Monitoring configuration '{request.name}' added successfully",
            "monitoring": {
                "name": request.name,
                "enabled": request.enabled,
                "health_check_interval": request.health_check_interval,
                "notification_channels": request.notification_channels
            }
        }
        
    except Exception as e:
        logger.error(f"Error adding monitoring config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring")
async def list_monitoring_configs(current_user: Dict[str, Any] = Depends(get_current_user)):
    """List all monitoring configurations."""
    try:
        monitoring_configs = []
        
        for name, config in enterprise_manager.monitoring_configs.items():
            monitoring_configs.append({
                "name": name,
                "enabled": config.enabled,
                "health_check_interval": config.health_check_interval,
                "notification_channels": config.notification_channels,
                "performance_thresholds": config.performance_thresholds
            })
        
        return {
            "success": True,
            "monitoring_configs": monitoring_configs,
            "count": len(monitoring_configs)
        }
        
    except Exception as e:
        logger.error(f"Error listing monitoring configs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/{config_name}/metrics")
async def get_performance_metrics(
    config_name: str,
    hours: int = 24,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get performance metrics for a monitoring configuration."""
    try:
        metrics = await enterprise_manager.get_performance_metrics(config_name, hours)
        
        return {
            "success": True,
            "config_name": config_name,
            "hours": hours,
            "metrics": metrics,
            "count": len(metrics)
        }
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Security Endpoints
@router.post("/security")
async def add_security_config(
    request: SecurityConfigRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add a new security configuration."""
    try:
        config = SecurityConfig(
            rbac_enabled=request.rbac_enabled,
            audit_logging=request.audit_logging,
            encryption_enabled=request.encryption_enabled,
            session_timeout=request.session_timeout,
            max_login_attempts=request.max_login_attempts,
            password_policy=request.password_policy,
            compliance_standards=request.compliance_standards
        )
        
        enterprise_manager.security_configs[request.name] = config
        
        return {
            "success": True,
            "message": f"Security configuration '{request.name}' added successfully",
            "security": {
                "name": request.name,
                "rbac_enabled": request.rbac_enabled,
                "audit_logging": request.audit_logging,
                "encryption_enabled": request.encryption_enabled,
                "session_timeout": request.session_timeout,
                "compliance_standards": request.compliance_standards
            }
        }
        
    except Exception as e:
        logger.error(f"Error adding security config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/login")
async def authenticate_user(request: AuthenticationRequest):
    """Authenticate a user and return session token."""
    try:
        user_data = await enterprise_manager.authenticate_user(
            request.username, 
            request.password
        )
        
        if user_data:
            return {
                "success": True,
                "message": "Authentication successful",
                "user": {
                    "user_id": user_data["user_id"],
                    "username": user_data["username"],
                    "role": user_data["role"],
                    "permissions": user_data["permissions"]
                },
                "session_token": user_data["session_token"]
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")


@router.get("/auth/validate")
async def validate_session(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Validate current session."""
    return {
        "success": True,
        "message": "Session is valid",
        "user": {
            "user_id": current_user["user_id"],
            "role": current_user.get("role"),
            "permissions": current_user.get("permissions", [])
        }
    }


# Audit and Compliance Endpoints
@router.get("/audit/logs")
async def get_audit_logs(
    user_id: str = None,
    action: str = None,
    resource: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get audit logs with optional filtering."""
    try:
        # Parse dates
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        logs = await enterprise_manager.get_audit_logs(
            user_id=user_id,
            action=action,
            resource=resource,
            start_date=start_dt,
            end_date=end_dt
        )
        
        # Apply limit
        logs = logs[-limit:] if limit > 0 else logs
        
        # Convert to dict for JSON serialization
        log_dicts = []
        for log in logs:
            log_dict = {
                "timestamp": log.timestamp.isoformat(),
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "details": log.details,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "success": log.success
            }
            log_dicts.append(log_dict)
        
        return {
            "success": True,
            "audit_logs": log_dicts,
            "count": len(log_dicts),
            "filters": {
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compliance/report")
async def generate_compliance_report(
    request: ComplianceReportRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate a compliance report."""
    try:
        # Parse dates
        start_date = None
        end_date = None
        
        if request.start_date:
            start_date = datetime.fromisoformat(request.start_date.replace('Z', '+00:00'))
        if request.end_date:
            end_date = datetime.fromisoformat(request.end_date.replace('Z', '+00:00'))
        
        report = await enterprise_manager.generate_compliance_report(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "success": True,
            "compliance_report": report
        }
        
    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health and Status Endpoints
@router.get("/health")
async def get_health_status():
    """Get system health status."""
    try:
        health_status = await enterprise_manager._perform_health_check()
        
        return {
            "success": True,
            "health": health_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_system_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get comprehensive system status."""
    try:
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "platforms": {
                "count": len(enterprise_manager.platform_configs),
                "names": list(enterprise_manager.platform_configs.keys())
            },
            "cicd": {
                "count": len(enterprise_manager.cicd_configs),
                "names": list(enterprise_manager.cicd_configs.keys())
            },
            "monitoring": {
                "count": len(enterprise_manager.monitoring_configs),
                "enabled": sum(1 for config in enterprise_manager.monitoring_configs.values() if config.enabled)
            },
            "security": {
                "count": len(enterprise_manager.security_configs),
                "audit_logs": len(enterprise_manager.audit_logs),
                "active_sessions": len(enterprise_manager.active_sessions)
            },
            "performance": {
                "metrics_count": sum(len(metrics) for metrics in enterprise_manager.performance_metrics.values())
            }
        }
        
        return {
            "success": True,
            "system_status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Initialize enterprise manager
async def initialize_enterprise_manager():
    """Initialize enterprise manager."""
    try:
        await enterprise_manager.initialize()
        logger.info("Enterprise API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Enterprise API: {e}")
        raise

# Initialize enterprise manager when the module is imported
# This will be called by the main app's lifespan manager
enterprise_manager_initialized = False

def ensure_enterprise_manager_initialized():
    """Ensure enterprise manager is initialized."""
    global enterprise_manager_initialized
    if not enterprise_manager_initialized:
        try:
            # This will be handled by the main app's lifespan
            enterprise_manager_initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Enterprise API: {e}") 