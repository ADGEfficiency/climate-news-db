import datetime
import json
import pathlib
import typing


class JSONEncoder(json.JSONEncoder):
    """seralize non-JSON compatabile data to JSON - numpy + timestamps"""

    def default(self, obj):
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

    def write(self, data: typing.Union[list, str], mode: str) -> None:
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
        return json.loads(self.path.read_text())
