from climatedb import files, types
from climatedb.config import data_home, s3_bucket, s3_prefix
from climatedb.databases import find_all_papers
from climatedb.search import search


def search_controller(
    event: dict, context: types.Union[dict, None] = None
) -> types.Dict[str, str]:
    """Search all newspapers for climate articles.

    Reads newspapers from the SQLite database.

    Writes urls to `urls.jsonl` on S3.
    """
    db = files.S3JSONLines(event["s3_bucket"], event["s3_key"])
    pkg = []
    papers = find_all_papers()

    for query in ["climate change", "climate crisis"]:
        for paper in papers:
            urls = search(paper, 5, query)
            db.write(urls)
            pkg.extend(urls)

    return pkg
