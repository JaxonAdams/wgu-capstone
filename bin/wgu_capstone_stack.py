from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_iam as iam,
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

        self.visualization_bucket = s3.Bucket(
            self, "VisualizationBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
                block_public_acls=False
            ),
        )

        # Attach a bucket policy to allow public read access
        self.visualization_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{self.visualization_bucket.bucket_arn}/*"],
                principals=[iam.ArnPrincipal("*")]
            )
        )

        # Deploy contents to a "visualizations" prefix in the bucket
        s3deploy.BucketDeployment(
            self, "DeployVisualizations",
            sources=[s3deploy.Source.asset("data/visualizations")],
            destination_bucket=self.visualization_bucket,
            destination_key_prefix="visualizations"
        )

        # Output the base URL for convenience
        CfnOutput(
            self, "VisualizationBaseUrl",
            value=f"https://{self.visualization_bucket.bucket_name}.s3.amazonaws.com/visualizations/"
        )
