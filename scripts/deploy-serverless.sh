#!/bin/bash

# 🦖 Restaceratops Serverless Deployment Script
# Deploy your API testing agent to the cloud for FREE!

set -e

echo "🦖 Restaceratops Serverless Deployment"
echo "======================================"
echo ""

# Check which deployment option the user wants
echo "Choose your serverless platform:"
echo "1. Vercel (Easiest - 100% FREE)"
echo "2. Netlify (Simple - 100% FREE)"
echo "3. AWS Lambda (Best Value - Practically FREE)"
echo "4. Show cost analysis"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚀 Deploying to Vercel (100% FREE)..."
        
        # Check if Vercel CLI is installed
        if ! command -v vercel &> /dev/null; then
            echo "📦 Installing Vercel CLI..."
            npm install -g vercel
        fi
        
        echo "✅ Vercel CLI ready!"
        echo ""
        echo "🔧 Next steps:"
        echo "1. Run: vercel"
        echo "2. Follow the prompts"
        echo "3. Set environment variables:"
        echo "   - BASE_URL=https://your-api.com"
        echo "   - BEARER_TOKEN=your-token"
        echo ""
        echo "🎉 Your agent will be live at: https://your-app.vercel.app/api/restaceratops"
        ;;
        
    2)
        echo "🚀 Deploying to Netlify (100% FREE)..."
        
        # Check if Netlify CLI is installed
        if ! command -v netlify &> /dev/null; then
            echo "📦 Installing Netlify CLI..."
            npm install -g netlify-cli
        fi
        
        echo "✅ Netlify CLI ready!"
        echo ""
        echo "🔧 Next steps:"
        echo "1. Run: netlify deploy"
        echo "2. Choose 'Create & configure a new site'"
        echo "3. Set environment variables in Netlify dashboard"
        echo ""
        echo "🎉 Your agent will be live at: https://your-app.netlify.app/.netlify/functions/restaceratops"
        ;;
        
    3)
        echo "🚀 Deploying to AWS Lambda (Practically FREE)..."
        
        # Check if AWS CLI is installed
        if ! command -v aws &> /dev/null; then
            echo "📦 Installing AWS CLI..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install awscli
            else
                echo "Please install AWS CLI from: https://aws.amazon.com/cli/"
                exit 1
            fi
        fi
        
        echo "✅ AWS CLI ready!"
        echo ""
        echo "🔧 Next steps:"
        echo "1. Configure AWS: aws configure"
        echo "2. Deploy: aws cloudformation create-stack --stack-name restaceratops --template-body file://deployments/aws-lambda.yml"
        echo "3. Set your API credentials as parameters"
        echo ""
        echo "🎉 Your agent will run daily at 1 AM UTC"
        ;;
        
    4)
        echo "💰 Cost Analysis:"
        echo "=================="
        echo ""
        echo "🆓 FREE Options:"
        echo "• Vercel: 100GB-hours/month (100% FREE forever)"
        echo "• Netlify: 125K invocations/month (100% FREE forever)"
        echo ""
        echo "💸 Nearly FREE Options:"
        echo "• AWS Lambda: 1M requests/month FREE, then ~$0.01/month"
        echo "• Google Cloud: 2M invocations/month FREE, then ~$0.03/month"
        echo ""
        echo "📊 Typical Usage (Daily API tests):"
        echo "• 24 tests/day = 720 requests/month"
        echo "• Cost: $0-5/month (practically free!)"
        echo ""
        echo "🎯 Recommendation:"
        echo "• Personal use: Vercel (100% FREE)"
        echo "• Production: AWS Lambda (practically FREE)"
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🦖 Your Restaceratops agent is ready for serverless deployment!"
echo "📚 See deployments/serverless-costs.md for detailed instructions."
echo ""
echo "💡 Pro tip: Start with Vercel for the easiest deployment!" 