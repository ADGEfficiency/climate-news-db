#!/usr/bin/env python3

import os

import aws_cdk as cdk
from stacks import Search

app = cdk.App()
Search(
    app,
    "ClimateNewsDB",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)
app.synth()
