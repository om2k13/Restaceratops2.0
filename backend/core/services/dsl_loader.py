
import yaml, jmespath, re, logging
from pathlib import Path
from typing import Union

log = logging.getLogger("agent.dsl")

class Step:
    def __init__(self, raw, context):
        self.name = raw.get("name", "unnamed")
        self.request = raw["request"]
        self.expect = raw["expect"]
        self.raw = raw
        self.context = context

    def render(self, s: str):
        return s.format(**self.context)

    def rendered_request(self):
        req = {}
        for k, v in self.request.items():
            if isinstance(v, str):
                req[k] = self.render(v)
            else:
                req[k] = v
        return req

    def save_from_response(self, response):
        save_map = self.expect.get("save", {})
        for var, expr in save_map.items():
            if expr.startswith("$."):
                value = jmespath.search(expr[2:], response.json())
            else:
                # Handle headers with hyphens by using get() method
                value = response.headers.get(expr)
            self.context[var] = value
            log.debug("Saved %s = %s", var, value)

def load_tests(directory: Union[str, Path]):
    tests = []
    for file in Path(directory).glob("**/*.yml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, list):
                raise ValueError(f"{file} must contain a list of steps")
            tests.append((file.name, data))
    return tests
