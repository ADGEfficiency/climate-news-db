import json
import pathlib
import typing


class File:
    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        self.path = pathlib.Path(path).with_suffix(self.suffix)
        self.path.parent.mkdir(exist_ok=True, parents=True)

    def read(self):
        raise NotImplementedError()

    def write(self):
        raise NotImplementedError()

    def exists(self) -> bool:
        raise NotImplementedError()


class JSONLines(File):
    suffix = ".jsonl"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(JSONLines, self).__init__(path)

    def read(self) -> list[dict]:
        print(f" reading JSONLines from: {self.path}")
        data = self.path.read_text().split("\n")[:-1]
        return [json.loads(a) for a in data]

    def write(self, data: list[dict], mode: str = "w") -> None:
        print(f" writing JSONLines to: {self.path}")
        data = [json.dumps(d) + "\n" for d in data]

        if self.path.is_file():
            mode = "a"

        with open(self.path, mode) as fp:
            fp.writelines(data)

    def exists(self) -> bool:
        return self.path.is_file()


class HTMLFile(File):
    suffix = ".html"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(HTMLFile, self).__init__(path)

    def write(self, html: str) -> None:
        print(f" writing HTMLFile {self.path}")
        self.path.write_text(html)


class JSONFile(File):
    suffix = ".json"

    def __init__(self, path: typing.Union[str, pathlib.Path]) -> None:
        super(JSONFile, self).__init__(path)

    def read(self) -> typing.Union[dict, list]:
        return json.loads(self.path.read_text())
