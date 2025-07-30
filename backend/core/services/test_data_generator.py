#!/usr/bin/env python3
"""
🦖 Smart Test Data Generator for Restaceratops
Intelligent test data generation with context awareness and validation
"""

import asyncio
import logging
import json
import random
import string
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re
from faker import Faker

log = logging.getLogger("restaceratops.test_data_generator")

class DataType(Enum):
    """Data types for test data generation"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    JSON = "json"
    ARRAY = "array"
    OBJECT = "object"

class DataCategory(Enum):
    """Data categories for different test scenarios"""
    VALID = "valid"
    INVALID = "invalid"
    BOUNDARY = "boundary"
    EDGE_CASE = "edge_case"
    PERFORMANCE = "performance"
    SECURITY = "security"

@dataclass
class DataField:
    """Data field configuration"""
    name: str
    data_type: DataType
    category: DataCategory
    constraints: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    required: bool = True
    default_value: Optional[Any] = None
    validation_rules: List[str] = field(default_factory=list)

@dataclass
class TestDataSet:
    """Generated test data set"""
    id: str
    name: str
    description: str
    test_case_id: str
    data_category: DataCategory
    fields: List[DataField]
    generated_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    validation_results: Dict[str, bool] = field(default_factory=dict)

class SmartTestDataGenerator:
    """Intelligent test data generator with context awareness"""
    
    def __init__(self):
        self.faker = Faker()
        self.data_templates = self._load_data_templates()
        self.generation_history: List[Dict[str, Any]] = []
        self.validation_rules = self._load_validation_rules()
        
    def _load_data_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined data templates for common scenarios"""
        return {
            "user_registration": {
                "fields": [
                    {"name": "username", "type": "string", "constraints": {"min_length": 3, "max_length": 20}},
                    {"name": "email", "type": "email", "constraints": {"format": "email"}},
                    {"name": "password", "type": "string", "constraints": {"min_length": 8}},
                    {"name": "first_name", "type": "string", "constraints": {"max_length": 50}},
                    {"name": "last_name", "type": "string", "constraints": {"max_length": 50}},
                    {"name": "age", "type": "integer", "constraints": {"min": 13, "max": 120}},
                    {"name": "is_active", "type": "boolean", "default": True}
                ]
            },
            "product_creation": {
                "fields": [
                    {"name": "name", "type": "string", "constraints": {"min_length": 1, "max_length": 100}},
                    {"name": "description", "type": "string", "constraints": {"max_length": 500}},
                    {"name": "price", "type": "float", "constraints": {"min": 0.01}},
                    {"name": "category", "type": "string", "constraints": {"enum": ["electronics", "clothing", "books"]}},
                    {"name": "stock_quantity", "type": "integer", "constraints": {"min": 0}},
                    {"name": "is_available", "type": "boolean", "default": True}
                ]
            },
            "order_processing": {
                "fields": [
                    {"name": "order_id", "type": "string", "constraints": {"pattern": r"ORD-\d{6}"}},
                    {"name": "customer_id", "type": "string", "constraints": {"pattern": r"CUST-\d{4}"}},
                    {"name": "total_amount", "type": "float", "constraints": {"min": 0.01}},
                    {"name": "order_date", "type": "datetime", "constraints": {"min_date": "2020-01-01"}},
                    {"name": "status", "type": "string", "constraints": {"enum": ["pending", "confirmed", "shipped", "delivered"]}},
                    {"name": "items", "type": "array", "constraints": {"min_items": 1, "max_items": 10}}
                ]
            }
        }
    
    def _load_validation_rules(self) -> Dict[str, callable]:
        """Load validation rules for different data types"""
        return {
            "email": lambda x: re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", x),
            "phone": lambda x: re.match(r"^\+?[\d\s\-\(\)]{10,}$", x),
            "url": lambda x: re.match(r"^https?://[^\s/$.?#].[^\s]*$", x),
            "positive_integer": lambda x: isinstance(x, int) and x > 0,
            "positive_float": lambda x: isinstance(x, (int, float)) and x > 0,
            "non_empty_string": lambda x: isinstance(x, str) and len(x.strip()) > 0,
            "valid_date": lambda x: isinstance(x, (str, datetime)) and self._is_valid_date(x),
            "valid_json": lambda x: self._is_valid_json(x)
        }
    
    async def generate_test_data_for_case(
        self, 
        test_case: Dict[str, Any], 
        data_category: DataCategory = DataCategory.VALID
    ) -> TestDataSet:
        """Generate test data for a specific test case"""
        
        log.info(f"Generating test data for test case: {test_case.get('id', 'Unknown')}")
        
        # Analyze test case to determine data requirements
        data_requirements = await self._analyze_test_case_requirements(test_case)
        
        # Generate data based on category
        if data_category == DataCategory.VALID:
            generated_data = await self._generate_valid_data(data_requirements)
        elif data_category == DataCategory.INVALID:
            generated_data = await self._generate_invalid_data(data_requirements)
        elif data_category == DataCategory.BOUNDARY:
            generated_data = await self._generate_boundary_data(data_requirements)
        elif data_category == DataCategory.EDGE_CASE:
            generated_data = await self._generate_edge_case_data(data_requirements)
        else:
            generated_data = await self._generate_valid_data(data_requirements)
        
        # Create test data set
        test_data_set = TestDataSet(
            id=f"TD-{test_case.get('id', 'UNKNOWN')}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=f"Test Data for {test_case.get('name', 'Test Case')}",
            description=f"Generated test data for {data_category.value} scenario",
            test_case_id=test_case.get('id', 'UNKNOWN'),
            data_category=data_category,
            fields=data_requirements,
            generated_data=generated_data,
            metadata={
                "test_type": test_case.get('test_type', 'unknown'),
                "complexity": test_case.get('complexity', 'medium'),
                "generation_method": "ai_enhanced"
            }
        )
        
        # Validate generated data
        test_data_set.validation_results = await self._validate_generated_data(
            generated_data, data_requirements
        )
        
        # Log generation
        self.generation_history.append({
            "test_case_id": test_case.get('id', 'UNKNOWN'),
            "data_category": data_category.value,
            "fields_count": len(data_requirements),
            "validation_passed": all(test_data_set.validation_results.values()),
            "timestamp": datetime.now().isoformat()
        })
        
        log.info(f"Generated test data with {len(generated_data)} fields for {data_category.value} scenario")
        return test_data_set
    
    async def _analyze_test_case_requirements(self, test_case: Dict[str, Any]) -> List[DataField]:
        """Analyze test case to determine data requirements"""
        
        # Extract data requirements from test case
        test_data = test_case.get('test_data', {})
        steps = test_case.get('steps', [])
        assertions = test_case.get('assertions', [])
        
        data_fields = []
        
        # Analyze existing test data
        for field_name, field_value in test_data.items():
            data_type = self._infer_data_type(field_value)
            data_fields.append(DataField(
                name=field_name,
                data_type=data_type,
                category=DataCategory.VALID,
                description=f"Field extracted from test case data"
            ))
        
        # Analyze steps for additional data requirements
        step_data_requirements = self._extract_data_from_steps(steps)
        for field_name, field_info in step_data_requirements.items():
            if not any(f.name == field_name for f in data_fields):
                data_fields.append(DataField(
                    name=field_name,
                    data_type=field_info.get('type', DataType.STRING),
                    category=DataCategory.VALID,
                    description=f"Field required by test steps"
                ))
        
        # Analyze assertions for validation requirements
        assertion_requirements = self._extract_data_from_assertions(assertions)
        for field_name, field_info in assertion_requirements.items():
            existing_field = next((f for f in data_fields if f.name == field_name), None)
            if existing_field:
                existing_field.validation_rules.extend(field_info.get('validation_rules', []))
            else:
                data_fields.append(DataField(
                    name=field_name,
                    data_type=field_info.get('type', DataType.STRING),
                    category=DataCategory.VALID,
                    description=f"Field required by assertions",
                    validation_rules=field_info.get('validation_rules', [])
                ))
        
        return data_fields
    
    def _infer_data_type(self, value: Any) -> DataType:
        """Infer data type from value"""
        if isinstance(value, str):
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
                return DataType.EMAIL
            elif re.match(r"^https?://", value):
                return DataType.URL
            elif re.match(r"^\d{4}-\d{2}-\d{2}", value):
                return DataType.DATE
            else:
                return DataType.STRING
        elif isinstance(value, int):
            return DataType.INTEGER
        elif isinstance(value, float):
            return DataType.FLOAT
        elif isinstance(value, bool):
            return DataType.BOOLEAN
        elif isinstance(value, list):
            return DataType.ARRAY
        elif isinstance(value, dict):
            return DataType.OBJECT
        else:
            return DataType.STRING
    
    def _extract_data_from_steps(self, steps: List[str]) -> Dict[str, Dict[str, Any]]:
        """Extract data requirements from test steps"""
        data_requirements = {}
        
        for step in steps:
            # Look for data patterns in steps
            if "enter" in step.lower() or "input" in step.lower():
                # Extract field names from input steps
                field_matches = re.findall(r'enter\s+(\w+)', step.lower())
                for field in field_matches:
                    data_requirements[field] = {
                        "type": DataType.STRING,
                        "required": True
                    }
            
            elif "select" in step.lower() or "choose" in step.lower():
                # Extract selection data
                field_matches = re.findall(r'select\s+(\w+)', step.lower())
                for field in field_matches:
                    data_requirements[field] = {
                        "type": DataType.STRING,
                        "required": True
                    }
        
        return data_requirements
    
    def _extract_data_from_assertions(self, assertions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Extract data requirements from assertions"""
        data_requirements = {}
        
        for assertion in assertions:
            assertion_type = assertion.get('type', '')
            
            if assertion_type == 'status_code':
                data_requirements['expected_status'] = {
                    "type": DataType.INTEGER,
                    "validation_rules": ["positive_integer"]
                }
            elif assertion_type == 'response_contains':
                data_requirements['expected_content'] = {
                    "type": DataType.STRING,
                    "validation_rules": ["non_empty_string"]
                }
            elif assertion_type == 'field_equals':
                field_name = assertion.get('field', 'unknown_field')
                data_requirements[field_name] = {
                    "type": DataType.STRING,
                    "validation_rules": ["non_empty_string"]
                }
        
        return data_requirements
    
    async def _generate_valid_data(self, fields: List[DataField]) -> Dict[str, Any]:
        """Generate valid test data"""
        generated_data = {}
        
        for field in fields:
            try:
                generated_data[field.name] = self._generate_field_value(field, DataCategory.VALID)
            except Exception as e:
                log.error(f"Failed to generate valid data for field {field.name}: {e}")
                generated_data[field.name] = self._generate_fallback_value(field)
        
        return generated_data
    
    async def _generate_invalid_data(self, fields: List[DataField]) -> Dict[str, Any]:
        """Generate invalid test data"""
        generated_data = {}
        
        for field in fields:
            try:
                generated_data[field.name] = self._generate_invalid_field_value(field)
            except Exception as e:
                log.error(f"Failed to generate invalid data for field {field.name}: {e}")
                generated_data[field.name] = self._generate_fallback_invalid_value(field)
        
        return generated_data
    
    async def _generate_boundary_data(self, fields: List[DataField]) -> Dict[str, Any]:
        """Generate boundary test data"""
        generated_data = {}
        
        for field in fields:
            try:
                generated_data[field.name] = self._generate_boundary_field_value(field)
            except Exception as e:
                log.error(f"Failed to generate boundary data for field {field.name}: {e}")
                generated_data[field.name] = self._generate_fallback_value(field)
        
        return generated_data
    
    async def _generate_edge_case_data(self, fields: List[DataField]) -> Dict[str, Any]:
        """Generate edge case test data"""
        generated_data = {}
        
        for field in fields:
            try:
                generated_data[field.name] = self._generate_edge_case_field_value(field)
            except Exception as e:
                log.error(f"Failed to generate edge case data for field {field.name}: {e}")
                generated_data[field.name] = self._generate_fallback_value(field)
        
        return generated_data
    
    def _generate_field_value(self, field: DataField, category: DataCategory) -> Any:
        """Generate a value for a specific field"""
        
        if field.data_type == DataType.STRING:
            return self._generate_string_value(field, category)
        elif field.data_type == DataType.INTEGER:
            return self._generate_integer_value(field, category)
        elif field.data_type == DataType.FLOAT:
            return self._generate_float_value(field, category)
        elif field.data_type == DataType.BOOLEAN:
            return self._generate_boolean_value(field, category)
        elif field.data_type == DataType.EMAIL:
            return self._generate_email_value(field, category)
        elif field.data_type == DataType.PHONE:
            return self._generate_phone_value(field, category)
        elif field.data_type == DataType.URL:
            return self._generate_url_value(field, category)
        elif field.data_type == DataType.DATE:
            return self._generate_date_value(field, category)
        elif field.data_type == DataType.DATETIME:
            return self._generate_datetime_value(field, category)
        elif field.data_type == DataType.ARRAY:
            return self._generate_array_value(field, category)
        elif field.data_type == DataType.OBJECT:
            return self._generate_object_value(field, category)
        else:
            return self._generate_fallback_value(field)
    
    def _generate_string_value(self, field: DataField, category: DataCategory) -> str:
        """Generate string value based on field constraints"""
        min_length = field.constraints.get('min_length', 1)
        max_length = field.constraints.get('max_length', 50)
        
        if category == DataCategory.VALID:
            length = random.randint(min_length, max_length)
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        elif category == DataCategory.INVALID:
            return ""  # Empty string for invalid
        elif category == DataCategory.BOUNDARY:
            return 'a' * max_length  # Maximum length
        else:
            return self.faker.word()
    
    def _generate_integer_value(self, field: DataField, category: DataCategory) -> int:
        """Generate integer value based on field constraints"""
        min_val = field.constraints.get('min', 0)
        max_val = field.constraints.get('max', 100)
        
        if category == DataCategory.VALID:
            return random.randint(min_val, max_val)
        elif category == DataCategory.INVALID:
            return -1  # Negative value for invalid
        elif category == DataCategory.BOUNDARY:
            return max_val  # Maximum value
        else:
            return random.randint(1, 1000)
    
    def _generate_float_value(self, field: DataField, category: DataCategory) -> float:
        """Generate float value based on field constraints"""
        min_val = field.constraints.get('min', 0.0)
        max_val = field.constraints.get('max', 1000.0)
        
        if category == DataCategory.VALID:
            return round(random.uniform(min_val, max_val), 2)
        elif category == DataCategory.INVALID:
            return -1.0  # Negative value for invalid
        elif category == DataCategory.BOUNDARY:
            return max_val  # Maximum value
        else:
            return round(random.uniform(0.01, 1000.0), 2)
    
    def _generate_boolean_value(self, field: DataField, category: DataCategory) -> bool:
        """Generate boolean value"""
        if category == DataCategory.VALID:
            return field.constraints.get('default', True)
        elif category == DataCategory.INVALID:
            return "invalid"  # Invalid boolean
        else:
            return random.choice([True, False])
    
    def _generate_email_value(self, field: DataField, category: DataCategory) -> str:
        """Generate email value"""
        if category == DataCategory.VALID:
            return self.faker.email()
        elif category == DataCategory.INVALID:
            return "invalid-email"  # Invalid email format
        else:
            return self.faker.email()
    
    def _generate_phone_value(self, field: DataField, category: DataCategory) -> str:
        """Generate phone value"""
        if category == DataCategory.VALID:
            return self.faker.phone_number()
        elif category == DataCategory.INVALID:
            return "invalid-phone"  # Invalid phone format
        else:
            return self.faker.phone_number()
    
    def _generate_url_value(self, field: DataField, category: DataCategory) -> str:
        """Generate URL value"""
        if category == DataCategory.VALID:
            return self.faker.url()
        elif category == DataCategory.INVALID:
            return "invalid-url"  # Invalid URL format
        else:
            return self.faker.url()
    
    def _generate_date_value(self, field: DataField, category: DataCategory) -> str:
        """Generate date value"""
        if category == DataCategory.VALID:
            return self.faker.date()
        elif category == DataCategory.INVALID:
            return "invalid-date"  # Invalid date format
        else:
            return self.faker.date()
    
    def _generate_datetime_value(self, field: DataField, category: DataCategory) -> str:
        """Generate datetime value"""
        if category == DataCategory.VALID:
            return self.faker.iso8601()
        elif category == DataCategory.INVALID:
            return "invalid-datetime"  # Invalid datetime format
        else:
            return self.faker.iso8601()
    
    def _generate_array_value(self, field: DataField, category: DataCategory) -> List[Any]:
        """Generate array value"""
        min_items = field.constraints.get('min_items', 1)
        max_items = field.constraints.get('max_items', 5)
        
        if category == DataCategory.VALID:
            count = random.randint(min_items, max_items)
            return [self.faker.word() for _ in range(count)]
        elif category == DataCategory.INVALID:
            return "not-an-array"  # Invalid array
        else:
            return [self.faker.word() for _ in range(random.randint(1, 3))]
    
    def _generate_object_value(self, field: DataField, category: DataCategory) -> Dict[str, Any]:
        """Generate object value"""
        if category == DataCategory.VALID:
            return {
                "id": self.faker.uuid4(),
                "name": self.faker.name(),
                "created_at": self.faker.iso8601()
            }
        elif category == DataCategory.INVALID:
            return "not-an-object"  # Invalid object
        else:
            return {"key": "value"}
    
    def _generate_invalid_field_value(self, field: DataField) -> Any:
        """Generate invalid value for a field"""
        if field.data_type == DataType.STRING:
            return ""  # Empty string
        elif field.data_type == DataType.INTEGER:
            return "not-a-number"  # String instead of number
        elif field.data_type == DataType.FLOAT:
            return "not-a-float"  # String instead of float
        elif field.data_type == DataType.BOOLEAN:
            return "not-a-boolean"  # String instead of boolean
        elif field.data_type == DataType.EMAIL:
            return "invalid-email-format"  # Invalid email
        elif field.data_type == DataType.PHONE:
            return "invalid-phone-format"  # Invalid phone
        elif field.data_type == DataType.URL:
            return "invalid-url-format"  # Invalid URL
        elif field.data_type == DataType.DATE:
            return "invalid-date-format"  # Invalid date
        elif field.data_type == DataType.DATETIME:
            return "invalid-datetime-format"  # Invalid datetime
        elif field.data_type == DataType.ARRAY:
            return "not-an-array"  # String instead of array
        elif field.data_type == DataType.OBJECT:
            return "not-an-object"  # String instead of object
        else:
            return None
    
    def _generate_boundary_field_value(self, field: DataField) -> Any:
        """Generate boundary value for a field"""
        if field.data_type == DataType.STRING:
            max_length = field.constraints.get('max_length', 100)
            return 'a' * max_length  # Maximum length
        elif field.data_type == DataType.INTEGER:
            max_val = field.constraints.get('max', 100)
            return max_val  # Maximum value
        elif field.data_type == DataType.FLOAT:
            max_val = field.constraints.get('max', 1000.0)
            return max_val  # Maximum value
        else:
            return self._generate_field_value(field, DataCategory.VALID)
    
    def _generate_edge_case_field_value(self, field: DataField) -> Any:
        """Generate edge case value for a field"""
        if field.data_type == DataType.STRING:
            return 'a' * 10000  # Very long string
        elif field.data_type == DataType.INTEGER:
            return 999999999  # Very large number
        elif field.data_type == DataType.FLOAT:
            return 999999.999  # Very large float
        else:
            return self._generate_field_value(field, DataCategory.VALID)
    
    def _generate_fallback_value(self, field: DataField) -> Any:
        """Generate fallback value when generation fails"""
        if field.default_value is not None:
            return field.default_value
        
        if field.data_type == DataType.STRING:
            return "fallback_value"
        elif field.data_type == DataType.INTEGER:
            return 0
        elif field.data_type == DataType.FLOAT:
            return 0.0
        elif field.data_type == DataType.BOOLEAN:
            return False
        else:
            return None
    
    def _generate_fallback_invalid_value(self, field: DataField) -> Any:
        """Generate fallback invalid value"""
        return self._generate_invalid_field_value(field)
    
    async def _validate_generated_data(self, data: Dict[str, Any], fields: List[DataField]) -> Dict[str, bool]:
        """Validate generated data against field requirements"""
        validation_results = {}
        
        for field in fields:
            field_value = data.get(field.name)
            is_valid = True
            
            # Check validation rules
            for rule_name in field.validation_rules:
                if rule_name in self.validation_rules:
                    validator = self.validation_rules[rule_name]
                    if not validator(field_value):
                        is_valid = False
                        break
            
            # Check constraints
            if is_valid and field.constraints:
                is_valid = self._check_constraints(field_value, field.constraints)
            
            validation_results[field.name] = is_valid
        
        return validation_results
    
    def _check_constraints(self, value: Any, constraints: Dict[str, Any]) -> bool:
        """Check if value meets constraints"""
        try:
            if 'min_length' in constraints and isinstance(value, str):
                if len(value) < constraints['min_length']:
                    return False
            
            if 'max_length' in constraints and isinstance(value, str):
                if len(value) > constraints['max_length']:
                    return False
            
            if 'min' in constraints and isinstance(value, (int, float)):
                if value < constraints['min']:
                    return False
            
            if 'max' in constraints and isinstance(value, (int, float)):
                if value > constraints['max']:
                    return False
            
            if 'enum' in constraints:
                if value not in constraints['enum']:
                    return False
            
            if 'pattern' in constraints and isinstance(value, str):
                if not re.match(constraints['pattern'], value):
                    return False
            
            return True
            
        except Exception as e:
            log.error(f"Error checking constraints: {e}")
            return False
    
    def _is_valid_date(self, value: Union[str, datetime]) -> bool:
        """Check if value is a valid date"""
        try:
            if isinstance(value, str):
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            elif isinstance(value, datetime):
                return True
            return True
        except:
            return False
    
    def _is_valid_json(self, value: Any) -> bool:
        """Check if value is valid JSON"""
        try:
            if isinstance(value, str):
                json.loads(value)
            elif isinstance(value, (dict, list)):
                return True
            return True
        except:
            return False
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get test data generation statistics"""
        total_generations = len(self.generation_history)
        successful_validations = sum(
            1 for entry in self.generation_history 
            if entry.get('validation_passed', False)
        )
        
        category_counts = {}
        for entry in self.generation_history:
            category = entry.get('data_category', 'unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_generations": total_generations,
            "successful_validations": successful_validations,
            "validation_success_rate": successful_validations / total_generations if total_generations > 0 else 0,
            "category_distribution": category_counts,
            "average_fields_per_generation": sum(
                entry.get('fields_count', 0) for entry in self.generation_history
            ) / total_generations if total_generations > 0 else 0,
            "generation_history": self.generation_history
        } 