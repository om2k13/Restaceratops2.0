#!/usr/bin/env python3
"""
🦖 Authentication Manager for Restaceratops
Comprehensive API key and authentication management system
"""

import os
import json
import logging
import base64
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from cryptography.fernet import Fernet
import keyring

log = logging.getLogger("agent.auth")

@dataclass
class APICredentials:
    """Represents API credentials for different authentication methods."""
    name: str
    type: str  # 'bearer', 'api_key', 'oauth2', 'basic'
    value: str
    header_name: Optional[str] = None
    base_url: Optional[str] = None
    description: Optional[str] = None
    expires_at: Optional[str] = None

class AuthManager:
    """Manages API credentials and authentication for Restaceratops."""
    
    def __init__(self, config_dir: str = "~/.restaceratops"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(exist_ok=True)
        self.credentials_file = self.config_dir / "credentials.json"
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self.credentials = self._load_credentials()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for secure credential storage."""
        key_name = "restaceratops_encryption_key"
        try:
            key = keyring.get_password("restaceratops", key_name)
            if key:
                return base64.urlsafe_b64decode(key)
        except Exception:
            pass
        
        # Create new key
        new_key = Fernet.generate_key()
        try:
            keyring.set_password("restaceratops", key_name, base64.urlsafe_b64encode(new_key).decode())
        except Exception as e:
            log.warning(f"Could not store encryption key in keyring: {e}")
        return new_key
    
    def _encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.fernet.encrypt(data.encode()).decode()
    
    def _decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def _load_credentials(self) -> Dict[str, APICredentials]:
        """Load encrypted credentials from file."""
        if not self.credentials_file.exists():
            return {}
        
        try:
            with open(self.credentials_file, 'r') as f:
                encrypted_data = json.load(f)
            
            credentials = {}
            for name, cred_data in encrypted_data.items():
                credentials[name] = APICredentials(
                    name=name,
                    type=cred_data['type'],
                    value=self._decrypt(cred_data['value']),
                    header_name=cred_data.get('header_name'),
                    base_url=cred_data.get('base_url'),
                    description=cred_data.get('description'),
                    expires_at=cred_data.get('expires_at')
                )
            return credentials
        except Exception as e:
            log.error(f"Failed to load credentials: {e}")
            return {}
    
    def _save_credentials(self):
        """Save encrypted credentials to file."""
        encrypted_data = {}
        for name, cred in self.credentials.items():
            encrypted_data[name] = {
                'type': cred.type,
                'value': self._encrypt(cred.value),
                'header_name': cred.header_name,
                'base_url': cred.base_url,
                'description': cred.description,
                'expires_at': cred.expires_at
            }
        
        with open(self.credentials_file, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
    
    def add_credentials(self, name: str, cred_type: str, value: str, 
                       header_name: Optional[str] = None, base_url: Optional[str] = None,
                       description: Optional[str] = None) -> bool:
        """Add new API credentials."""
        try:
            self.credentials[name] = APICredentials(
                name=name,
                type=cred_type,
                value=value,
                header_name=header_name,
                base_url=base_url,
                description=description
            )
            self._save_credentials()
            log.info(f"Added credentials: {name}")
            return True
        except Exception as e:
            log.error(f"Failed to add credentials: {e}")
            return False
    
    def get_credentials(self, name: str) -> Optional[APICredentials]:
        """Get credentials by name."""
        return self.credentials.get(name)
    
    def list_credentials(self) -> List[Dict[str, Any]]:
        """List all stored credentials (without sensitive values)."""
        return [
            {
                'name': cred.name,
                'type': cred.type,
                'header_name': cred.header_name,
                'base_url': cred.base_url,
                'description': cred.description,
                'expires_at': cred.expires_at
            }
            for cred in self.credentials.values()
        ]
    
    def remove_credentials(self, name: str) -> bool:
        """Remove credentials by name."""
        if name in self.credentials:
            del self.credentials[name]
            self._save_credentials()
            log.info(f"Removed credentials: {name}")
            return True
        return False
    
    def get_auth_headers(self, name: str) -> Dict[str, str]:
        """Get authentication headers for the specified credentials."""
        cred = self.get_credentials(name)
        if not cred:
            return {}
        
        if cred.type == 'bearer':
            return {'Authorization': f'Bearer {cred.value}'}
        elif cred.type == 'api_key':
            header_name = cred.header_name or 'X-API-Key'
            return {header_name: cred.value}
        elif cred.type == 'basic':
            return {'Authorization': f'Basic {cred.value}'}
        elif cred.type == 'oauth2':
            return {'Authorization': f'Bearer {cred.value}'}
        
        return {}
    
    def validate_credentials(self, name: str) -> bool:
        """Validate that credentials exist and are not expired."""
        cred = self.get_credentials(name)
        if not cred:
            return False
        
        # Check if expired
        if cred.expires_at:
            from datetime import datetime
            try:
                expires = datetime.fromisoformat(cred.expires_at.replace('Z', '+00:00'))
                if datetime.now().replace(tzinfo=expires.tzinfo) > expires:
                    log.warning(f"Credentials {name} have expired")
                    return False
            except Exception as e:
                log.warning(f"Could not parse expiration date: {e}")
        
        return True

def main():
    """Command line interface for credential management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage API credentials for Restaceratops")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add credentials
    add_parser = subparsers.add_parser('add', help='Add new credentials')
    add_parser.add_argument('name', help='Credential name')
    add_parser.add_argument('type', choices=['bearer', 'api_key', 'oauth2', 'basic'], 
                           help='Credential type')
    add_parser.add_argument('value', help='Credential value')
    add_parser.add_argument('--header-name', help='Header name for API key')
    add_parser.add_argument('--base-url', help='Base URL for the API')
    add_parser.add_argument('--description', help='Description')
    
    # List credentials
    subparsers.add_parser('list', help='List all credentials')
    
    # Remove credentials
    remove_parser = subparsers.add_parser('remove', help='Remove credentials')
    remove_parser.add_argument('name', help='Credential name to remove')
    
    # Validate credentials
    validate_parser = subparsers.add_parser('validate', help='Validate credentials')
    validate_parser.add_argument('name', help='Credential name to validate')
    
    args = parser.parse_args()
    
    auth_manager = AuthManager()
    
    if args.command == 'add':
        success = auth_manager.add_credentials(
            args.name, args.type, args.value,
            args.header_name, args.base_url, args.description
        )
        if success:
            print(f"✅ Added credentials: {args.name}")
        else:
            print(f"❌ Failed to add credentials: {args.name}")
    
    elif args.command == 'list':
        credentials = auth_manager.list_credentials()
        if credentials:
            print("📋 Stored Credentials:")
            for cred in credentials:
                print(f"  • {cred['name']} ({cred['type']})")
                if cred['description']:
                    print(f"    Description: {cred['description']}")
                if cred['base_url']:
                    print(f"    Base URL: {cred['base_url']}")
                print()
        else:
            print("📋 No credentials stored")
    
    elif args.command == 'remove':
        if auth_manager.remove_credentials(args.name):
            print(f"✅ Removed credentials: {args.name}")
        else:
            print(f"❌ Credentials not found: {args.name}")
    
    elif args.command == 'validate':
        if auth_manager.validate_credentials(args.name):
            print(f"✅ Credentials valid: {args.name}")
        else:
            print(f"❌ Credentials invalid or expired: {args.name}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 