from aws_cdk import (CfnOutput, Duration, Stack, aws_events,
                     aws_events_targets, aws_iam, aws_lambda, aws_s3)
from constructs import Construct


class ClimatedbStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # IAM Role
        lambda_role = aws_iam.Role(
            self,
            "LambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "LambdaPolicy": aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=["s3:*"],
                            resources=["*"],
                        ),
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=["logs:*"],
                            resources=["arn:aws:logs:*:*:*"],
                        ),
                    ]
                ),
            },
        )

        # S3 Bucket
        bucket = aws_s3.Bucket(
            self,
            "Bucket",
            access_control=aws_s3.BucketAccessControl.PUBLIC_READ,
        )
        CfnOutput(
            self, "BucketNameOutput", value=bucket.bucket_name, export_name="BucketName"
        )

        # Lambda Functions
        search_function = aws_lambda.DockerImageFunction(
            self,
            "SearchLambda",
            code=aws_lambda.DockerImageCode.from_image_asset(
                directory="../",
                file="docker/search.Dockerfile",
                entrypoint=["/lambda-entrypoint.sh"],
                cmd=["climatedb.lambda.search_controller"],
                exclude=[".git", ".gitignore", ".vscode", "infra", "__pycache__"],
            ),
            role=lambda_role,
            timeout=Duration.seconds(900),
        )

        # EventBridge Rules
        aws_events.Rule(
            self,
            "SearchRule",
            schedule=aws_events.Schedule.cron(minute="0", hour="0"),
            targets=[
                aws_events_targets.LambdaFunction(
                    search_function,
                    event=aws_events.RuleTargetInput.from_object(
                        {
                            "s3_bucket": bucket.bucket_name,
                            "s3_key": "data/urls.jsonl",
                            "num": 5,
                        }
                    ),
                ),
            ],
        )
