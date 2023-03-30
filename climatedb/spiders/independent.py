import datetime

from scrapy.http.response.html import HtmlResponse

from climatedb import parse
from climatedb.crawl import create_article_name, find_start_url
from climatedb.models import ArticleItem
from climatedb.spiders.base import BaseSpider


class IndependentSpider(BaseSpider):
    name = "independent"

    def parse(self, response: HtmlResponse) -> ArticleItem:
        """
        @url https://www.independent.co.uk/climate-change/boris-johnson-g20-cop26-climate-b1948000.html
        @returns items 1
        @scrapes headline date_published body article_name article_url
        """
        ld_json = parse.get_ld_json(response, idx=1)

        body = response.xpath('//div[@class="text-wrapper"]/p/text()')
        body = " ".join(body.getall())

        unwanted = [
            "Please refresh the page or navigate to another page on the site to be automatically logged in Please refresh your browser to be logged in",
            " Registration is a free and easy way to support our truly independent journalism By registering, you will also enjoy limited access to Premium articles, exclusive newsletters, commenting, and virtual events with our leading journalists {{#verifyErrors}} {{message}} {{/verifyErrors}} {{^verifyErrors}} {{message}} {{/verifyErrors}} By clicking ‘Create my account’ you confirm that your data has been entered correctly and you have read and agree to our  Terms of use,   Cookie policy  and  Privacy notice. This site is protected by reCAPTCHA and the Google  Privacy policy  and  Terms of service  apply. Already have an account? sign in By clicking ‘Register’ you confirm that your data has been entered correctly and you have read and agree to our  Terms of use,   Cookie policy  and  Privacy notice. This site is protected by reCAPTCHA and the Google  Privacy policy  and  Terms of service  apply. Join thought-provoking conversations, follow other Independent readers and see their replies Want to bookmark your favourite articles and stories to read or reference later? Start your Independent Premium subscription today. Please refresh the page or navigate to another page on the site to be automatically logged in Please refresh your browser to be logged in Log in New to The Independent? Or if you would prefer: Want an ad-free experience? Hi {{indy.fullName}}",
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

        headline = ld_json["headline"]
        date_published = ld_json["datePublished"]
        date_published = datetime.datetime.strptime(
            date_published, "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        return ArticleItem(
            body=body,
            html=response.text,
            headline=headline,
            date_published=date_published,
            article_url=response.url,
            article_name=create_article_name(response.url, -1),
            article_start_url=find_start_url(response),
        )
