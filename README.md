
# 🦖 Team Agentosaurus – AI-Augmented Testing Suite

## 🎯 **Vision: Complete AI Testing Ecosystem**

Team Agentosaurus is a comprehensive AI-augmented testing framework featuring specialized dinosaur-themed agents:

- 🦖 **Restaceratops** (API Tester) - *Async HTTP testing with YAML DSL*
- 🦕 **Scriptodon** (Automation Generator) - *AI-powered test script generation*
- 🦖 **Bugzilla Rex** (Bug Reporter) - *Intelligent bug detection & reporting*
- 🦕 **Swaggosaur** (OpenAPI Converter) - *Swagger/OpenAPI to test cases*
- 🦖 **Loadosaurus** (Performance Tester) - *Load & stress testing*
- 🦕 **Testaraptor** (Manual Tester) - *AI-assisted manual testing*
- 🦖 **Thinkodactyl** (Test Advisor) - *LLM-based testing strategy*

---

## 🚀 **Restaceratops - API Testing Agent** (Ready for Deployment!)

### ✨ **Features**
* **Async HTTP** testing with `httpx` and `asyncio`
* **YAML DSL** for human‑readable test cases (supports variable capture and reuse)
* **Assertions** for status codes and JSON Schema validation
* **JUnit XML, Console, Prometheus** reporters
* **LLM booster** – optional module to generate new tests from an OpenAPI spec
* **Docker‑ready** – one command to run anywhere
* **CI‑friendly** – exits non‑zero on failures; drop into GitHub Actions, GitLab, Jenkins

### 🏃‍♂️ **Quick Start**

```bash
# Install dependencies
poetry install

# Run tests
poetry run python -m agent.runner --tests tests

# Run with custom concurrency
poetry run python -m agent.runner --tests tests --concurrency 5
```

### 🐳 **Docker Deployment**
```bash
# Build image
docker build -t restaceratops .

# Run with environment variables
docker run --rm -e BASE_URL=https://your-api.com restaceratops

# Run with custom test directory
docker run --rm -v $(pwd)/tests:/app/tests restaceratops
```

### 🤖 **Generate Tests with AI**
```bash
# Generate tests from OpenAPI spec
poetry run python -m agent.generator_llm openapi.json

# Use custom model
poetry run python -m agent.generator_llm openapi.json --model gpt-4
```

### 💬 **Chat with Restaceratops (NEW!)**
Talk to your agent in simple English:

```bash
# Start interactive chat
poetry run python -m agent.chat_interface

# Demo the conversational features
poetry run python demo_chat.py
```

**Example Conversations:**
```
You: "Hello!"
Restaceratops: "🦖 Hello! I'm Restaceratops, your AI-powered API testing agent!"

You: "Test my API at https://my-api.com"
Restaceratops: *runs health checks and basic tests*

You: "Create tests for my authentication endpoint"
Restaceratops: *generates login/logout test cases*

You: "Show me the test results"
Restaceratops: *displays detailed results and metrics*
```

### 📊 **Deploy as Kubernetes CronJob**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: restaceratops-nightly
spec:
  schedule: "0 1 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: runner
            image: ghcr.io/your/restaceratops:0.1.0
            env:
            - name: BASE_URL
              value: "https://your-api.com"
            - name: BEARER_TOKEN
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: bearer-token
          restartPolicy: Never
```

---

## 🧪 **Test Examples**

### Basic API Test
```yaml
- name: "User Authentication"
  request:
    method: POST
    url: https://api.example.com/auth
    json:
      username: "testuser"
      password: "testpass"
  expect:
    status: 200
    save:
      token: $.access_token
```

### Schema Validation
```yaml
- name: "User Profile Validation"
  request:
    method: GET
    url: https://api.example.com/user/profile
  expect:
    status: 200
    schema:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
      required: ["id", "name", "email"]
```

### Variable Reuse
```yaml
- name: "Create User"
  request:
    method: POST
    url: https://api.example.com/users
    json:
      name: "John Doe"
      email: "john@example.com"
  expect:
    status: 201
    save:
      user_id: $.id

- name: "Get Created User"
  request:
    method: GET
    url: https://api.example.com/users/{user_id}
  expect:
    status: 200
```

---

## 🔧 **Configuration**

### Environment Variables
- `BASE_URL`: Base URL for API endpoints
- `BEARER_TOKEN`: Authentication token
- `PUSHGATEWAY_URL`: Prometheus push gateway URL

### Command Line Options
- `--tests`: Directory containing YAML test files
- `--concurrency`: Maximum concurrent requests (default: 5)
- `--help`: Show help message

---

## 📈 **Monitoring & Reporting**

### Console Output
```
=== Restaceratops Report ===
✓ User Authentication (245.2 ms)
✓ Profile Validation (189.7 ms)
✗ Create User (456.1 ms)
    → Status 400 != 201
Total: 3, Failed: 1, Time: 0.9s
```

### JUnit XML
```xml
<?xml version='1.0' encoding='utf-8'?>
<testsuite name="restaceratops">
  <testcase name="User Authentication" time="0.245" />
  <testcase name="Profile Validation" time="0.190" />
  <testcase name="Create User" time="0.456">
    <failure message="Status 400 != 201" />
  </testcase>
</testsuite>
```

### Prometheus Metrics
- `restaceratops_step_latency_seconds`: Request latency
- `restaceratops_step_failures`: Failure count

---

## 🚧 **Roadmap: Complete Team Agentosaurus**

### Phase 1: Core Agents ✅
- [x] **Restaceratops** - API Testing
- [ ] **Swaggosaur** - OpenAPI to Test Cases
- [ ] **Thinkodactyl** - Test Strategy Advisor

### Phase 2: Advanced Testing
- [ ] **Loadosaurus** - Performance Testing
- [ ] **Scriptodon** - Test Automation Generator
- [ ] **Bugzilla Rex** - Intelligent Bug Reporting

### Phase 3: Integration & Orchestration
- [ ] **Testaraptor** - Manual Testing Assistant
- [ ] **Agentosaurus Commander** - Multi-agent orchestration
- [ ] **DinoHub** - Centralized test management

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 **License**

MIT License - see LICENSE file for details.

---

*Built with 🦖 by Team Agentosaurus*
