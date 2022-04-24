from climatedb import types, files
from climatedb.config import data_home, s3_bucket, s3_prefix
from climatedb.databases import find_all_papers
from climatedb.search import search


def controller_handler(
    event: dict, context: types.Union[dict, None] = None
) -> types.Dict[str, str]:
    """Could use the search lambda here, or just the handler here"""

    bucket = event.get("s3_bucket", s3_bucket)
    key = event.get("s3_key", s3_prefix + "/urls.jsonl")
    urls_db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])

    #  TODO - create a daily stamp file as simple backup (maybe)
    pkg = []
    papers = find_all_papers()
    for np in papers:
        urls = search(np, 5)
        urls_db.write(urls)
        pkg.extend(urls)

    for np in papers:
        urls = search(np, 5, "climate crisis")
        urls_db.write(urls)
        pkg.extend(urls)

    return pkg
