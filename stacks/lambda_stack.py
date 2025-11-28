from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_secretsmanager as secretsmanager,
    Duration
)
from constructs import Construct

class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 image_bucket: s3.Bucket,
                 api_secret: secretsmanager.Secret,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer = _lambda.LayerVersion(
            self, 'lambda_layer',
            code=_lambda.Code.from_asset('./layers/layer.zip'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],  
        )
        
        request_layer = _lambda.LayerVersion(
            self, 'request_layer',
            code=_lambda.Code.from_asset('./layers/request.zip'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],  
        )
        
        self.upload_lambda = _lambda.Function(
            self, 'upload_lambda',
            function_name="deepfake_upload_lambda_function",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda'),
            handler='upload.lambda_handler',
            layers=[layer, request_layer],
            tracing=_lambda.Tracing.ACTIVE,
            timeout=Duration.seconds(30),
            environment={
                'BUCKET_NAME': image_bucket.bucket_name,
                'API_SECRET_ARN': api_secret.secret_arn,
                "POWERTOOLS_SERVICE_NAME": "recieptApp"
            }
            
        )
        
        api_secret.grant_read(self.upload_lambda)
        image_bucket.grant_write(self.upload_lambda)

