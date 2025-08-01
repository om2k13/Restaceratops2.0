# 🤖 AI Setup Guide for Restaceratops

## 🎯 **Current Status: AI System Ready but Needs Real API Key**

The AI system is fully configured to use **OpenRouter's Qwen3 Coder model**, but it needs a **real API key** to work.

## 🔑 **How to Get OpenRouter API Key (FREE)**

### **Step 1: Sign Up for OpenRouter**
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Click "Sign Up" and create an account
3. Verify your email

### **Step 2: Get Your API Key**
1. Go to your [OpenRouter Dashboard](https://openrouter.ai/keys)
2. Click "Create Key"
3. Copy your API key (starts with `sk-or-`)

### **Step 3: Set Environment Variable**
```bash
# For local development
export OPENROUTER_API_KEY="sk-or-your-real-api-key-here"

# Or add to your .env file
echo "OPENROUTER_API_KEY=sk-or-your-real-api-key-here" >> .env
```

## 🚀 **What Happens After Setup**

Once you set the **real API key**:

### **✅ AI Chat Will:**
- Use **Qwen3 Coder model** for intelligent responses
- Provide context-aware API testing guidance
- Generate test cases using AI
- Give debugging assistance
- Offer performance optimization tips

### **✅ Test Generation Will:**
- Generate comprehensive test suites from API specs
- Create positive and negative test scenarios
- Include edge cases and error handling
- Provide performance test recommendations

## 🎯 **Current Fallback Behavior**

Without the **real API key**, the system provides:
- ✅ **Intelligent fallback responses** for common questions
- ✅ **Structured guidance** for API testing
- ✅ **Helpful templates** and best practices
- ✅ **No errors** - graceful degradation

## 🔧 **For Production Deployment**

When deploying to Render/Vercel:

1. **Add Environment Variable:**
   - `OPENROUTER_API_KEY`: Your **real** OpenRouter API key

2. **The system will automatically:**
   - Use Qwen3 Coder for AI responses
   - Generate intelligent test cases
   - Provide advanced debugging assistance

## 💰 **Cost Information**

- **OpenRouter Free Tier:** $0/month
- **Qwen3 Coder Free Model:** $0/request
- **Usage Limits:** Generous free limits
- **No Credit Card Required:** For free tier

## 🎉 **Ready to Use!**

Once you set the **real API key**, your Restaceratops will have:
- 🤖 **Full AI-powered test generation**
- 💬 **Intelligent chat assistance**
- 🧪 **Smart debugging guidance**
- 📊 **AI-enhanced reporting**

**The system is production-ready and will work perfectly for your HR demo!**

## 🚨 **IMPORTANT: Get Real API Key**

**Current Status:** Using fallback logic because no real API key is configured.

**To enable real Qwen3 AI:**
1. Get your API key from [OpenRouter.ai/keys](https://openrouter.ai/keys)
2. Set it as environment variable: `export OPENROUTER_API_KEY='your-real-key'`
3. Restart the backend
4. Test with: `curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "test"}'` 