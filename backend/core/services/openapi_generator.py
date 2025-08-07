#!/usr/bin/env python3
"""
🦖 OpenAPI Test Generator for Restaceratops
Automatically generates test cases from OpenAPI/Swagger specifications
"""

import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

log = logging.getLogger("agent.openapi")

class OpenAPITestGenerator:
    """Generate test cases from OpenAPI specifications."""
    
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec = self._load_spec()
        self.base_url = self._get_base_url()
        
    def _load_spec(self) -> Dict:
        """Load OpenAPI specification from file."""
        if not self.spec_path.exists():
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
    
    def _generate_test_data(self, schema: Dict, required: bool = False) -> Any:
        """Generate test data based on JSON schema."""
        if not schema:
            return None
        
        schema_type = schema.get('type', 'string')
        
        if schema_type == 'string':
            if 'enum' in schema:
                return schema['enum'][0] if schema['enum'] else "test"
            elif schema.get('format') == 'email':
                return "test@example.com"
            elif schema.get('format') == 'date':
                return "2024-01-01"
            elif schema.get('format') == 'date-time':
                return "2024-01-01T00:00:00Z"
            else:
                return "test_string"
        
        elif schema_type == 'integer':
            return 1
        
        elif schema_type == 'number':
            return 1.0
        
        elif schema_type == 'boolean':
            return True
        
        elif schema_type == 'array':
            items = schema.get('items', {})
            return [self._generate_test_data(items)]
        
        elif schema_type == 'object':
            properties = schema.get('properties', {})
            required_fields = schema.get('required', [])
            result = {}
            
            for field, field_schema in properties.items():
                is_required = field in required_fields
                if is_required or not required:
                    result[field] = self._generate_test_data(field_schema, is_required)
            
            return result
        
        return None
    
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
    
    def _build_url(self, path: str, path_params: Dict) -> str:
        """Build complete URL with path parameters."""
        url = urljoin(self.base_url, path)
        
        for param_name, param_value in path_params.items():
            url = url.replace(f'{{{param_name}}}', str(param_value))
        
        return url
    
    def generate_tests(self) -> List[Dict]:
        """Generate test cases from OpenAPI specification."""
        tests = []
        paths = self.spec.get('paths', {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    test = self._generate_test_case(path, method, operation)
                    if test:
                        tests.append(test)
        
        return tests
    
    def _generate_test_case(self, path: str, method: str, operation: Dict) -> Optional[Dict]:
        """Generate a single test case."""
        operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_').strip('_')}")
        summary = operation.get('summary', operation_id)
        
        # Generate path parameters
        path_params = self._generate_path_params(path, operation)
        
        # Generate query parameters
        query_params = self._generate_query_params(operation)
        
        # Generate request body
        request_body = self._generate_request_body(operation)
        
        # Build URL
        url = self._build_url(path, path_params)
        
        # Add query parameters to URL
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            url = f"{url}?{query_string}"
        
        # Determine expected status code
        responses = operation.get('responses', {})
        expected_status = 200
        if '201' in responses:
            expected_status = 201
        elif '204' in responses:
            expected_status = 204
        
        # Build test case
        test_case = {
            "name": f"{summary} ({method.upper()})",
            "request": {
                "method": method.upper(),
                "url": url
            },
            "expect": {
                "status": expected_status
            }
        }
        
        # Add request body if present
        if request_body:
            test_case["request"]["json"] = request_body
        
        # Add schema validation if response schema is available
        if '200' in responses:
            content = responses['200'].get('content', {})
            if 'application/json' in content:
                schema = content['application/json'].get('schema', {})
                if schema:
                    test_case["expect"]["schema"] = schema
        
        return test_case
    
    def save_tests(self, output_path: str = "tests/generated_from_openapi.yml"):
        """Generate and save tests to file."""
        tests = self.generate_tests()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            yaml.dump(tests, f, default_flow_style=False, sort_keys=False)
        
        log.info(f"Generated {len(tests)} test cases to {output_file}")
        return output_file

def main():
    """Command line interface for OpenAPI test generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate test cases from OpenAPI specification")
    parser.add_argument("spec_file", help="Path to OpenAPI specification file")
    parser.add_argument("--output", "-o", default="tests/generated_from_openapi.yml", 
                       help="Output file path")
    
    args = parser.parse_args()
    
    try:
        generator = OpenAPITestGenerator(args.spec_file)
        output_file = generator.save_tests(args.output)
        print(f"✅ Generated {len(generator.generate_tests())} test cases to {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 