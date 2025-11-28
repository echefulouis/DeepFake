from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager,
    SecretValue
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()

class SecretsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_key = os.getenv('api-key')
        if not api_key:
            raise ValueError("api-key not found in .env file")

        self.api_key_secret = secretsmanager.Secret(
            self, "ApiKeySecret",
            secret_name="deepfake/api-key",
            description="NVIDIA API Key for DeepFake application",
            secret_string_value=SecretValue.unsafe_plain_text(api_key)
        )