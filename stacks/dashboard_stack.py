from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_cloudwatch as cloudwatch,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct


class DashboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 upload_lambda: _lambda.Function,
                 api_gateway: apigateway.RestApi,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self, "DeepFakeMonitoringDashboard",
            dashboard_name="DeepFake-Monitoring-Dashboard"
        )

        # Lambda Metrics
        lambda_invocations = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Invocations",
            dimensions_map={
                "FunctionName": upload_lambda.function_name
            },
            statistic="Sum",
            period=Duration.minutes(5),  # Standardized to 5 minutes for consistency
            label="Lambda Invocations"
        )

        lambda_errors = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Errors",
            dimensions_map={
                "FunctionName": upload_lambda.function_name
            },
            statistic="Sum",
            period=Duration.minutes(5),
            label="Lambda Errors"
        )

        lambda_duration = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Duration",
            dimensions_map={
                "FunctionName": upload_lambda.function_name
            },
            statistic="Average",
            period=Duration.minutes(5),
            label="Lambda Duration (ms)"
        )

        lambda_throttles = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="Throttles",
            dimensions_map={
                "FunctionName": upload_lambda.function_name
            },
            statistic="Sum",
            period=Duration.minutes(5),
            label="Lambda Throttles"
        )

        # Cold Start Metrics using Lambda Insights
        # Lambda Insights provides enhanced metrics including cold start tracking
        # These metrics are more reliable and comprehensive than standard InitDuration
        lambda_insights_init_duration = cloudwatch.Metric(
            namespace="LambdaInsights",
            metric_name="init_duration",
            dimensions_map={
                "function_name": upload_lambda.function_name
            },
            statistic="Average",
            period=Duration.minutes(5),
            label="Cold Start Init Duration (ms) - Average (Lambda Insights)"
        )

        # Maximum InitDuration from Lambda Insights
        lambda_insights_init_duration_max = cloudwatch.Metric(
            namespace="LambdaInsights",
            metric_name="init_duration",
            dimensions_map={
                "function_name": upload_lambda.function_name
            },
            statistic="Maximum",
            period=Duration.minutes(5),
            label="Cold Start Init Duration (ms) - Maximum (Lambda Insights)"
        )

        # Minimum InitDuration from Lambda Insights
        lambda_insights_init_duration_min = cloudwatch.Metric(
            namespace="LambdaInsights",
            metric_name="init_duration",
            dimensions_map={
                "function_name": upload_lambda.function_name
            },
            statistic="Minimum",
            period=Duration.minutes(5),
            label="Cold Start Init Duration (ms) - Minimum (Lambda Insights)"
        )

        # Cold Start Count from Lambda Insights
        # Use SampleCount of init_duration - each sample represents one cold start
        # Lambda Insights doesn't have a direct cold_start_count metric
        lambda_insights_cold_start_count = cloudwatch.Metric(
            namespace="LambdaInsights",
            metric_name="init_duration",
            dimensions_map={
                "function_name": upload_lambda.function_name
            },
            statistic="SampleCount",  # Count samples = count cold starts
            period=Duration.minutes(5),
            label="Cold Start Count (Lambda Insights)"
        )

        # Concurrent Executions - helps identify when new containers are created
        lambda_concurrent = cloudwatch.Metric(
            namespace="AWS/Lambda",
            metric_name="ConcurrentExecutions",
            dimensions_map={
                "FunctionName": upload_lambda.function_name
            },
            statistic="Maximum",
            period=Duration.minutes(5),
            label="Concurrent Executions"
        )

        # API Gateway Metrics - Use API ID for REST APIs
        api_requests = cloudwatch.Metric(
            namespace="AWS/ApiGateway",
            metric_name="Count",
            dimensions_map={
                "ApiName": api_gateway.rest_api_name,
                "Stage": "prod"
            },
            statistic="Sum",
            period=Duration.minutes(5),
            label="API Requests"
        )

        api_4xx_errors = cloudwatch.Metric(
            namespace="AWS/ApiGateway",
            metric_name="4XXError",
            dimensions_map={
                "ApiName": api_gateway.rest_api_name,
                "Stage": "prod"
            },
            statistic="Sum",
            period=Duration.minutes(5),
            label="4XX Errors"
        )

        api_5xx_errors = cloudwatch.Metric(
            namespace="AWS/ApiGateway",
            metric_name="5XXError",
            dimensions_map={
                "ApiName": api_gateway.rest_api_name,
                "Stage": "prod"
            },
            statistic="Sum",
            period=Duration.minutes(5),
            label="5XX Errors"
        )

        api_latency = cloudwatch.Metric(
            namespace="AWS/ApiGateway",
            metric_name="Latency",
            dimensions_map={
                "ApiName": api_gateway.rest_api_name,
                "Stage": "prod"
            },
            statistic="Average",
            period=Duration.minutes(5),
            label="API Latency (ms)"
        )

        # Add widgets to dashboard
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Lambda Invocations",
                left=[lambda_invocations],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="Lambda Errors",
                left=[lambda_errors],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="Lambda Duration",
                left=[lambda_duration],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="Lambda Throttles",
                left=[lambda_throttles],
                width=12
            ),
            # Cold Start Metrics from Lambda Insights - Duration metrics
            cloudwatch.GraphWidget(
                title="Lambda Cold Starts - Init Duration (Average, Min, Max) [Lambda Insights]",
                left=[lambda_insights_init_duration, lambda_insights_init_duration_max, lambda_insights_init_duration_min],
                width=12,
                left_y_axis=cloudwatch.YAxisProps(
                    label="Duration (ms)",
                    show_units=False
                )
            ),
            # Cold Start Count from Lambda Insights
            cloudwatch.GraphWidget(
                title="Cold Start Count [Lambda Insights]",
                left=[lambda_insights_cold_start_count],
                width=12,
                left_y_axis=cloudwatch.YAxisProps(
                    label="Count",
                    show_units=False
                )
            ),
            cloudwatch.GraphWidget(
                title="Lambda Concurrent Executions",
                left=[lambda_concurrent],
                width=12
            ),
            # Total Lambda Invocations single value widget
            # Shows sum of invocations over the last 1 hour
            cloudwatch.SingleValueWidget(
                title="Total Lambda Invocations (Last 1 Hour)",
                metrics=[cloudwatch.Metric(
                    namespace="AWS/Lambda",
                    metric_name="Invocations",
                    dimensions_map={
                        "FunctionName": upload_lambda.function_name
                    },
                    statistic="Sum",
                    period=Duration.hours(1),  # Aggregates invocations over 1 hour period
                    label="Total Invocations"
                )],
                width=6
            ),
            cloudwatch.GraphWidget(
                title="API Gateway Requests",
                left=[api_requests],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="API Gateway 4XX Errors",
                left=[api_4xx_errors],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="API Gateway 5XX Errors",
                left=[api_5xx_errors],
                width=12
            ),
            cloudwatch.GraphWidget(
                title="API Gateway Latency",
                left=[api_latency],
                width=12
            ),
        )

        # Output dashboard URL
        dashboard_url = f"https://{self.region}.console.aws.amazon.com/cloudwatch/home?region={self.region}#dashboards:name={dashboard.dashboard_name}"
        
        CfnOutput(
            self, "DashboardURL",
            value=dashboard_url,
            description="CloudWatch Dashboard URL for monitoring"
        )
        
        self.dashboard_url = dashboard_url

