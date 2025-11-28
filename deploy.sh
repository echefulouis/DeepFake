#!/bin/bash

# Create dist folder if it doesn't exist to avoid frontend deployment errors
mkdir -p frontend/dist
echo "temporary file" > frontend/dist/index.html

# Deploy infrastructure stacks (excluding frontend)
cdk deploy S3Stack DynamoDBStack SecretsStack LambdaStack EventBridgeStack ApiGatewayStack --require-approval never 2>&1 | tee deployment-output.txt

# Extract API endpoint and create frontend .env file
{
  echo "VITE_API_ENDPOINT=$(grep "DeepFakeApi" deployment-output.txt | awk -F'=' '{print $2}' | tr -d ' ')"
} > frontend/.env

# Build and deploy frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy frontend stack
echo "Deploying frontend to S3 + CloudFront..."
cdk deploy FrontendStack --require-approval never

echo "Deployment complete. Check CloudFront URL in the output above."