import argparse

parser = argparse.ArgumentParser()
parser.add_argument("urls", metavar="N", type=str, nargs="+", help="urls to remove")
args = parser.parse_args()
urls = args.urls

print(urls)
for url in urls:
    pass

urls = ["https://www.bbc.co.uk/bitesize/guides/z432pv4/revision/1"]

"""
https://www.bbc.com/bitesize/guides/zt6sfg8/revision/2

https://www.bbc.com/bitesize/guides/zx234j6/revision/1
"""
