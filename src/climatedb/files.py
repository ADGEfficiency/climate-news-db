import datetime
import json
import pathlib
import typing

import boto3
from rich import print
from scrapy.settings import Settings


class JSONEncoder(json.JSONEncoder):
    """seralize non-JSON compatabile data to JSON - numpy + timestamps"""

    def default(self, obj: typing.Any) -> typing.Any:
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        else:
            return super(JSONEncoder, self).default(obj)


class File:
    suffix = ""

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        self.path = pathlib.Path(path).with_suffix(self.suffix)
        self.path.parent.mkdir(exist_ok=True, parents=True)

    def read(self) -> typing.Union[list, str, dict]:
        raise NotImplementedError()

    def write(self, data: typing.Union[dict, list, str]) -> None:
        raise NotImplementedError()

    def exists(self) -> bool:
        raise NotImplementedError()


class JSONLines(File):
    suffix = ".jsonl"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(JSONLines, self).__init__(path)

    def read(self) -> list:
        print(f" reading JSONLines from: {self.path}")
        data = self.path.read_text().split("\n")[:-1]
        return [json.loads(a) for a in data]

    def write(self, data: list, mode: str = "w") -> None:  # type: ignore[override]
        print(f" writing JSONLines to: {self.path}")

        if self.path.is_file():
            mode = "a"

        with open(self.path, mode) as fp:
            fp.writelines([json.dumps(d, cls=JSONEncoder) + "\n" for d in data])

    def exists(self) -> bool:
        return self.path.is_file()


class HTMLFile(File):
    suffix = ".html"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(HTMLFile, self).__init__(path)

    def write(self, data: str) -> None:  # type: ignore[override]
        print(f" writing HTMLFile {self.path}")
        self.path.write_text(data)


class JSONFile(File):
    suffix = ".json"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(JSONFile, self).__init__(path)

    def read(self) -> typing.Any:
        print(f" read JSONFile {self.path.name}")
        return json.loads(self.path.read_text())

    def write(self, data: dict) -> None:
        print(f" write JSONFile {self.path.name}")
        self.path.write_text(json.dumps(data, cls=JSONEncoder))

    def exists(self) -> bool:
        return self.path.is_file()


class S3JSONLines:
    def __init__(self, bucket: str, key: str) -> None:
        settings = Settings()
        settings.setmodule("climatedb.settings")

        self.bucket = bucket
        self.key = key

        self.session = boto3.Session(region_name=settings["AWS_REGION"])
        self.resource = self.session.resource("s3")
        self.client = self.session.client("s3")
        self.obj = self.resource.Object(self.bucket, self.key)

    def read(self) -> list[dict]:
        print(f" reading JSONLines from s3: {self.bucket, self.key}")
        obj = self.client.get_object(Bucket=self.bucket, Key=self.key)
        #  this will be a big string
        data = obj["Body"].read().decode("UTF-8")
        data = data.split("\n")[:-1]
        #  last one is empty string
        return [json.loads(d) for d in data]

    def write(self, data: list, mode: str = "w") -> None:
        print(f" writing JSONLines to s3: {self.bucket, self.key}")
        #  write data into a list of strings
        #  separated by new lines
        existing = self.read()

        #  can actually use the jsonlines package here probably...
        print(f" joining {len(data)} urls onto {len(existing)} existing urls")
        #  TODO - messy
        pkg = "".join([json.dumps(d) + "\n" for d in existing]) + "".join(
            [json.dumps(d) + "\n" for d in data]
        )
        self.obj.put(Body=bytes(pkg.encode("UTF-8")))
