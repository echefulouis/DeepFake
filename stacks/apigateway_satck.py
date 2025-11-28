from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda
)
from constructs import Construct

class ApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, upload_lambda: _lambda.Function, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(
            self, "DeepFakeApi",
            rest_api_name="DeepFake API",
            deploy_options=apigateway.StageOptions(
                stage_name="prod",
                tracing_enabled=True,
                data_trace_enabled=True,
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization"]
            )
        )

        upload_integration = apigateway.LambdaIntegration(upload_lambda)
        api.root.add_resource("upload").add_method("POST", upload_integration)