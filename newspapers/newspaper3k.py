"""
https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html

https://newspaper.readthedocs.io/en/latest/user_guide/advanced.html
"""

import newspaper

guardian = newspaper.build('http://theguardian.com', memoize_articles=False)

articles = guardian.articles

print(len(articles))
