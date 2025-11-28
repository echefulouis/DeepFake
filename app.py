#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks.lambda_stack import LambdaStack
from stacks.s3_stack import S3Stack
from stacks.apigateway_satck import ApiGatewayStack
from stacks.dynamodb_stack import DynamoDBStack
from stacks.frontend_stack import FrontendStack
from stacks.secrets_stack import SecretsStack

app = cdk.App()

s3_stack = S3Stack(app, "S3Stack")
dynamodb_stack = DynamoDBStack(app, "DynamoDBStack")
secrets_stack = SecretsStack(app, "SecretsStack")
lambda_stack = LambdaStack(app, "LambdaStack", image_bucket=s3_stack.image_bucket, api_secret=secrets_stack.api_key_secret)
apigateway_stack = ApiGatewayStack(app, "ApiGatewayStack", upload_lambda=lambda_stack.upload_lambda)
frontend_stack = FrontendStack(app, "FrontendStack")

app.synth()
