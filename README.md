# DeepFake Detection System

A web application that detects deepfake images using NVIDIA's AI detection API. Built with React frontend and AWS serverless backend.

## What it does

Upload an image and get instant analysis showing whether it's authentic or artificially generated. The system uses a deepfake detection model to analyze facial features and provides confidence scores.

## Quick Start

1. Get your NVIDIA API key from [here](https://build.nvidia.com/hive/deepfake-image-detection?snippet_tab=Python)

2. Add it to `.env` file:
```
api-key = "nvapi-your-key-here"
```

3. Deploy everything:
```bash
./deploy.sh
```

4. Run the frontend locally:
```bash
cd frontend
npm install
npm run dev
```

## How it works

The app sends your image to AWS Lambda, which calls NVIDIA's API for analysis. Results show:
- Green card = Real image
- Red card = Deepfake detected
- Confidence percentages for both detection and accuracy

Images are temporarily stored in S3 for processing.

## Tech Stack

**Backend:** AWS Lambda, API Gateway, S3, Secrets Manager, Python
**Frontend:** React, Vite, Axios
**AI:** Deepfake Detection API

## Project Structure

```
DeepFake/
├── frontend/     # React app
├── lambda/       # AWS Lambda functions  
├── stacks/       # CDK infrastructure
├── deploy.sh     # One-click deployment
└── .env          # Your API key goes here
```

## Requirements

- AWS CLI configured
- Node.js 18+
- Python 3.12+
- AWS CDK v2

## Troubleshooting

- Check CloudWatch logs if Lambda fails
- Verify your NVIDIA API key is active
- Make sure AWS credentials are set up

## License

MIT