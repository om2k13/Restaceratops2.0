# 🆓 **Multi-Provider AI Setup Guide - RESTACERATOPS**

## 🎯 **Overview**

RESTACERATOPS now supports **automatic AI provider fallback** with multiple free API keys! If one provider fails or hits its limit, it automatically switches to the next available provider.

## 🚀 **How It Works**

### **Automatic Fallback System**
1. **Primary**: DeepSeek (Best quality, 1M tokens/month free)
2. **Secondary**: Hugging Face (Good quality, free tier)
3. **Tertiary**: Ollama (Local, unlimited, always available)
4. **Fallback**: OpenAI (If you have a paid key)

### **Smart Provider Management**
- ✅ **Automatic Detection**: Tests each provider on startup
- ✅ **Failover**: Switches to next provider if one fails
- ✅ **Rate Limit Handling**: Automatically handles daily limits
- ✅ **Health Monitoring**: Tracks provider status in real-time
- ✅ **Recovery**: Retries failed providers after some time

---

## 🔑 **Getting Multiple Free API Keys**

### **1. DeepSeek (Primary - Best Quality)**

**Step 1: Create Multiple Accounts**
- Go to [https://platform.deepseek.com/](https://platform.deepseek.com/)
- Create 5 different accounts using different email addresses
- Each account gets **1M tokens/month free**

**Step 2: Get API Keys**
- Log into each account
- Go to API Keys section
- Copy each API key

**Step 3: Configure RESTACERATOPS**
```bash
# Edit your .env file
DEEPSEEK_API_KEY=your-first-deepseek-key
DEEPSEEK_API_KEY_2=your-second-deepseek-key
DEEPSEEK_API_KEY_3=your-third-deepseek-key
DEEPSEEK_API_KEY_4=your-fourth-deepseek-key
DEEPSEEK_API_KEY_5=your-fifth-deepseek-key
```

**Total Free Tokens**: 5M tokens/month (5 accounts × 1M each)

### **2. Hugging Face (Secondary - Good Quality)**

**Step 1: Create Multiple Accounts**
- Go to [https://huggingface.co/](https://huggingface.co/)
- Create 5 different accounts using different email addresses
- Each account gets free API access

**Step 2: Get API Tokens**
- Log into each account
- Go to Settings → Access Tokens
- Create a new token for each account

**Step 3: Configure RESTACERATOPS**
```bash
# Edit your .env file
HUGGINGFACE_API_TOKEN=your-first-huggingface-token
HUGGINGFACE_API_TOKEN_2=your-second-huggingface-token
HUGGINGFACE_API_TOKEN_3=your-third-huggingface-token
HUGGINGFACE_API_TOKEN_4=your-fourth-huggingface-token
HUGGINGFACE_API_TOKEN_5=your-fifth-huggingface-token
```

### **3. Ollama (Local - Unlimited)**

**Step 1: Install Ollama**
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

**Step 2: Start Ollama & Download Model**
```bash
# Start the service
ollama serve

# Download a model (in another terminal)
ollama pull llama3.2:3b
```

**Step 3: No Configuration Needed**
- Ollama is automatically detected and used as fallback
- No API keys required
- Unlimited usage

---

## 🎯 **Complete Setup Example**

### **Step 1: Get All API Keys**
```bash
# Create accounts and get keys from:
# - DeepSeek: https://platform.deepseek.com/ (5 accounts)
# - Hugging Face: https://huggingface.co/ (5 accounts)
# - Ollama: https://ollama.ai/ (local installation)
```

### **Step 2: Configure Environment**
```bash
# Edit your .env file with all your keys:
DEEPSEEK_API_KEY=sk-1234567890abcdef...
DEEPSEEK_API_KEY_2=sk-0987654321fedcba...
DEEPSEEK_API_KEY_3=sk-abcdef1234567890...
DEEPSEEK_API_KEY_4=sk-fedcba0987654321...
DEEPSEEK_API_KEY_5=sk-567890abcdef1234...

HUGGINGFACE_API_TOKEN=hf_1234567890abcdef...
HUGGINGFACE_API_TOKEN_2=hf_0987654321fedcba...
HUGGINGFACE_API_TOKEN_3=hf_abcdef1234567890...
HUGGINGFACE_API_TOKEN_4=hf_fedcba0987654321...
HUGGINGFACE_API_TOKEN_5=hf_567890abcdef1234...
```

### **Step 3: Install Dependencies**
```bash
poetry install
```

### **Step 4: Start Services**
```bash
# Start Ollama (if using local models)
ollama serve

# Start RESTACERATOPS
poetry run uvicorn api.backend:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 **Provider Comparison**

| Provider | Accounts | Free Tokens | Quality | Setup | Reliability |
|----------|----------|-------------|---------|-------|-------------|
| **DeepSeek** | 5 | 5M/month | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐ Easy | ⭐⭐⭐⭐ High |
| **Hugging Face** | 5 | Unlimited* | ⭐⭐⭐⭐ Very Good | ⭐⭐ Medium | ⭐⭐⭐ Good |
| **Ollama** | 1 | Unlimited | ⭐⭐⭐ Good | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Perfect |
| **OpenAI** | 1 | Paid | ⭐⭐⭐⭐⭐ Excellent | ⭐ Easy | ⭐⭐⭐⭐⭐ Perfect |

*Within reasonable usage limits

---

## 🧪 **Testing Your Multi-Provider Setup**

### **Test Provider Status**
```bash
curl http://localhost:8000/api/system/stats
```

**Expected Response**:
```json
{
  "ai_system": {
    "total_providers": 11,
    "working_providers": 11,
    "failed_providers": [],
    "current_provider": "DeepSeek-1",
    "providers": [
      {"name": "DeepSeek-1", "type": "deepseek", "status": "working"},
      {"name": "DeepSeek-2", "type": "deepseek", "status": "working"},
      {"name": "HuggingFace-1", "type": "huggingface", "status": "working"},
      {"name": "Ollama-Local", "type": "ollama", "status": "working"}
    ]
  }
}
```

### **Test AI Response**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Can you help me test my API?"}'
```

### **Test Automatic Fallback**
1. **Simulate Provider Failure**: Stop Ollama service
2. **Check Logs**: Watch for automatic provider switching
3. **Verify Response**: AI should still respond using other providers

---

## 🔄 **Automatic Fallback Behavior**

### **When a Provider Fails**
1. **Rate Limit Exceeded**: Automatically switches to next provider
2. **Network Error**: Tries next provider immediately
3. **API Error**: Marks provider as failed and continues
4. **All Providers Failed**: Falls back to enhanced responses

### **Provider Recovery**
- **Failed providers** are retried after some time
- **Rate limits** reset daily
- **Network issues** are retried automatically
- **Health monitoring** tracks provider status

---

## 🛠️ **Troubleshooting**

### **DeepSeek Issues**
- **Error**: "Rate limit exceeded"
  - **Solution**: System automatically switches to next DeepSeek key
- **Error**: "API key not found"
  - **Solution**: Check your `.env` file configuration

### **Hugging Face Issues**
- **Error**: "Token not found"
  - **Solution**: Verify all tokens in `.env` file
- **Error**: "Model not available"
  - **Solution**: System automatically tries next provider

### **Ollama Issues**
- **Error**: "Connection refused"
  - **Solution**: Make sure `ollama serve` is running
- **Error**: "Model not found"
  - **Solution**: Run `ollama pull llama3.2:3b`

### **General Issues**
- **All providers failed**: Check network connectivity
- **No AI responses**: Verify at least one provider is configured
- **Slow responses**: Some providers are slower than others

---

## 🎉 **Benefits of Multi-Provider Setup**

### **Reliability**
- ✅ **Always Available**: At least one provider working
- ✅ **No Downtime**: Automatic failover
- ✅ **Redundancy**: Multiple backup options

### **Cost Efficiency**
- ✅ **Completely Free**: 5M+ tokens/month
- ✅ **No Rate Limits**: Ollama unlimited usage
- ✅ **No Credit Cards**: All providers free

### **Performance**
- ✅ **Best Quality**: DeepSeek for important tasks
- ✅ **Fast Response**: Multiple providers reduce latency
- ✅ **Load Distribution**: Spreads usage across providers

### **Flexibility**
- ✅ **Easy Setup**: Just add API keys
- ✅ **Automatic Management**: No manual switching needed
- ✅ **Monitoring**: Real-time provider status

---

## 🚀 **Next Steps**

1. **Get Multiple API Keys** from DeepSeek and Hugging Face
2. **Configure Your `.env` File** with all keys
3. **Install Ollama** for local fallback
4. **Test the System** with the provided commands
5. **Monitor Provider Status** in the system stats
6. **Enjoy Unlimited AI** with automatic fallback! 🦖

Your RESTACERATOPS will now have **bulletproof AI availability** with multiple free providers and automatic failover! 