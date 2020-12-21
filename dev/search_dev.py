from climatedb.collect_urls import google_search, get_newspapers_from_registry


from climatedb.logger import make_logger

logger = make_logger()

papers = get_newspapers_from_registry(['washington_post', 'skyau'])
post = papers[1]
print(post)

# collection = []
# for idx in range(10):
#     urls = google_search(post['newspaper_url'], 'climate change', start=idx, stop=idx+1)
#     collection.extend(urls)
#     print(idx, len(collection))
#     print(urls)

from googlesearch.googlesearch import GoogleSearch
response = GoogleSearch().search("something")
for result in response.results:
    print("Title: " + result.title)
    print("Content: " + result.getText())
