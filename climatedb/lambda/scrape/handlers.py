import time
import typing

import boto3
from rich import print

region = "ap-southeast-2"
instances = ["i-0293ee8524464fefc"]


def start_instance(instances, region):
    ec2 = boto3.client("ec2", region_name=region)
    ec2.start_instances(InstanceIds=instances)


def run_ssm_command(instances, region):
    """
    requires `sudo snap start amazon-ssm-agent` on the ec2 instance

    also attaching IAM permissions to the ec2 instance

    """
    ssm = boto3.client("ssm", region_name=region)
    info = ssm.describe_instance_information()
    assert info["InstanceInformationList"], info
    return ssm.send_command(
        InstanceIds=instances,
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [
                "bash -c 'sh /home/ubuntu/.bashrc && cd /home/ubuntu/climate-news-db && make scrape -o setup && sudo shutdown'"
            ]
        },
        TimeoutSeconds=24 * 60 * 60,
    )


def scrape_controller(
    event: dict, context: typing.Union[dict, None] = None
) -> typing.Dict[str, str]:
    """Starts up an EC2 instance, runs scraping."""
    start_instance(instances, region)
    time.sleep(60)
    run_ssm_command(instances, region)


if __name__ == "__main__":
    #  just for development
    ssm = boto3.client("ssm", region_name=region)
    response = run_ssm_command(instances, region)
    command_id = response["Command"]["CommandId"]
    success = False
    while not success:
        time.sleep(2)
        output = ssm.get_command_invocation(
            CommandId=command_id, InstanceId=instances[0]
        )

        if output["Status"] == "InProgress":
            print("in-progress - trying again")

        else:
            print(output["Status"])
            print(output)
            print("")
            break
