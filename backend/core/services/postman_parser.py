#!/usr/bin/env python3
"""
🦖 Postman Collection Parser for Restaceratops
Converts Postman collection JSON to test cases
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

log = logging.getLogger("restaceratops.postman_parser")

class PostmanParser:
    """Parse Postman collection JSON and convert to test cases"""
    
    def __init__(self):
        self.variables = {}
        self.environments = {}
    
    def parse_collection(self, json_content: str) -> Dict[str, Any]:
        """Parse Postman collection JSON and return test cases"""
        try:
            collection = json.loads(json_content)
            
            # Extract collection info
            collection_info = {
                "name": collection.get("info", {}).get("name", "Imported Collection"),
                "description": collection.get("info", {}).get("description", ""),
                "variables": collection.get("variable", []),
                "auth": collection.get("auth", {}),
                "test_cases": []
            }
            
            # Parse variables
            self.variables = self._extract_variables(collection.get("variable", []))
            
            # Parse all requests recursively
            test_cases = self._parse_items(collection.get("item", []))
            collection_info["test_cases"] = test_cases
            
            log.info(f"Successfully parsed Postman collection: {collection_info['name']}")
            log.info(f"Found {len(test_cases)} test cases")
            
            return collection_info
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse Postman collection: {e}")
    
    def _extract_variables(self, variables: List[Dict]) -> Dict[str, str]:
        """Extract variables from Postman collection"""
        var_dict = {}
        for var in variables:
            if isinstance(var, dict) and "key" in var and "value" in var:
                var_dict[var["key"]] = var["value"]
        return var_dict
    
    def _parse_items(self, items: List[Dict], parent_name: str = "") -> List[Dict]:
        """Recursively parse items (folders and requests)"""
        test_cases = []
        
        for item in items:
            if item.get("request"):
                # This is a request
                test_case = self._parse_request(item, parent_name)
                if test_case:
                    test_cases.append(test_case)
            elif item.get("item"):
                # This is a folder
                folder_name = item.get("name", "Unknown Folder")
                folder_test_cases = self._parse_items(item["item"], folder_name)
                test_cases.extend(folder_test_cases)
        
        return test_cases
    
    def _parse_request(self, item: Dict, parent_name: str = "") -> Optional[Dict]:
        """Parse a single request into a test case"""
        request = item.get("request", {})
        if not request:
            return None
        
        # Extract request details
        method = request.get("method", "GET")
        url_info = request.get("url", {})
        
        # Handle different URL formats
        if isinstance(url_info, str):
            url = url_info
        elif isinstance(url_info, dict):
            url = url_info.get("raw", "")
            if not url:
                # Build URL from components
                protocol = url_info.get("protocol", "https")
                host = url_info.get("host", [])
                path = url_info.get("path", [])
                
                if isinstance(host, list):
                    host = ".".join(host)
                if isinstance(path, list):
                    path = "/".join(path)
                
                url = f"{protocol}://{host}/{path}".replace("//", "/")
        else:
            url = str(url_info)
        
        # Extract headers
        headers = {}
        for header in request.get("header", []):
            if isinstance(header, dict) and "key" in header and "value" in header:
                headers[header["key"]] = header["value"]
        
        # Extract body
        body = request.get("body", {})
        json_data = None
        if body and body.get("mode") == "raw":
            try:
                json_data = json.loads(body.get("raw", "{}"))
            except:
                json_data = None
        
        # Extract tests/expectations
        test_script = item.get("event", [])
        expected_status = 200  # Default expectation
        
        # Look for test scripts that set expected status
        for event in test_script:
            if event.get("listen") == "test":
                script = event.get("script", {}).get("exec", [])
                for line in script:
                    if "pm.test" in str(line) and "status" in str(line):
                        # Try to extract status code from test
                        if "200" in str(line):
                            expected_status = 200
                        elif "201" in str(line):
                            expected_status = 201
                        elif "400" in str(line):
                            expected_status = 400
                        elif "401" in str(line):
                            expected_status = 401
                        elif "404" in str(line):
                            expected_status = 404
                        elif "500" in str(line):
                            expected_status = 500
        
        # Create test case
        test_name = item.get("name", f"{method} {url}")
        if parent_name:
            test_name = f"{parent_name} - {test_name}"
        
        test_case = {
            "name": test_name,
            "request": {
                "method": method,
                "url": url,
                "headers": headers
            },
            "expected_response": {
                "status_code": expected_status
            }
        }
        
        # Add JSON body if present
        if json_data:
            test_case["request"]["json"] = json_data
        
        return test_case
    
    def generate_yaml(self, collection_data: Dict[str, Any]) -> str:
        """Generate YAML test file from parsed collection"""
        yaml_content = f"""# 🦖 Restaceratops Test Cases
# Generated from Postman Collection: {collection_data['name']}
# Description: {collection_data['description']}

"""
        
        for test_case in collection_data["test_cases"]:
            yaml_content += f"""- name: "{test_case['name']}"
  request:
    method: {test_case['request']['method']}
    url: "{test_case['request']['url']}"
"""
            
            # Add headers if present
            if test_case['request'].get('headers'):
                yaml_content += "    headers:\n"
                for key, value in test_case['request']['headers'].items():
                    yaml_content += f'      {key}: "{value}"\n'
            
            # Add JSON body if present
            if test_case['request'].get('json'):
                yaml_content += "    json:\n"
                for key, value in test_case['request']['json'].items():
                    yaml_content += f'      {key}: "{value}"\n'
            
            # Add expected response
            yaml_content += f"""  expected_response:
    status_code: {test_case['expected_response']['status_code']}

"""
        
        return yaml_content

# Global parser instance
postman_parser = PostmanParser() 