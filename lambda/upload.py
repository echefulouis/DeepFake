from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.logging import correlation_paths
from typing import Dict
import boto3
import os
import base64
import uuid
import json
import requests

cors_config = CORSConfig(
    allow_origin="*",
    allow_headers=["Content-Type", "Authorization", "X-Amz-Date", "X-Api-Key", "X-Amz-Security-Token"],
    max_age=300,
    expose_headers=["Content-Type", "Authorization"],
    allow_credentials=True
)

logger = Logger(service="ReceiptApp")
tracer = Tracer(service="ReceiptApp")
app = APIGatewayRestResolver(cors=cors_config)

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def build_response(status_code: int, body: Dict) -> Dict:
    logger.info(f"Building response with status code: {status_code}")
    return {
        "statusCode": status_code,
        "body": body,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "application/json"
        }
    }

@app.post("/upload")
@tracer.capture_method
def upload_file():
    try:
        body = app.current_event.json_body
        base64_image = body.get('image')
        
        if not base64_image:
            return build_response(400, {"error": "No image provided"})
        
        # Get API key from Secrets Manager
        secrets_client = boto3.client('secretsmanager')
        secret_value = secrets_client.get_secret_value(SecretId=os.environ['API_SECRET_ARN'])
        api_key = secret_value['SecretString']
        
        # Call NVIDIA deepfake detection API
        invoke_url = "https://ai.api.nvidia.com/v1/cv/hive/deepfake-image-detection"
        
        payload = {
            "input": [f"data:image/png;base64,{base64_image}"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        response = requests.post(invoke_url, headers=headers, json=payload, timeout=30)
        api_response = response.json()
        
        # Remove the image key from response if it exists
        if 'image' in api_response:
            del api_response['image']
        
        logger.info(f"NVIDIA API Response: {api_response}")
        
        # Save image to S3
        image_data = base64.b64decode(base64_image)
        file_key = f"raw/{uuid.uuid4()}.jpg"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=image_data,
            ContentType='image/jpeg'
        )
        
        return build_response(200, {
            "message": "Analysis complete",
            "detection_result": api_response
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return build_response(500, {"error": "Analysis failed"})

    
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Lambda handler started")
    return app.resolve(event, context)
