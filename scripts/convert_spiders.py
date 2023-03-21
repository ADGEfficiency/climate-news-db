import os
import pathlib

import requests

from climatedb.gpt import CompletionRequest, Message

olds = pathlib.Path.home() / "cdb-main" / "climatedb" / "spiders"
olds = [p for p in olds.iterdir() if p.suffix == ".py"]

base = pathlib.Path.cwd() / "climatedb" / "spiders" / "china_daily.py"
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
                    content=f"Convert the given Python code to be the same as the base template.  Make sure to remove parsing_utils and clean_body.  Make sure you import scrapy and pathlib. Keep the xpath scraping logic for the article processing from the original article, but base the other logic on the base china daily spider. return an ArticleItem in the style of the base template. Don't create a meta dictionary, instead initialize the arguments for the ArticleItem class inline during the init. For the article_start_url use the function `article_start_url=find_start_url(response)`. Dont use any start_urls - remove it all like the china daily spider. Remove any unused imports. Remove any reference to description or subtitle. Remove any reference to `get_urls_for_paper`. Remove the `start_requests` function from the spider class. Use the typing from the base china daily class with the needed imports. Change the name to match the original spider. Remove the start_requests function from the spider class. If the given Python code includes the get_body function, use it. The spider should inherit from the base BaseSpider. The base template is ```\n{base}\n```",
                ),
                Message(
                    role="user", content=f"Code to convert ```python\n{old_code}\n```"
                ),
            ]
        )
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            json=request.dict(),
        )

        choices = response.json()["choices"]
        assert len(choices) == 1
        new_code = choices[0]["message"]["content"]
        new_code_fi.write_text(new_code)
        print(f"{new_code_fi} created")
        breakpoint()  # fmt: skip
    else:
        print(f"{new_code_fi} already exists")
