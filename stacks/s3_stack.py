from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.image_bucket = s3.Bucket(
            self, "ImageBucket",
            cors=[s3.CorsRule(
                allowed_methods=[s3.HttpMethods.GET],
                allowed_origins=["*"], 
                allowed_headers=["*"],
            )],
            removal_policy=RemovalPolicy.RETAIN,
            versioned=True,

        )

