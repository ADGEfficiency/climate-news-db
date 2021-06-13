from climatedb.newspapers.guardian import guardian

check_url = guardian['checker']
parse_url = guardian['parser']
get_article_id = guardian['get_article_id']


def test_guardian_good_urls():
    good_urls = (
        'https://www.theguardian.com/environment/2020/jun/17/climate-crisis-alarm-at-record-breaking-heatwave-in-siberia',
        'https://www.theguardian.com/commentisfree/2018/oct/30/climate-change-action-effective-ipcc-report-fossil-fuels',
        'https://www.theguardian.com/world/2020/dec/02/new-zealand-declares-a-climate-change-emergency'
    )
    for u in good_urls:
        assert check_url(u)


def test_guardian_bad_urls():
    bad_urls = (
        'https://www.theguardian.com/environment/live/2020/mar/03/the-frontline-experts-answer-your-questions-on-the-impacts-of-the-climate-emergency-live',
        'https://www.theguardian.com/environment/audio/2019/jan/21/what-can-we-do-right-now-about-climate-change',
        'https://www.theguardian.com/environment/gallery/2020/oct/08/fragile-planet-documenting-the-impact-of-the-climate-crisis-in-pictures'
        'https://www.theguardian.com/'
    )
    for u in bad_urls:
        assert not check_url(u)
