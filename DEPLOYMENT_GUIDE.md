# 🚀 **Restaceratops Deployment Guide**
## Vercel (Frontend) + Render (Backend)

---

## 📋 **Prerequisites**

1. **GitHub Account** - Your code should be on GitHub
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Render Account** - Sign up at [render.com](https://render.com)
4. **Environment Variables** - You'll need API keys

---

## 🔧 **Step 1: Prepare Environment Variables**

### **Required Environment Variables:**

```bash
# Backend (Render)
OPENROUTER_API_KEY=your_openrouter_api_key
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=restaceratops

# Frontend (Vercel)
VITE_API_BASE_URL=https://your-backend-app.onrender.com
```

### **How to Get These:**

1. **OpenRouter API Key:**
   - Go to [openrouter.ai](https://openrouter.ai)
   - Sign up and get your API key

2. **MongoDB Atlas:**
   - Go to [mongodb.com/atlas](https://mongodb.com/atlas)
   - Create a free cluster
   - Get your connection string

---

## 🌐 **Step 2: Deploy Backend to Render**

### **2.1 Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account

### **2.2 Deploy Backend Service**
1. **Click "New +" → "Web Service"**
2. **Connect your GitHub repository**
3. **Configure the service:**

```yaml
Name: restaceratops-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT
Root Directory: backend
```

### **2.3 Set Environment Variables**
In Render dashboard, go to your service → Environment → Add:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=restaceratops
```

### **2.4 Deploy**
- Click "Create Web Service"
- Wait for deployment (usually 2-3 minutes)
- Note your backend URL: `https://your-app-name.onrender.com`

---

## ⚡ **Step 3: Deploy Frontend to Vercel**

### **3.1 Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account

### **3.2 Deploy Frontend**
1. **Click "New Project"**
2. **Import your GitHub repository**
3. **Configure the project:**

```json
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### **3.3 Set Environment Variables**
In Vercel dashboard, go to your project → Settings → Environment Variables:

```bash
VITE_API_BASE_URL=https://your-backend-app.onrender.com
```

### **3.4 Deploy**
- Click "Deploy"
- Wait for deployment (usually 1-2 minutes)
- Your frontend will be available at: `https://your-app-name.vercel.app`

---

## 🔗 **Step 4: Connect Frontend to Backend**

### **4.1 Update API Base URL**
Make sure your frontend is pointing to the correct backend URL:

```typescript
// frontend/src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

### **4.2 Test the Connection**
1. Go to your Vercel frontend URL
2. Try the AI Chat feature
3. Test file upload functionality
4. Verify test execution works

---

## 🛠️ **Step 5: Troubleshooting**

### **Common Issues:**

#### **Backend Issues:**
```bash
# Check Render logs
- Go to your Render service → Logs
- Look for Python errors or import issues

# Common fixes:
- Ensure all dependencies are in requirements.txt
- Check environment variables are set correctly
- Verify MongoDB connection string format
```

#### **Frontend Issues:**
```bash
# Check Vercel logs
- Go to your Vercel project → Functions → View Function Logs

# Common fixes:
- Verify VITE_API_BASE_URL is set correctly
- Check CORS settings in backend
- Ensure build completes successfully
```

#### **CORS Issues:**
If you get CORS errors, update your backend CORS settings:

```python
# backend/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 **Step 6: Monitor Your Deployment**

### **Render Monitoring:**
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory usage
- **Health Checks**: Automatic monitoring

### **Vercel Monitoring:**
- **Analytics**: Page views, performance
- **Functions**: API call logs
- **Speed Insights**: Performance metrics

---

## 🔄 **Step 7: Continuous Deployment**

### **Automatic Deployments:**
- **Render**: Automatically deploys on git push to main branch
- **Vercel**: Automatically deploys on git push to main branch

### **Manual Deployments:**
```bash
# Trigger manual deployment on Render
- Go to your service → Manual Deploy → Deploy Latest Commit

# Trigger manual deployment on Vercel
- Go to your project → Deployments → Redeploy
```

---

## 🎯 **Step 8: Custom Domains (Optional)**

### **Render Custom Domain:**
1. Go to your service → Settings → Custom Domains
2. Add your domain
3. Configure DNS records

### **Vercel Custom Domain:**
1. Go to your project → Settings → Domains
2. Add your domain
3. Configure DNS records

---

## ✅ **Final Checklist**

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] API connection tested
- [ ] File upload working
- [ ] AI chat functional
- [ ] Test execution working

---

## 🆘 **Need Help?**

### **Support Resources:**
- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Issues**: Create an issue in your repository

### **Common Commands:**
```bash
# Check deployment status
curl https://your-backend.onrender.com/health

# Test API endpoints
curl https://your-backend.onrender.com/api/health

# View logs
# Render: Dashboard → Logs
# Vercel: Dashboard → Functions → Logs
```

---

**🎉 Congratulations! Your Restaceratops API Testing Platform is now live!** 