from newspapers.guardian import check_guardian_url, parse_guardian_html
from newspapers.fox import check_fox_url, parse_fox_html
from newspapers.skyau import check_sky_au_url, parse_sky_au_url
from newspapers.nytimes import check_nytimes_url, parse_nytimes_html


registry = [
    {
        "newspaper-id": "guardian",
        "newspaper": "The Guardian",
        "url": "theguardian.com",
        "checker": check_guardian_url,
        "parser": parse_guardian_html
    },
    {
        "newspaper-id": "fox",
        "newspaper": "Fox News",
        "url": "foxnews.com",
        "checker": check_fox_url,
        "parser": parse_fox_html
    },
    {
        "newspaper-id": "nytimes",
        "newspaper": "New York Times",
        "url": "nytimes.com",
        "checker": check_nytimes_url,
        "parser": parse_nytimes_html
    },
    {
        "newspaper-id": "skyau",
        "newspaper": "Sky News Australia",
        "url": "skynews.com.au",
        "checker": check_sky_au_url,
        "parser": parse_sky_au_url
    }
]
