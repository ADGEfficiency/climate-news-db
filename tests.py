import pytest



@pytest.mark.parametrize(
    'url, expected',
    (
        ('https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live', True),

        ('https://www.theguardian.com/world/live/2020/may/27/uk-coronavirus-live-tory-revolt-continues-to-build-over-dominic-cummings-lockdown-trip', False),

        ('https://www.theguardian.com/world/2020/may/27/spanish-dig-closes-in-on-burial-site-of-irish-lord-red-hugh-odonnell', True),

        ('https://www.theguardian.com/environment/2020/may/05/one-billion-people-will-live-in-insufferable-heat-within-50-years-study', True),

        ('https://www.theguardian.com/environment/2019/may/18/climate-crisis-heat-is-on-global-heating-four-degrees-2100-change-way-we-live', True),

        ('https://www.theguardian.com/environment/live/2018/oct/08/ipcc-climate-change-report-urgent-action-fossil-fuels-live', False),

        ('https://www.theguardian.com/environment/2019/nov/14/coalition-inaction-on-climate-change-and-health-is-risking-australian-lives-global-report-finds', True)
    )
)
def test_guardian_check_url(url, expected):
    check = check_guardian_url(url, logger=None)
    assert expected == check

