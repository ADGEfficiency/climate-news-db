import pandas as pd
from aws_cdk import (CfnOutput, Duration, Stack, aws_events,
                     aws_events_targets, aws_iam, aws_lambda, aws_s3)
from aws_cdk.aws_ecr_assets import Platform
from constructs import Construct

from climatedb.utils import read_newspapers_json


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

        search_function = aws_lambda.Function(
            self,
            "SearchLambda",
            code=aws_lambda.EcrImageCode.from_asset_image(
                directory="../",
                file="docker/search.Dockerfile",
                entrypoint=["/lambda-entrypoint.sh"],
                cmd=["climatedb.lambda.search_controller"],
                exclude=[
                    ".git",
                    ".gitignore",
                    ".vscode",
                    "infra",
                    "__pycache__",
                    "data",
                    "data-neu",
                ],
                platform=Platform.LINUX_AMD64,
            ),
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            memory_size=128,
            timeout=Duration.seconds(900),
            role=lambda_role,
        )

        # EventBridge Rules
        #  lambda timeout is 15 min
        timeout = 15 + 1
        newspapers = read_newspapers_json("..")
        lambda_start_times = pd.date_range(
            "2021-01-01T00:00:00", freq=f"{timeout}T", periods=len(newspapers)
        )

        max_newspapers_per_day = 24 * 60 / timeout
        assert len(newspapers) < max_newspapers_per_day
        print(f"scheduling newspapers until {lambda_start_times[-1]}")

        for start_time, paper in zip(lambda_start_times, newspapers):
            print(f"scheduling {start_time} {paper.name}")
            aws_events.Rule(
                self,
                f"SearchRule-{paper.name}",
                schedule=aws_events.Schedule.cron(
                    minute=str(start_time.minute),
                    hour=str(start_time.hour),
                ),
                targets=[
                    aws_events_targets.LambdaFunction(
                        search_function,
                        event=aws_events.RuleTargetInput.from_object(
                            {
                                "s3_bucket": bucket.bucket_name,
                                "s3_key": "urls.jsonl",
                                "newspaper_name": paper.name,
                                "num": 5,
                            }
                        ),
                    ),
                ],
            )
