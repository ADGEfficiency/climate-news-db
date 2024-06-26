import pandas as pd
from aws_cdk import (CfnOutput, Duration, Stack, aws_events,
                     aws_events_targets, aws_iam, aws_lambda, aws_s3)
from aws_cdk.aws_ecr_assets import Platform
from constructs import Construct

from climatedb.models import SearchLambdaEvent
from climatedb.utils import read_newspapers_json


class Search(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs: dict) -> None:
        super().__init__(scope, id, **kwargs)

        unversioned_bucket = aws_s3.Bucket(self, "Unversioned")
        CfnOutput(self, "UnversionedBucket", value=unversioned_bucket.bucket_name, export_name="UnversionedBucket")

        versioned_bucket = aws_s3.Bucket(
            self,
            "Versioned",
            versioned=True,
            lifecycle_rules=[aws_s3.LifecycleRule(noncurrent_version_expiration=Duration.days(30))]
        )
        CfnOutput(self, "VersionedBucket", value=versioned_bucket.bucket_name, export_name="VersionedBucket")

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
            memory_size=256,
            timeout=Duration.seconds(900),
            role=lambda_role,
        )

        #  lambda timeout is 15 min, so run every 16 minutes
        timeout = 15 + 1
        newspapers = read_newspapers_json("..")
        lambda_start_times = pd.date_range(
            "2021-01-01T00:00:00", freq=f"{timeout}T", periods=len(newspapers)
        )
        max_newspapers_per_day = 24 * 60 / timeout
        assert len(newspapers) < max_newspapers_per_day
        print(f"scheduling newspapers until {lambda_start_times[-1]}")
        for start_time, newspaper in zip(lambda_start_times, newspapers):
            print(f"scheduling {start_time} {newspaper.name}")
            aws_events.Rule(
                self,
                f"SearchRule-{newspaper.name}",
                schedule=aws_events.Schedule.cron(
                    minute=str(start_time.minute),
                    hour=str(start_time.hour),
                    month="*",
                    week_day="1",
                ),
                targets=[
                    aws_events_targets.LambdaFunction(
                        search_function,
                        event=aws_events.RuleTargetInput.from_object(
                            SearchLambdaEvent(
                                s3_bucket=versioned_bucket.bucket_name,
                                newspaper_name=newspaper.name,
                            ).dict()
                        ),
                    ),
                ],
            )
