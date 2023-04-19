from aws_cdk import (CfnOutput, Duration, Stack, aws_events,
                     aws_events_targets, aws_iam, aws_lambda, aws_s3)
from aws_cdk.aws_ecr_assets import Platform
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
        for hour, query in enumerate(["climate change", "climate crisis"]):
            aws_events.Rule(
                self,
                f"SearchRule-{query}",
                schedule=aws_events.Schedule.cron(
                    minute="0",
                    hour=str(hour),
                ),
                targets=[
                    aws_events_targets.LambdaFunction(
                        search_function,
                        event=aws_events.RuleTargetInput.from_object(
                            {
                                "s3_bucket": bucket.bucket_name,
                                "s3_key": "urls.jsonl",
                                "query": query,
                                "num": 5,
                            }
                        ),
                    ),
                ],
            )
