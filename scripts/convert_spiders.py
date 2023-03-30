import os
import pathlib

import requests

from climatedb.gpt import CompletionRequest, Message

olds = pathlib.Path.home() / "cdb-main" / "climatedb" / "spiders"
olds = [p for p in olds.iterdir() if p.suffix == ".py" if "washingtion" not in str(p)]

base = pathlib.Path.cwd() / "climatedb" / "spiders" / "skyau.py"
base = base.read_text()
for fi in olds:
    old_code = fi.read_text()
    new_code_fi = pathlib.Path.cwd() / "climatedb" / "spiders" / fi.name

    if not new_code_fi.exists():
        print(f"{new_code_fi} not exists")
        request = CompletionRequest(
            messages=[
                Message(
                    role="system",
                    content=f"I am converting scrapy Spiders written in Python from the old style to a new style.  The new style is given as the ChinaDailySpider:\n```\n{base}\n```.  Below you will be given a spider to convert to the new style - this is the OLD spider.  You should convert the spider to the new style as defined by ChinaDailySpider.  You should remove parsing_utils and clean_body.  You should import scrapy.  Base the xpath scraping logic on the OLD spider, but any other logic or code style on the ChinaDailySpider.  Return an ArticleItem is the style of the ChinaDailySpider. For the article_start_url use the function `article_start_url=find_start_url(response)`. Dont use any start_urls - remove it all like the china daily spider. Remove any unused imports. Remove any reference to description or subtitle. Remove any reference to `get_urls_for_paper`. Remove the `start_requests` function from the spider class. Use the typing from the base china daily class with the needed imports. Change the name to match the original spider. Remove the start_requests function from the spider class. If the given Python code includes the get_body function, use it. The spider should inherit from the base BaseSpider.  The parse function should be called `parse`. Return an ArticleItem with everything inline - do not create a meta dictionary for use in the ArticleItem init.",
                ),
                Message(
                    role="user", content=f"OLD spider code:\n```python\n{old_code}\n```"
                ),
            ]
        )
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            json=request.dict(exclude={"request_time_utc": True}),
        )
        assert response.ok, response.json()

        choices = response.json()["choices"]
        assert len(choices) == 1
        new_code = choices[0]["message"]["content"]
        new_code_fi.write_text(new_code)
        print(f"{new_code_fi} created")
        breakpoint()  # fmt: skip
    else:
        print(f"{new_code_fi} already exists")
