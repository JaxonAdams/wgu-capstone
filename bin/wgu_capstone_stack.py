from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
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

        CfnOutput(
            self, "ModelBucketName",
            value=model_bucket.bucket_name,
        )

        visualization_bucket = s3.Bucket(
            self, "VisualizationBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        s3deploy.BucketDeployment(
            self, "DeployVisualizations",
            sources=[s3deploy.Source.asset("data/visualizations")],
            destination_bucket=visualization_bucket,
            destination_key_prefix="visualizations"
        )
