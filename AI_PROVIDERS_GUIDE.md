# 🤖 **AI Providers & API Keys Guide - RESTACERATOPS**

## 🎯 **Current System Status**

Based on the running system, here's how AI providers and API keys are configured:

### **🔄 Multi-Provider AI System**
The system uses a **smart fallback mechanism** with multiple AI providers:

1. **Primary**: Gemini AI (Free, High Quality)
2. **Secondary**: OpenRouter (10 free models available)
3. **Tertiary**: Enhanced AI System (Ollama local model)
4. **Automatic Failover**: If one provider fails, it switches to the next

---

## 🔑 **API Key Configuration**

### **Current Status**
```
✅ Gemini AI: Integrated and ready, but NO API KEY configured
✅ OpenRouter: 10 models available, but NO API KEY configured
✅ Ollama: Local model working (no API key needed)
❌ DeepSeek: Not configured
❌ Hugging Face: Not configured
❌ OpenAI: Not configured
```

### **How to Add API Keys**

#### **1. Gemini AI (Recommended - Free, High Quality)**
```bash
# Get free API key from https://makersuite.google.com/app/apikey
# Add to .env file:
GOOGLE_API_KEY=your-google-api-key-here
```

**Available Models:**
- `gemini-1.5-flash` (Fast, capable, free)
- `gemini-1.5-pro` (High quality, free tier)
- `gemini-2.0-flash-exp` (Experimental, free)

#### **2. OpenRouter (Secondary - Free Models)**
```bash
# Get free API key from https://openrouter.ai/
# Add to .env file:
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

**Available Free Models:**
- `openai/gpt-3.5-turbo` (Reliable, fast)
- `anthropic/claude-3-haiku` (Good reasoning)
- `google/gemini-2.5-flash-lite` (Fast responses)
- `qwen/qwen3-235b-a22b-2507:free` (High quality)
- `z-ai/glm-4.5-air` (Good for tasks)
- `meta-llama/llama-3.1-8b-instruct` (Reliable)
- `microsoft/phi-3.5-mini-128k` (Fast)
- `deepseek-ai/deepseek-coder-6.7b-instruct` (Good for code)
- `mistralai/mistral-7b-instruct` (Reliable)
- `nousresearch/nous-hermes-2-mixtral-8x7b-dpo` (High quality)

#### **3. DeepSeek (Best Quality - 1M tokens/month free)**
```bash
# Get free API key from https://platform.deepseek.com/
# Add to .env file:
DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

#### **4. Multiple DeepSeek Keys (5M tokens/month free)**
```bash
# Create 5 accounts for 5M free tokens/month
DEEPSEEK_API_KEY=your-first-deepseek-key
DEEPSEEK_API_KEY_2=your-second-deepseek-key
DEEPSEEK_API_KEY_3=your-third-deepseek-key
DEEPSEEK_API_KEY_4=your-fourth-deepseek-key
DEEPSEEK_API_KEY_5=your-fifth-deepseek-key
```

#### **5. Hugging Face (Free tier)**
```bash
# Get free API token from https://huggingface.co/
# Add to .env file:
HUGGINGFACE_API_TOKEN=your-huggingface-token-here
```

#### **6. OpenAI (Paid - if you have a key)**
```bash
# Add to .env file:
OPENAI_API_KEY=your-openai-api-key-here
```

---

## 🧠 **How AI Models Are Used**

### **1. Chat Interface**
- **API Testing**: Generates detailed test reports with actual HTTP requests
- **Status Reports**: Shows real system information and file structure
- **Debug Reports**: Provides system health and troubleshooting info
- **Help Guide**: Dynamic help based on current system state

### **2. Test Generation**
- **OpenAPI Tests**: Creates comprehensive test suites from API specs
- **Intelligent Test Cases**: Generates context-aware test scenarios
- **Error Handling**: Creates tests for edge cases and failures

### **3. Workflow Management**
- **Smart Orchestration**: AI-powered workflow execution
- **Error Recovery**: Automatic troubleshooting and recovery
- **Performance Optimization**: Intelligent resource management

