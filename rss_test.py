import feedparser
from urllib.parse import quote_plus
from datetime import datetime, timezone

query = "Crystal Palace"

url = (
    "https://news.google.com/rss/search"
    f"?q={quote_plus(query)}"
    "&hl=en-GB"
    "&gl=GB"
    "&ceid=GB:en"
)

feed = feedparser.parse(url)

articles = sorted(
    feed.entries,
    key=lambda article: article.published_parsed or (0,),
    reverse=True
)

for article in articles:
    dt = datetime(*article.published_parsed[:6], tzinfo=timezone.utc)
    print(article.title, dt)