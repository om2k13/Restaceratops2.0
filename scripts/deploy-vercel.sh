#!/bin/bash

# 🦖 Deploy Restaceratops to Vercel (100% FREE)
echo "🦖 Deploying Restaceratops to Vercel..."
echo "======================================"

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Make sure you're in the project directory."
    exit 1
fi

echo "✅ Project files ready!"
echo ""

# Deploy to Vercel
echo "🚀 Starting Vercel deployment..."
echo "When prompted:"
echo "  - Choose 'Y' to link to existing project (or create new)"
echo "  - Choose your Vercel account"
echo "  - Project name: restaceratops (or press Enter for default)"
echo "  - Choose 'Y' to override settings"
echo ""

vercel --prod

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📝 Next steps:"
echo "1. Set environment variables in Vercel dashboard:"
echo "   - BASE_URL=https://your-api.com"
echo "   - BEARER_TOKEN=your-token"
echo ""
echo "2. Your agent will be live at:"
echo "   https://your-project-name.vercel.app/api/restaceratops"
echo ""
echo "3. Test your deployment by visiting the URL above"
echo ""
echo "🦖 Your Restaceratops is now running in the cloud for FREE!" 