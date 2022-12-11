import typing

import boto3

region = "ap-southeast-2"
instances = ["i-0293ee8524464fefc"]


def scrape_controller(event: dict, context: typing.Union[dict, None] = None) -> None:
    """Starts up an EC2 instance"""
    ec2 = boto3.client("ec2", region_name=region)
    ec2.start_instances(InstanceIds=instances)
