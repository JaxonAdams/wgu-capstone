from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy
)
from constructs import Construct

class WguCapstoneStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for storing the ML model
        self.model_bucket = s3.Bucket(
            self, f"{self.stack_name}-ModelBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Upload the machine learning model to the bucket
        s3deploy.BucketDeployment(
            self, "DeployModel",
            sources=[s3deploy.Source.asset("data/models")],
            destination_bucket=self.model_bucket,
            destination_key_prefix="models",
        )
