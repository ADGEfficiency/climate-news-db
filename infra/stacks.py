import pandas as pd
from aws_cdk import CfnOutput, Duration, Stack
from aws_cdk.aws_ecs import LogDriver, AwsLogDriver, AwsLogDriverProps
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_events
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets, aws_iam, aws_lambda, aws_s3
from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform
from aws_cdk.aws_ecs import Cluster, ContainerImage, FargateTaskDefinition
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import EcsTask
from constructs import Construct

from climatedb.models import SearchLambdaEvent
from climatedb.utils import read_newspapers_json


class Search(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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

        bucket = aws_s3.Bucket(self, "BucketName")
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
                ),
                targets=[
                    aws_events_targets.LambdaFunction(
                        search_function,
                        event=aws_events.RuleTargetInput.from_object(
                            SearchLambdaEvent(
                                s3_bucket=bucket.bucket_name,
                                newspaper_name=newspaper.name,
                            ).dict()
                        ),
                    ),
                ],
            )


class Crawl(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = Cluster(self, "EcsCluster")

        docker_image = DockerImageAsset(
            self,
            "DockerImage",
            directory="../",
            file="docker/search.Dockerfile",
            build_args={
                "ENTRYPOINT": "/lambda-entrypoint.sh",
                "CMD": "climatedb.lambda.search_controller",
            },
            exclude=[
                ".git",
                ".gitignore",
                ".vscode",
                "infra",
                "__pycache__",
                "data",
            ],
        )

        task_definition = FargateTaskDefinition(self, "TaskDefinition")

        container = task_definition.add_container(
            "Container",
            image=ContainerImage.from_docker_image_asset(docker_image),
            logging=LogDriver.aws_logs(stream_prefix="climate-news-db-scrape")
        )

        rule = Rule(self, "WeeklyRule", schedule=Schedule.rate(Duration.days(7)))
        rule.add_target(EcsTask(cluster=cluster, task_definition=task_definition))
