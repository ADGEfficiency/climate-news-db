from climatedb.files import JSONLines

fi = JSONLines("./data-neu/articles/washington_post.jsonlines.old")

data = fi.read()

neu_data = []
for item in data:
    headline = item["headline"]
    headline = headline.split("|")[-1]
    item["headline"] = headline

    body = item["body"]
    body = body.replace("This article was published more than  1 year ago ", "")
    item["body"] = body
    neu_data.append(item)

for item in neu_data:
    assert "|" not in item["headline"]
fi = JSONLines("./data-neu/articles/washington_post.jsonlines")
fi.write(data)
