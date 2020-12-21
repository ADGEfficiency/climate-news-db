from datetime import datetime
import html.parser
import random

from climatedb.newspapers.guardian import check_guardian_url, parse_guardian_html
from climatedb.newspapers.fox import check_fox_url, parse_fox_html
from climatedb.newspapers.skyau import check_sky_au_url, parse_sky_au_url
from climatedb.newspapers.nytimes import check_nytimes_url, parse_nytimes_html

from climatedb.newspapers.cnn import cnn
from climatedb.newspapers.economist import economist
from climatedb.newspapers.newshub import newshub
from climatedb.newspapers.nzherald import nzherald
from climatedb.newspapers.stuff import stuff
from climatedb.newspapers.aljazeera import aljazeera
from climatedb.newspapers.atlantic import atlantic
from climatedb.newspapers.washington_post import washington_post
from climatedb.newspapers.dw import dw
from climatedb.newspapers.bbc import bbc
from climatedb.newspapers.independent import independent
#from climatedb.newspapers.the_times import the_times
from climatedb.newspapers.dailymail import dailymail


def find_newspaper_from_url(url):
    for paper in registry:
        if paper["newspaper_url"] in url:
            return paper


registry = [
    nzherald,
    stuff,
    newshub,
    economist,
    aljazeera,
    atlantic,
    washington_post,
    cnn,
    dw,
    bbc,
    independent,
    #the_times, paywall
    dailymail,
    {
        "newspaper_id": "guardian",
        "newspaper": "The Guardian",
        "newspaper_url": "theguardian.com",
        "checker": check_guardian_url,
        "parser": parse_guardian_html,
    },
    {
        "newspaper_id": "fox",
        "newspaper": "Fox News",
        "newspaper_url": "foxnews.com",
        "checker": check_fox_url,
        "parser": parse_fox_html,
    },
    {
        "newspaper_id": "nytimes",
        "newspaper": "The New York Times",
        "newspaper_url": "nytimes.com",
        "checker": check_nytimes_url,
        "parser": parse_nytimes_html,
    },
    {
        "newspaper_id": "skyau",
        "newspaper": "Sky News Australia",
        "newspaper_url": "skynews.com.au",
        "checker": check_sky_au_url,
        "parser": parse_sky_au_url,
    },
]


def get_newspaper(newspaper):
    for paper in registry:
        if paper["newspaper_id"] == newspaper:
            return paper
    raise ValueError(f"{newspaper} not in registry")


def check_parsed_article(parsed):
    if not parsed:
        return {}

    newspaper = get_newspaper(parsed["newspaper_id"])
    parsed["date_uploaded"] = datetime.utcnow().isoformat()
    parsed = {**parsed, **newspaper}

    del parsed["checker"]
    del parsed["parser"]

    schema = [
        "newspaper",
        "newspaper_id",
        "newspaper_url",
        "body",
        "headline",
        "html",
        "article_url",
        "article_id",
        "date_published",
        "date_uploaded",
    ]
    for sc in schema:
        #  check key exists
        if sc not in parsed.keys():
            raise ValueError(f"{sc} missing from parsed article")

        #  check value length
        val = parsed[sc]
        if len(val) < 2:
            url = parsed["article_url"]
            msg = f"{url} - {sc} not long enough - {val}"
            print(msg)
            import pdb; pdb.set_trace()
            raise ValueError(msg)

    return parsed


def clean_parsed_article(parsed):
    #  data cleaning - replacing escaped html characters
    html_parser = html.parser.HTMLParser()
    parsed["body"] = html_parser.unescape(parsed["body"])
    parsed["headline"] = html_parser.unescape(parsed["headline"])
    return parsed


def get_newspapers_from_registry(newspapers=None):
    if (newspapers == ("all",)) or (newspapers is None):
        papers = registry
    else:
        if isinstance(newspapers, str):
            newspapers = [newspapers, ]
        papers = [n for n in registry if n["newspaper_id"] in newspapers]
    random.shuffle(papers)
    return papers
