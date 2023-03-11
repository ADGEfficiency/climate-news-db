from climatedb import Article, get_urls_for_paper, parsing_utils
from climatedb.spiders.base import ClimateDBSpider


class IndependentSpider(ClimateDBSpider):
    name = "independent"
    start_urls = get_urls_for_paper(name)

    def parse(self, response):
        article_name = parsing_utils.form_article_id(response.url, -1)
        body = parsing_utils.get_body(response)

        unwanted = [
            "Please refresh the page or navigate to another page on the site to be automatically logged in Please refresh your browser to be logged in",
            " Registration is a free and easy way to support our truly independent journalism By registering, you will also enjoy limited access to Premium articles, exclusive newsletters, commenting, and virtual events with our leading journalists {{#verifyErrors}} {{message}} {{/verifyErrors}} {{^verifyErrors}} {{message}} {{/verifyErrors}} By clicking ‘Create my account’ you confirm that your data has been entered correctly and you have read and agree to our  Terms of use,   Cookie policy  and  Privacy notice. This site is protected by reCAPTCHA and the Google  Privacy policy  and  Terms of service  apply. Already have an account? sign in By clicking ‘Register’ you confirm that your data has been entered correctly and you have read and agree to our  Terms of use,   Cookie policy  and  Privacy notice. This site is protected by reCAPTCHA and the Google  Privacy policy  and  Terms of service  apply. Join thought-provoking conversations, follow other Independent readers and see their replies Want to bookmark your favourite articles and stories to read or reference later? Start your Independent Premium subscription today. Please refresh the page or navigate to another page on the site to be automatically logged in Please refresh your browser to be logged in Log in New to The Independent? Or if you would prefer: Want an ad-free experience? Hi {{indy.fullName}}",
        ]
        for unw in unwanted:
            body = body.replace(unw, "")

        headline = response.xpath('//meta[@property="og:title"]/@content').get()
        headline = headline.split("|")[0]
        subtitle = response.xpath('//meta[@property="og:description"]/@content').get()

        app_json = parsing_utils.get_app_json(response, n=1)
        date = app_json["datePublished"]

        meta = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body,
            "article_url": response.url,
            "date_published": date,
            "article_name": article_name,
        }
        meta = Article(**meta).dict()
        return self.tail(response, meta)
