#!/usr/bin/env python3
"""
🦖 Unified Restaceratops Agent
All-in-one AI-powered API testing agent for both web and terminal interfaces
"""

import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from backend.core.models.auth_manager import AuthManager
from backend.core.services.enhanced_openapi_generator import EnhancedOpenAPIGenerator
from backend.core.models.test_input_manager import TestInputManager

class UnifiedRestaceratopsAgent:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.input_manager = TestInputManager(self.auth_manager)
        # Optionally, add more state here

    # --- Credential Management ---
    def add_credential(self, name: str, cred_type: str, value: str, header_name: Optional[str] = None, description: Optional[str] = None) -> bool:
        return self.auth_manager.add_credentials(name, cred_type, value, header_name=header_name, description=description)

    def list_credentials(self) -> List[Dict[str, Any]]:
        return self.auth_manager.list_credentials()

    def remove_credential(self, name: str) -> bool:
        return self.auth_manager.remove_credentials(name)

    def validate_credential(self, name: str) -> bool:
        return self.auth_manager.validate_credentials(name)

    # --- OpenAPI Test Generation ---
    def generate_tests_from_openapi(self, spec_path: str, output_path: str = "tests/generated_from_openapi.yml", include_security: bool = True) -> Path:
        generator = EnhancedOpenAPIGenerator(spec_path, self.auth_manager)
        return generator.save_tests(output_path, include_security=include_security)

    # --- Dynamic Test Input Management ---
    def add_data_source(self, name: str, source_type: str, source_path: str, options: Optional[Dict] = None) -> bool:
        return self.input_manager.add_data_source(name, source_type, source_path, options)

    def add_template(self, name: str, template: Dict) -> bool:
        return self.input_manager.add_template(name, template)

    def generate_test_data(self, template_name: str, count: int = 1, context: Optional[Dict] = None) -> List[Dict]:
        return self.input_manager.generate_test_data(template_name, count, context)

    def load_test_suite(self, suite_path: str) -> Dict:
        return self.input_manager.load_test_suite(suite_path)

    # --- Test Execution (Stub) ---
    def run_tests(self, test_file: str = "tests/generated_from_openapi.yml") -> str:
        # This is a stub; integrate with your runner as needed
        # Example: poetry run python -m agent.runner --tests <test_file>
        return f"[Stub] Would run tests from {test_file}"

    # --- CLI Interface ---
    async def cli(self):
        print("🦖 Welcome to the Unified Restaceratops Agent!")
        print("Type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                cmd = input("restaceratops> ").strip()
                if cmd in ("exit", "quit"): break
                elif cmd == "help":
                    print("""
Available commands:
  add-cred <name> <type> <value> [--header <header>] [--desc <desc>]
  list-creds
  remove-cred <name>
  validate-cred <name>
  openapi <spec_path> [--output <file>] [--no-security]
  add-source <name> <type> <path>
  add-template <name> <file>
  gen-data <template> [--count N]
  run-tests [<test_file>]
  help
  exit
""")
                elif cmd.startswith("add-cred"):
                    parts = cmd.split()
                    name, typ, value = parts[1:4]
                    header = None
                    desc = None
                    for i, p in enumerate(parts):
                        if p == "--header" and i+1 < len(parts): header = parts[i+1]
                        if p == "--desc" and i+1 < len(parts): desc = parts[i+1]
                    ok = self.add_credential(name, typ, value, header, desc)
                    print("✅ Added" if ok else "❌ Failed")
                elif cmd == "list-creds":
                    for cred in self.list_credentials():
                        print(f"  • {cred['name']} ({cred['type']})")
                elif cmd.startswith("remove-cred"):
                    name = cmd.split()[1]
                    ok = self.remove_credential(name)
                    print("✅ Removed" if ok else "❌ Not found")
                elif cmd.startswith("validate-cred"):
                    name = cmd.split()[1]
                    ok = self.validate_credential(name)
                    print("✅ Valid" if ok else "❌ Invalid or expired")
                elif cmd.startswith("openapi"):
                    parts = cmd.split()
                    spec = parts[1]
                    output = "tests/generated_from_openapi.yml"
                    include_security = True
                    if "--output" in parts:
                        output = parts[parts.index("--output") + 1]
                    if "--no-security" in parts:
                        include_security = False
                    out = self.generate_tests_from_openapi(spec, output, include_security)
                    print(f"✅ Generated tests: {out}")
                elif cmd.startswith("add-source"):
                    _, name, typ, path = cmd.split()[:4]
                    ok = self.add_data_source(name, typ, path)
                    print("✅ Added" if ok else "❌ Failed")
                elif cmd.startswith("add-template"):
                    _, name, file = cmd.split()[:3]
                    import yaml
                    with open(file) as f:
                        template = yaml.safe_load(f)
                    ok = self.add_template(name, template)
                    print("✅ Added" if ok else "❌ Failed")
                elif cmd.startswith("gen-data"):
                    parts = cmd.split()
                    template = parts[1]
                    count = 1
                    if "--count" in parts:
                        count = int(parts[parts.index("--count") + 1])
                    data = self.generate_test_data(template, count)
                    import yaml
                    print(yaml.dump(data, default_flow_style=False))
                elif cmd.startswith("run-tests"):
                    parts = cmd.split()
                    test_file = parts[1] if len(parts) > 1 else "tests/generated_from_openapi.yml"
                    print(self.run_tests(test_file))
                else:
                    print("❓ Unknown command. Type 'help' for options.")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    agent = UnifiedRestaceratopsAgent()
    asyncio.run(agent.cli()) 