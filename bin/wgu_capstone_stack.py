from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as lambda_alpha,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as integrations,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct


class WguCapstoneStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        model_bucket = s3.Bucket(
            self, "ModelBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        s3deploy.BucketDeployment(
            self, "DeployModel",
            sources=[s3deploy.Source.asset("data/models")],
            destination_bucket=model_bucket,
            destination_key_prefix="models",
        )

        # Lambda function for model prediction
        lambda_fn = _lambda.DockerImageFunction(
            self, "PredictLambda",
            function_name=f"{self.stack_name}-PredictLambda",
            code=_lambda.DockerImageCode.from_image_asset("src/lambda"),
            timeout=Duration.seconds(120),
            memory_size=2048,
            environment={
                "MODEL_BUCKET_NAME": model_bucket.bucket_name,
                "MODEL_KEY": "models/rf.pkl"
            }
        )


        model_bucket.grant_read(lambda_fn)

        http_api = apigwv2.HttpApi(self, "PredictAPI", create_default_stage=True)

        http_integration = integrations.HttpLambdaIntegration(
            "PredictIntegration", handler=lambda_fn
        )

        http_api.add_routes(
            path="/predict",
            methods=[apigwv2.HttpMethod.POST],
            integration=http_integration
        )

        self.api_endpoint = http_api.url

        CfnOutput(
            self, "HttpApiUrl",
            value=self.api_endpoint,
        )