### **4. Enterprise Features**
- **Multi-Platform Testing**: AI-assisted cross-platform validation
- **Security Analysis**: AI-powered security testing
- **Compliance Checking**: Automated compliance validation

---

## 🔄 **Fallback System**

### **Automatic Provider Selection**
```
1. Try Gemini AI (if API key configured)
2. Try OpenRouter (if API key configured)
3. Try DeepSeek (if API key configured)
4. Try Hugging Face (if API key configured)
5. Use Ollama (local, always available)
6. Use OpenAI (if API key configured)
```

### **Smart Model Selection**
- **For API Testing**: Uses models good at HTTP/API understanding
- **For Code Generation**: Uses coding-specialized models
- **For General Chat**: Uses conversational models
- **For Analysis**: Uses reasoning-focused models

---

## 📊 **Current Performance**

### **Working Features**
✅ **API Testing**: Real HTTP requests with detailed results
✅ **Status Reports**: Dynamic system information
✅ **System Info**: Platform and configuration details
✅ **Help Guide**: Comprehensive command documentation
✅ **Local AI**: Ollama providing fallback support

### **Missing Features**
❌ **Advanced AI Features**: Need API keys for full functionality
❌ **Test Generation**: Requires AI provider for intelligent test creation
❌ **Workflow AI**: Needs AI for smart workflow management
❌ **API Analysis**: Requires AI for comprehensive insights
❌ **Test Optimization**: Needs AI for smart improvements

---

## 🚀 **Quick Setup**

### **Option 1: Gemini AI (Recommended - Free, High Quality)**
```bash
# 1. Get free API key from https://makersuite.google.com/app/apikey
# 2. Create .env file:
echo "GOOGLE_API_KEY=your-key-here" > .env
# 3. Restart the server
pkill -f "start_unified_backend.py"
poetry run python start_unified_backend.py
```

### **Option 2: OpenRouter (Multiple Models)**
```bash
# 1. Get free API key from https://openrouter.ai/
# 2. Create .env file:
echo "OPENROUTER_API_KEY=your-key-here" > .env
# 3. Restart the server
pkill -f "start_unified_backend.py"
poetry run python start_unified_backend.py
```

### **Option 3: DeepSeek (Best Quality)**
```bash
# 1. Get free API key from https://platform.deepseek.com/
# 2. Create .env file:
echo "DEEPSEEK_API_KEY=your-key-here" > .env
# 3. Restart the server
pkill -f "start_unified_backend.py"
poetry run python start_unified_backend.py
```

### **Option 4: Multiple Free Keys (Maximum Tokens)**
```bash
# 1. Create 5 DeepSeek accounts
# 2. Create .env file with all keys:
cat > .env << EOF
DEEPSEEK_API_KEY=key1
DEEPSEEK_API_KEY_2=key2
DEEPSEEK_API_KEY_3=key3
DEEPSEEK_API_KEY_4=key4
DEEPSEEK_API_KEY_5=key5
EOF
# 3. Restart the server
pkill -f "start_unified_backend.py"
poetry run python start_unified_backend.py
```

---

## 🔍 **Testing AI Providers**

### **Check Current Status**
```bash
curl http://localhost:8000/api/chat/system-stats | python3 -m json.tool
```

### **Test AI Functionality**
```bash
# Test API testing (works without API keys)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test api https://jsonplaceholder.typicode.com"}'

# Test AI features (needs API keys)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "create tests for my API"}'
```

---

## 💡 **Key Benefits**

1. **🆓 Completely Free**: Use multiple free AI providers
2. **🔄 Automatic Fallback**: Never lose functionality
3. **🧠 Smart Selection**: Uses best model for each task
4. **📈 Scalable**: Add more API keys for more tokens
5. **🔒 Reliable**: Local Ollama as ultimate fallback

---

## 🎯 **Next Steps**

1. **Add Gemini AI API key** for immediate improvement (recommended)
2. **Add OpenRouter API key** for multiple models
3. **Add DeepSeek API key** for best quality
4. **Create multiple accounts** for maximum free tokens
5. **Test all AI features** once configured

**The system is already working with local AI, but adding API keys will unlock full AI-powered features!** 🦖✨ 