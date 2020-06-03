import pytest

from guardian import check_match


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
