import pytest

from newspapers.guardian import check_match


@pytest.mark.parametrize(
    'unwanted, url, expected',
    (
        (['live', 'gallery'],
        'https://www.theguardian.com/world/live/2020/may/27/uk-coronavirus-live-tory-revolt-continues-to-build-over-dominic-cummings-lockdown-trip',
        False),
        (['live', 'gallery'],
        'theguardian.com/world/2020/may/27/spanish-dig-closes-in-on-burial-site-of-irish-lord-red-hugh-odonnell',
        True),
    )
)
def test_remove_on_match(unwanted, url, expected):
    result = check_match(url, unwanted)
    assert result is expected


from newspapers.guardian import check_guardian_url


@pytest.mark.parametrize(
    'url, expected',
    (
        ('https://www.theguardian.com/environment/2020/may/05/one-billion-people-will-live-in-insufferable-heat-within-50-years-study', True),
        ('https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live', True)
    )
)
def test_guardian_check_url(url, expected):
    check = check_guardian_url(url)
    assert expected == check
