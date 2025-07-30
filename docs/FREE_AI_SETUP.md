# 🆓 **Free AI Models Setup Guide for RESTACERATOPS**

## 🎯 **Overview**

RESTACERATOPS now supports **completely free AI models**! You can use these instead of paid OpenAI models and get excellent results.

## 🚀 **Available Free AI Models**

### **1. DeepSeek (Recommended)**
- **Free Tier**: 1M tokens/month
- **Quality**: Excellent for coding and technical tasks
- **Setup**: Very easy
- **Cost**: Completely free

### **2. Ollama (Local Models)**
- **Free Tier**: Unlimited usage
- **Quality**: Good for general tasks
- **Setup**: Requires local installation
- **Cost**: Completely free

### **3. Hugging Face**
- **Free Tier**: Available for many models
- **Quality**: Varies by model
- **Setup**: Moderate complexity
- **Cost**: Completely free

---

## 🔧 **Setup Instructions**

### **Option 1: DeepSeek (Easiest)**

1. **Get Free API Key**:
   - Go to [https://platform.deepseek.com/](https://platform.deepseek.com/)
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Configure RESTACERATOPS**:
   ```bash
   # Edit your .env file
   FREE_MODEL_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your-deepseek-api-key-here
   ```

3. **Install Dependencies**:
   ```bash
   poetry install
   ```

4. **Restart the Backend**:
   ```bash
   poetry run uvicorn api.backend:app --reload --host 0.0.0.0 --port 8000
   ```

### **Option 2: Ollama (Local)**

1. **Install Ollama**:
   ```bash
   # macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Start Ollama Service**:
   ```bash
   ollama serve
   ```

3. **Download a Model**:
   ```bash
   # Lightweight model (recommended)
   ollama pull llama3.2:3b
   
   # Or use a coding model
   ollama pull codellama:7b
   ```

4. **Configure RESTACERATOPS**:
   ```bash
   # Edit your .env file
   FREE_MODEL_PROVIDER=ollama
   ```

5. **Install Dependencies**:
   ```bash
   poetry install
   ```

6. **Restart the Backend**:
   ```bash
   poetry run uvicorn api.backend:app --reload --host 0.0.0.0 --port 8000
   ```

### **Option 3: Hugging Face**

1. **Get Free Token**:
   - Go to [https://huggingface.co/](https://huggingface.co/)
   - Sign up for a free account
   - Go to Settings → Access Tokens
   - Create a new token

2. **Configure RESTACERATOPS**:
   ```bash
   # Edit your .env file
   FREE_MODEL_PROVIDER=huggingface
   HUGGINGFACE_API_TOKEN=your-huggingface-token-here
   ```

3. **Install Dependencies**:
   ```bash
   poetry install
   ```

4. **Restart the Backend**:
   ```bash
   poetry run uvicorn api.backend:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 🎯 **Model Comparison**

| Feature | DeepSeek | Ollama | Hugging Face |
|---------|----------|--------|--------------|
| **Setup Difficulty** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐ Medium |
| **Response Quality** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Very Good |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Fast |
| **Cost** | 🆓 Free | 🆓 Free | 🆓 Free |
| **Offline** | ❌ No | ✅ Yes | ❌ No |
| **Customization** | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐ High |

---

## 🧪 **Testing Your Setup**

### **Test the AI Response**:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Can you help me test my API?"}'
```

### **Expected Response**:
You should get a detailed, helpful response from your chosen AI model instead of the fallback system.

### **Check Model Status**:
```bash
curl http://localhost:8000/api/system/stats
```

---

## 🔄 **Switching Between Models**

You can easily switch between models by changing the `FREE_MODEL_PROVIDER` in your `.env` file:

```bash
# For DeepSeek
FREE_MODEL_PROVIDER=deepseek

# For Ollama
FREE_MODEL_PROVIDER=ollama

# For Hugging Face
FREE_MODEL_PROVIDER=huggingface
```

Then restart the backend:
```bash
poetry run uvicorn api.backend:app --reload --host 0.0.0.0 --port 8000
```

---

## 🛠️ **Troubleshooting**

### **DeepSeek Issues**:
- **Error**: "API key not found"
  - **Solution**: Make sure your `DEEPSEEK_API_KEY` is set correctly
- **Error**: "Rate limit exceeded"
  - **Solution**: Wait a bit or upgrade to paid plan

### **Ollama Issues**:
- **Error**: "Connection refused"
  - **Solution**: Make sure `ollama serve` is running
- **Error**: "Model not found"
  - **Solution**: Run `ollama pull llama3.2:3b`

### **Hugging Face Issues**:
- **Error**: "Token not found"
  - **Solution**: Check your `HUGGINGFACE_API_TOKEN`
- **Error**: "Model not available"
  - **Solution**: Try a different model ID

### **General Issues**:
- **Fallback to enhanced responses**: This is normal if models fail to load
- **Slow responses**: Some models are slower than others
- **Memory usage**: Ollama models use local RAM

---

## 🎉 **Benefits of Free AI Models**

1. **No Cost**: Completely free to use
2. **No Rate Limits**: (except DeepSeek's 1M tokens/month)
3. **Privacy**: Ollama runs locally, no data sent to cloud
4. **Customization**: Full control over models and parameters
5. **Reliability**: No dependency on external services (Ollama)

---

## 🚀 **Next Steps**

1. **Choose your preferred model** from the options above
2. **Follow the setup instructions** for your chosen model
3. **Test the AI responses** to ensure everything works
4. **Enjoy free AI-powered API testing!** 🦖

Your RESTACERATOPS will now use the free AI model you've configured, providing intelligent responses without any costs! 