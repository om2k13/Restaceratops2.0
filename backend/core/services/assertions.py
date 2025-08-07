
import jsonschema, logging

log = logging.getLogger("agent.assertions")

class AssertionErrorDetails(AssertionError):
    pass

def assert_status(resp, expected):
    if resp.status_code != expected:
        raise AssertionErrorDetails(f"Status {resp.status_code} != {expected}")

def assert_json_schema(resp, schema):
    try:
        jsonschema.validate(resp.json(), schema)
    except jsonschema.ValidationError as e:
        raise AssertionErrorDetails(f"Schema validation failed: {e}") from e

def run_assertions(resp, expect_block):
    assert_status(resp, expect_block["status"])
    if "schema" in expect_block:
        assert_json_schema(resp, expect_block["schema"])
