import boto3
from pathlib import Path

import json

from climatedb import types
from climatedb.config import region


class JSONLines:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        data = self.path.read_text().split("\n")[:-1]
        return [json.loads(a) for a in data]

    def write(self, data: types.List[dict], mode="w"):
        #  write data into a list of strings
        #  separated by new lines
        data = [json.dumps(d) + "\n" for d in data]

        if self.path.is_file():
            mode = "a"

        with open(self.path, mode) as fp:
            fp.writelines(data)


class S3JSONLines:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

        self.session = boto3.Session(region_name=region)
        self.resource = self.session.resource("s3")
        self.client = self.session.client("s3")
        self.obj = self.resource.Object(self.bucket, self.key)

        print(f"s3 jsonl: key: {self.key}, bucket: {self.bucket}")

    def read(self) -> types.List[dict]:
        obj = self.client.get_object(Bucket=self.bucket, Key=self.key)
        #  this will be a big string
        data = obj["Body"].read().decode("UTF-8")
        data = data.split("\n")[:-1]
        #  last one is empty string
        return [json.loads(d) for d in data]

    def write(self, data: types.List[dict], mode="w"):
        #  write data into a list of strings
        #  separated by new lines
        existing = self.read()

        print(f"joining {len(data)} urls onto {len(existing)} existing urls")
        existing = "".join([json.dumps(d) + "\n" for d in existing])
        data = "".join([json.dumps(d) + "\n" for d in data])

        pkg = existing + data
        self.obj.put(Body=bytes(pkg.encode("UTF-8")))


class JSONFile:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        return json.loads(self.path.read_text())
