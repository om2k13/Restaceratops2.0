#!/usr/bin/env python3
"""
🦖 Enhanced OpenAPI Test Generator for Restaceratops
Advanced test generation from OpenAPI/Swagger specifications with security support
"""

import yaml
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urljoin, urlparse
from backend.core.models.auth_manager import AuthManager

log = logging.getLogger("agent.enhanced_openapi")

class EnhancedOpenAPIGenerator:
    """Enhanced test generator with security schemes and advanced features."""
    
    def __init__(self, spec_path: str, auth_manager: Optional[AuthManager] = None):
        self.spec_path = Path(spec_path)
        self.spec = self._load_spec()
        self.base_url = self._get_base_url()
        self.auth_manager = auth_manager or AuthManager()
        self.security_schemes = self._extract_security_schemes()
        
    def _load_spec(self) -> Dict:
        """Load OpenAPI specification from file or URL."""
        if not self.spec_path.exists():
            # Try to load from URL
            if str(self.spec_path).startswith(('http://', 'https://')):
                import httpx
                try:
                    with httpx.Client() as client:
                        response = client.get(str(self.spec_path))
                        response.raise_for_status()
                        content = response.text
                        if self.spec_path.suffix in ['.yaml', '.yml']:
                            return yaml.safe_load(content)
                        else:
                            return json.loads(content)
                except Exception as e:
                    raise FileNotFoundError(f"Could not load OpenAPI spec from {self.spec_path}: {e}")
            else:
                raise FileNotFoundError(f"OpenAPI spec not found: {self.spec_path}")
        
        with open(self.spec_path, 'r') as f:
            if self.spec_path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def _get_base_url(self) -> str:
        """Extract base URL from OpenAPI spec."""
        servers = self.spec.get('servers', [])
        if servers:
            return servers[0].get('url', 'http://localhost:8000')
        return 'http://localhost:8000'
    
    def _extract_security_schemes(self) -> Dict[str, Dict]:
        """Extract security schemes from OpenAPI spec."""
        components = self.spec.get('components', {})
        return components.get('securitySchemes', {})
    
    def _generate_test_data(self, schema: Dict, required: bool = False) -> Any:
        """Generate realistic test data based on JSON schema."""
        if not schema:
            return None
        
        schema_type = schema.get('type', 'string')
        
        # Handle references
        if '$ref' in schema:
            ref_path = schema['$ref']
            if ref_path.startswith('#/components/schemas/'):
                schema_name = ref_path.split('/')[-1]
                components = self.spec.get('components', {})
                schemas = components.get('schemas', {})
                if schema_name in schemas:
                    return self._generate_test_data(schemas[schema_name], required)
        
        # Handle examples
        if 'example' in schema:
            return schema['example']
        
        if schema_type == 'string':
            if 'enum' in schema:
                return schema['enum'][0] if schema['enum'] else "test"
            elif schema.get('format') == 'email':
                return "test@example.com"
            elif schema.get('format') == 'date':
                return "2024-01-01"
            elif schema.get('format') == 'date-time':
                return "2024-01-01T00:00:00Z"
            elif schema.get('format') == 'uuid':
                return "123e4567-e89b-12d3-a456-426614174000"
            elif schema.get('format') == 'uri':
                return "https://example.com"
            elif schema.get('format') == 'ipv4':
                return "192.168.1.1"
            elif schema.get('format') == 'ipv6':
                return "2001:db8::1"
            else:
                # Generate realistic string based on property name
                property_name = getattr(schema, 'property_name', 'test')
                if isinstance(property_name, str) and 'name' in property_name.lower():
                    return "Test User"
                elif isinstance(property_name, str) and 'email' in property_name.lower():
                    return "test@example.com"
                elif isinstance(property_name, str) and 'description' in property_name.lower():
                    return "This is a test description"
                elif isinstance(property_name, str) and 'title' in property_name.lower():
                    return "Test Title"
                else:
                    return "test_string"
        
        elif schema_type == 'integer':
            if 'minimum' in schema and 'maximum' in schema:
                return (schema['minimum'] + schema['maximum']) // 2
            elif 'minimum' in schema:
                return schema['minimum'] + 1
            elif 'maximum' in schema:
                return schema['maximum'] - 1
            else:
                return 1
        
        elif schema_type == 'number':
            if 'minimum' in schema and 'maximum' in schema:
                return (schema['minimum'] + schema['maximum']) / 2
            else:
                return 1.0
        
        elif schema_type == 'boolean':
            return True
        
        elif schema_type == 'array':
            items = schema.get('items', {})
            min_items = schema.get('minItems', 1)
            max_items = schema.get('maxItems', 3)
            count = min(min_items, max_items)
            return [self._generate_test_data(items) for _ in range(count)]
        
        elif schema_type == 'object':
            properties = schema.get('properties', {})
            required_fields = schema.get('required', [])
            result = {}
            
            for field, field_schema in properties.items():
                is_required = field in required_fields
                if is_required or not required:
                    # Create a copy of the schema with property_name
                    field_schema_copy = field_schema.copy()
                    field_schema_copy['property_name'] = field
                    result[field] = self._generate_test_data(field_schema_copy, is_required)
            
            return result
        
        return None
    
    def _generate_path_params(self, path: str, operation: Dict) -> Dict:
        """Generate path parameters."""
        params = {}
        path_params = operation.get('parameters', [])
        
        for param in path_params:
            if param.get('in') == 'path':
                param_name = param['name']
                param_schema = param.get('schema', {})
                params[param_name] = self._generate_test_data(param_schema)
        
        return params
    
    def _generate_query_params(self, operation: Dict) -> Dict:
        """Generate query parameters."""
        params = {}
        query_params = operation.get('parameters', [])
        
        for param in query_params:
            if param.get('in') == 'query':
                param_name = param['name']
                param_schema = param.get('schema', {})
                params[param_name] = self._generate_test_data(param_schema)
        
        return params
    
    def _generate_request_body(self, operation: Dict) -> Optional[Dict]:
        """Generate request body for POST/PUT operations."""
        request_body = operation.get('requestBody', {})
        if not request_body:
            return None
        
        content = request_body.get('content', {})
        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})
            return self._generate_test_data(schema)
        
        return None
    
    def _build_url(self, path: str, path_params: Dict) -> str:
        """Build complete URL with path parameters."""
        url = urljoin(self.base_url, path)
        
        for param_name, param_value in path_params.items():
            url = url.replace(f'{{{param_name}}}', str(param_value))
        
        return url
    
    def _generate_security_headers(self, operation: Dict) -> Dict[str, str]:
        """Generate security headers based on operation security requirements."""
        security = operation.get('security', [])
        if not security:
            # Use global security
            security = self.spec.get('security', [])
        
        headers = {}
        for security_req in security:
            for scheme_name, scopes in security_req.items():
                if scheme_name in self.security_schemes:
                    scheme = self.security_schemes[scheme_name]
                    scheme_type = scheme.get('type', '')
                    
                    if scheme_type == 'http':
                        if scheme.get('scheme') == 'bearer':
                            # Try to get bearer token from auth manager
                            cred = self.auth_manager.get_credentials(f"{scheme_name}_token")
                            if cred:
                                headers['Authorization'] = f"Bearer {cred.value}"
                        elif scheme.get('scheme') == 'basic':
                            cred = self.auth_manager.get_credentials(f"{scheme_name}_basic")
                            if cred:
                                headers['Authorization'] = f"Basic {cred.value}"
                    
                    elif scheme_type == 'apiKey':
                        header_name = scheme.get('name', 'X-API-Key')
                        cred = self.auth_manager.get_credentials(f"{scheme_name}_key")
                        if cred:
                            headers[header_name] = cred.value
                    
                    elif scheme_type == 'oauth2':
                        cred = self.auth_manager.get_credentials(f"{scheme_name}_oauth")
                        if cred:
                            headers['Authorization'] = f"Bearer {cred.value}"
        
        return headers
    
    def _generate_test_case(self, path: str, method: str, operation: Dict) -> Optional[Dict]:
        """Generate a comprehensive test case with security and validation."""
        operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_').strip('_')}")
        summary = operation.get('summary', operation_id)
        description = operation.get('description', '')
        
        # Generate path parameters
        path_params = self._generate_path_params(path, operation)
        
        # Generate query parameters
        query_params = self._generate_query_params(operation)
        
        # Generate request body
        request_body = self._generate_request_body(operation)
        
        # Generate security headers
        security_headers = self._generate_security_headers(operation)
        
        # Build URL
        url = self._build_url(path, path_params)
        
        # Add query parameters to URL
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            url = f"{url}?{query_string}"
        
        # Determine expected status codes
        responses = operation.get('responses', {})
        expected_statuses = self._get_expected_status_codes(responses)
        
        # Build test case
        test_case = {
            "name": f"{summary} ({method.upper()})",
            "description": description,
            "request": {
                "method": method.upper(),
                "url": url
            },
            "expect": {
                "status": expected_statuses[0] if expected_statuses else 200
            }
        }
        
        # Add request body if present
        if request_body:
            test_case["request"]["json"] = request_body
        
        # Add security headers
        if security_headers:
            test_case["request"]["headers"] = security_headers
        
        # Add schema validation for successful responses
        if '200' in responses:
            content = responses['200'].get('content', {})
            if 'application/json' in content:
                schema = content['application/json'].get('schema', {})
                if schema:
                    test_case["expect"]["schema"] = schema
        
        # Add variable capture for authentication flows
        if 'access_token' in str(responses) or 'token' in str(responses):
            test_case["expect"]["save"] = {
                "access_token": "$.access_token",
                "token_type": "$.token_type"
            }
        
        return test_case
    
    def _get_expected_status_codes(self, responses: Dict) -> List[int]:
        """Get expected status codes from responses."""
        status_codes = []
        for status in responses.keys():
            try:
                status_codes.append(int(status))
            except ValueError:
                pass
        
        # Sort by priority: 2xx, 4xx, 5xx
        status_codes.sort(key=lambda x: (x // 100, x))
        return status_codes
    
    def generate_tests(self, include_security: bool = True) -> List[Dict]:
        """Generate comprehensive test cases from OpenAPI specification."""
        tests = []
        paths = self.spec.get('paths', {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    test = self._generate_test_case(path, method, operation)
                    if test:
                        tests.append(test)
        
        return tests
    
    def generate_security_tests(self) -> List[Dict]:
        """Generate security-focused test cases."""
        security_tests = []
        paths = self.spec.get('paths', {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    # Test without authentication
                    test = self._generate_test_case(path, method, operation)
                    if test and test.get('request', {}).get('headers'):
                        # Create unauthorized test
                        unauthorized_test = test.copy()
                        unauthorized_test['name'] = f"{test['name']} - Unauthorized"
                        unauthorized_test['request']['headers'] = {}
                        unauthorized_test['expect']['status'] = 401
                        security_tests.append(unauthorized_test)
                        
                        # Create invalid token test
                        invalid_test = test.copy()
                        invalid_test['name'] = f"{test['name']} - Invalid Token"
                        invalid_test['request']['headers'] = {'Authorization': 'Bearer invalid_token'}
                        invalid_test['expect']['status'] = 401
                        security_tests.append(invalid_test)
        
        return security_tests
    
    def save_tests(self, output_path: str = "tests/generated_from_openapi.yml", 
                   include_security: bool = True) -> Path:
        """Generate and save tests to file."""
        tests = self.generate_tests(include_security)
        
        if include_security:
            security_tests = self.generate_security_tests()
            tests.extend(security_tests)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            yaml.dump(tests, f, default_flow_style=False, sort_keys=False)
        
        log.info(f"Generated {len(tests)} test cases to {output_file}")
        return output_file

def main():
    """Command line interface for enhanced OpenAPI test generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate enhanced test cases from OpenAPI specification")
    parser.add_argument("spec_file", help="Path to OpenAPI specification file or URL")
    parser.add_argument("--output", "-o", default="tests/generated_from_openapi.yml", 
                       help="Output file path")
    parser.add_argument("--no-security", action="store_true", 
                       help="Skip security test generation")
    parser.add_argument("--auth-config", help="Path to authentication configuration")
    
    args = parser.parse_args()
    
    try:
        generator = EnhancedOpenAPIGenerator(args.spec_file)
        output_file = generator.save_tests(args.output, include_security=not args.no_security)
        print(f"✅ Generated {len(generator.generate_tests())} test cases to {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main() 