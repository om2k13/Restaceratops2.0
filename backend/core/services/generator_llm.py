
"""Optional module to generate YAML tests from an OpenAPI spec using an LLM."""
import openai, yaml, json, pathlib, os

TEMPLATE = """
You are an assistant that writes API test cases in a YAML array format. Each element should have:
- name
- request: method, url, optional json
- expect: status, optional json or schema
Use concise names. Only output YAML array.
API specification JSON:
{spec}
"""

def generate_tests(openapi_json_path: str, output_path: str = "tests/generated.yml", model="gpt-4o-mini"):
    with open(openapi_json_path) as f:
        spec = json.load(f)
    prompt = TEMPLATE.format(spec=json.dumps(spec)[:6000])  # truncate for token safety
    resp = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.2,
    )
    yaml_text = resp.choices[0].message.content.strip()
    pathlib.Path(output_path).write_text(yaml_text)
    print(f"Wrote generated tests to {output_path}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate API tests from OpenAPI spec using LLM")
    parser.add_argument("openapi_json", help="Path to OpenAPI JSON specification file")
    parser.add_argument("--output", "-o", default="tests/generated.yml", help="Output YAML file path")
    parser.add_argument("--model", "-m", default="gpt-4o-mini", help="OpenAI model to use")
    args = parser.parse_args()
    
    generate_tests(args.openapi_json, args.output, args.model)

if __name__ == "__main__":
    main()
