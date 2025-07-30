#!/usr/bin/env python3
"""
🦖 Test Input Manager for Restaceratops
Advanced test input management with dynamic data generation and external sources
"""

import yaml
import json
import csv
import logging
import random
import string
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import faker
from .auth_manager import AuthManager

log = logging.getLogger("agent.test_input")

class TestInputManager:
    """Manages test inputs with dynamic data generation and external sources."""
    
    def __init__(self, auth_manager: Optional[AuthManager] = None):
        self.auth_manager = auth_manager or AuthManager()
        self.fake = faker.Faker()
        self.context = {}
        self.data_sources = {}
        self.templates = {}
        
    def add_data_source(self, name: str, source_type: str, source_path: str, 
                       options: Optional[Dict] = None) -> bool:
        """Add external data source for test inputs."""
        try:
            self.data_sources[name] = {
                'type': source_type,
                'path': source_path,
                'options': options or {},
                'data': self._load_data_source(source_type, source_path, options)
            }
            log.info(f"Added data source: {name}")
            return True
        except Exception as e:
            log.error(f"Failed to add data source {name}: {e}")
            return False
    
    def _load_data_source(self, source_type: str, source_path: str, options: Dict) -> List[Dict]:
        """Load data from external source."""
        path = Path(source_path)
        
        if source_type == 'csv':
            data = []
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        
        elif source_type == 'json':
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif source_type == 'yaml':
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        elif source_type == 'api':
            # Load data from API endpoint
            import httpx
            with httpx.Client() as client:
                response = client.get(source_path)
                response.raise_for_status()
                return response.json()
        
        else:
            raise ValueError(f"Unsupported data source type: {source_type}")
    
    def add_template(self, name: str, template: Dict) -> bool:
        """Add test data template."""
        try:
            self.templates[name] = template
            log.info(f"Added template: {name}")
            return True
        except Exception as e:
            log.error(f"Failed to add template {name}: {e}")
            return False
    
    def generate_test_data(self, template_name: str, count: int = 1, 
                          context: Optional[Dict] = None) -> List[Dict]:
        """Generate test data using template and dynamic generation."""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        
        template = self.templates[template_name]
        context = context or {}
        
        results = []
        for i in range(count):
            data = self._process_template(template, context, i)
            results.append(data)
        
        return results
    
    def _process_template(self, template: Any, context: Dict, index: int) -> Any:
        """Process template with dynamic data generation."""
        if isinstance(template, dict):
            result = {}
            for key, value in template.items():
                result[key] = self._process_template(value, context, index)
            return result
        
        elif isinstance(template, list):
            return [self._process_template(item, context, index) for item in template]
        
        elif isinstance(template, str):
            return self._process_string_template(template, context, index)
        
        else:
            return template
    
    def _process_string_template(self, template: str, context: Dict, index: int) -> str:
        """Process string template with dynamic functions and variables."""
        # Handle dynamic functions
        if '{{' in template and '}}' in template:
            import re
            
            def replace_function(match):
                func_call = match.group(1).strip()
                return self._execute_function(func_call, context, index)
            
            template = re.sub(r'\{\{([^}]+)\}\}', replace_function, template)
        
        # Handle context variables
        if '{' in template and '}' in template:
            template = template.format(**context, index=index)
        
        return template
    
    def _execute_function(self, func_call: str, context: Dict, index: int) -> str:
        """Execute dynamic function in template."""
        func_name = func_call.split('(')[0].strip()
        args_str = func_call.split('(')[1].split(')')[0].strip()
        
        # Parse arguments
        args = []
        if args_str:
            for arg in args_str.split(','):
                arg = arg.strip().strip('"\'')
                args.append(arg)
        
        # Execute function
        if func_name == 'fake':
            return self._execute_fake_function(args)
        elif func_name == 'random':
            return self._execute_random_function(args)
        elif func_name == 'sequence':
            return self._execute_sequence_function(args, index)
        elif func_name == 'data_source':
            return self._execute_data_source_function(args)
        elif func_name == 'auth':
            return self._execute_auth_function(args)
        else:
            return f"{{UNKNOWN_FUNCTION: {func_call}}}"
    
    def _execute_fake_function(self, args: List[str]) -> str:
        """Execute faker function."""
        if not args:
            return self.fake.word()
        
        method_name = args[0]
        if hasattr(self.fake, method_name):
            method = getattr(self.fake, method_name)
            return str(method())
        else:
            return f"{{INVALID_FAKE_METHOD: {method_name}}}"
    
    def _execute_random_function(self, args: List[str]) -> str:
        """Execute random function."""
        if not args:
            return str(random.randint(1, 100))
        
        func_type = args[0]
        if func_type == 'int':
            min_val = int(args[1]) if len(args) > 1 else 1
            max_val = int(args[2]) if len(args) > 2 else 100
            return str(random.randint(min_val, max_val))
        elif func_type == 'choice':
            choices = args[1:]
            return random.choice(choices)
        elif func_type == 'string':
            length = int(args[1]) if len(args) > 1 else 10
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        else:
            return str(random.randint(1, 100))
    
    def _execute_sequence_function(self, args: List[str], index: int) -> str:
        """Execute sequence function."""
        if not args:
            return str(index + 1)
        
        start = int(args[0]) if args[0].isdigit() else 1
        step = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
        
        return str(start + (index * step))
    
    def _execute_data_source_function(self, args: List[str]) -> str:
        """Execute data source function."""
        if not args:
            return "{{NO_DATA_SOURCE_SPECIFIED}}"
        
        source_name = args[0]
        if source_name not in self.data_sources:
            return f"{{DATA_SOURCE_NOT_FOUND: {source_name}}}"
        
        data = self.data_sources[source_name]['data']
        if not data:
            return "{{EMPTY_DATA_SOURCE}}"
        
        # Get random item from data source
        item = random.choice(data)
        
        if len(args) > 1:
            field = args[1]
            return str(item.get(field, f"{{FIELD_NOT_FOUND: {field}}}"))
        else:
            return str(item)
    
    def _execute_auth_function(self, args: List[str]) -> str:
        """Execute authentication function."""
        if not args:
            return "{{NO_AUTH_CREDENTIAL_SPECIFIED}}"
        
        cred_name = args[0]
        cred = self.auth_manager.get_credentials(cred_name)
        if not cred:
            return f"{{CREDENTIAL_NOT_FOUND: {cred_name}}}"
        
        return cred.value
    
    def create_parameterized_tests(self, base_test: Dict, parameters: List[Dict]) -> List[Dict]:
        """Create parameterized tests from base test and parameters."""
        tests = []
        
        for i, params in enumerate(parameters):
            test = self._deep_copy(base_test)
            test = self._apply_parameters(test, params)
            test['name'] = f"{test['name']} - {i+1}"
            tests.append(test)
        
        return tests
    
    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy object."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj
    
    def _apply_parameters(self, test: Dict, params: Dict) -> Dict:
        """Apply parameters to test."""
        # Convert test to string, apply parameters, then parse back
        test_str = json.dumps(test)
        
        for key, value in params.items():
            placeholder = f"${{{key}}}"
            test_str = test_str.replace(placeholder, str(value))
        
        return json.loads(test_str)
    
    def load_test_suite(self, suite_path: str) -> Dict:
        """Load test suite with input configurations."""
        path = Path(suite_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Test suite not found: {suite_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            suite = yaml.safe_load(f)
        
        # Process data sources
        data_sources = suite.get('data_sources', {})
        for name, config in data_sources.items():
            self.add_data_source(name, config['type'], config['path'], config.get('options'))
        
        # Process templates
        templates = suite.get('templates', {})
        for name, template in templates.items():
            self.add_template(name, template)
        
        # Process tests
        tests = suite.get('tests', [])
        processed_tests = []
        
        for test in tests:
            if 'template' in test:
                # Generate test data from template
                template_name = test['template']
                count = test.get('count', 1)
                context = test.get('context', {})
                
                generated_data = self.generate_test_data(template_name, count, context)
                for data in generated_data:
                    test_copy = test.copy()
                    test_copy.update(data)
                    processed_tests.append(test_copy)
            else:
                processed_tests.append(test)
        
        return {
            'name': suite.get('name', 'Test Suite'),
            'description': suite.get('description', ''),
            'tests': processed_tests
        }

def main():
    """Command line interface for test input management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage test inputs for Restaceratops")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add data source
    add_source_parser = subparsers.add_parser('add-source', help='Add data source')
    add_source_parser.add_argument('name', help='Data source name')
    add_source_parser.add_argument('type', choices=['csv', 'json', 'yaml', 'api'], 
                                  help='Data source type')
    add_source_parser.add_argument('path', help='Path to data source')
    
    # Add template
    add_template_parser = subparsers.add_parser('add-template', help='Add test template')
    add_template_parser.add_argument('name', help='Template name')
    add_template_parser.add_argument('file', help='Path to template file')
    
    # Generate test data
    generate_parser = subparsers.add_parser('generate', help='Generate test data')
    generate_parser.add_argument('template', help='Template name')
    generate_parser.add_argument('--count', type=int, default=1, help='Number of records')
    generate_parser.add_argument('--output', help='Output file path')
    
    # Load test suite
    suite_parser = subparsers.add_parser('load-suite', help='Load test suite')
    suite_parser.add_argument('suite', help='Path to test suite file')
    suite_parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    input_manager = TestInputManager()
    
    if args.command == 'add-source':
        success = input_manager.add_data_source(args.name, args.type, args.path)
        if success:
            print(f"✅ Added data source: {args.name}")
        else:
            print(f"❌ Failed to add data source: {args.name}")
    
    elif args.command == 'add-template':
        with open(args.file, 'r') as f:
            template = yaml.safe_load(f)
        success = input_manager.add_template(args.name, template)
        if success:
            print(f"✅ Added template: {args.name}")
        else:
            print(f"❌ Failed to add template: {args.name}")
    
    elif args.command == 'generate':
        try:
            data = input_manager.generate_test_data(args.template, args.count)
            if args.output:
                with open(args.output, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
                print(f"✅ Generated {len(data)} records to {args.output}")
            else:
                print(yaml.dump(data, default_flow_style=False))
        except Exception as e:
            print(f"❌ Error generating data: {e}")
    
    elif args.command == 'load-suite':
        try:
            suite = input_manager.load_test_suite(args.suite)
            if args.output:
                with open(args.output, 'w') as f:
                    yaml.dump(suite, f, default_flow_style=False)
                print(f"✅ Loaded test suite to {args.output}")
            else:
                print(f"✅ Loaded test suite: {suite['name']} with {len(suite['tests'])} tests")
        except Exception as e:
            print(f"❌ Error loading suite: {e}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 