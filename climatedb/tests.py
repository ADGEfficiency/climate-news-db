import pytest

from newspapers.nzherald import check_nzherald_url, get_nzherald_article_id
from newspapers.guardian import check_guardian_url
from newspapers.stuff import check_stuff_url
from newspapers.economist import check_economist_url


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live",
            True,
        ),
        (
            "https://www.theguardian.com/world/live/2020/may/27/uk-coronavirus-live-tory-revolt-continues-to-build-over-dominic-cummings-lockdown-trip",
            False,
        ),
        (
            "https://www.theguardian.com/world/2020/may/27/spanish-dig-closes-in-on-burial-site-of-irish-lord-red-hugh-odonnell",
            True,
        ),
        (
            "https://www.theguardian.com/environment/2020/may/05/one-billion-people-will-live-in-insufferable-heat-within-50-years-study",
            True,
        ),
        (
            "https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live",
            True,
        ),
        (
            "https://www.theguardian.com/environment/live/2018/oct/08/ipcc-climate-change-report-urgent-action-fossil-fuels-live",
            False,
        ),
        (
            "https://www.theguardian.com/environment/2019/nov/14/coalition-inaction-on-climate-change-and-health-is-risking-australian-lives-global-report-finds",
            True,
        ),
    ),
)
def test_guardian_check_url(url, expected):
    check = check_guardian_url(url, logger=None)
    assert expected == check


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://www.nzherald.co.nz/nz/news/video.cfm?c_id=1&gal_cid=1&gallery_id=214561",
            False,
        ),
        (
            "https://www.nzherald.co.nz/world/news/article.cfm?c_id=2&objectid=11558468",
            True,
        ),
        (
            "http://media.nzherald.co.nz/webcontent/document/pdf/201311/drought.pdf",
            False,
        ),
    ),
)
def test_check_nzherald_url(url, expected):
    check = check_nzherald_url(url, logger=None)
    assert expected == check


def test_nzherald_article_id():
    url, expected = (
        "https://www.nzherald.co.nz/the-country/news/article.cfm?c_id=16&objectid=12255029",
        12255029,
    )

    result = get_nzherald_article_id(url)
    assert str(expected) == result


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://www.stuff.co.nz/environment/climate-news/120171514/world-temperatures-on-the-rise--climate-change-report",
            True,
        ),
        ("https://www.stuff.co.nz/environment/climate-news/climate-explained", False),
        ("https://i.stuff.co.nz/environment/climate-news", False),
        ("https://interactives.stuff.co.nz/2019/07/407-and-rising/", False),
        (
            "https://events.stuff.co.nz/nelson-mail/2019/sustainable-backyards-climate-change-presentation/hastings",
            False,
        ),
    ),
)
def test_stuff_url_check(url, expected):
    check = check_stuff_url(url, logger=None)
    assert expected == check


@pytest.mark.parametrize(
    "url, expected",
    (
        ("https://www.economist.com/topics/climate-change", False),
        (
            "https://www.economist.com/schools-brief/2020/05/16/damage-from-climate-change-will-be-widespread-and-sometimes-surprising",
            True,
        ),
        (
            "https://www.economist.com/schools-brief/2020/04/23/why-tackling-global-warming-is-a-challenge-without-precedent",
            True,
        ),
        (
            "https://www.economist.com/1843/2018/10/29/worried-about-climate-change-hope-is-in-the-air",
            False,
        ),
    ),
)
def test_economist_url(url, expected):
    check = check_economist_url(url, logger=None)
    assert expected == check


def test_integration():
    from climatedb.collect_urls import main as collect

    collect(1, "all", "google", False)
