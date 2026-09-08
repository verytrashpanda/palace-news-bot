import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# quick test for scraping headlines from cpfc.co.uk's news reel

NEWS_URL = "https://www.cpfc.co.uk/news/news/" #this is where the actual news reel is for some reason
BASE_URL = "https://www.cpfc.co.uk"

HEADERS = {
    "User-Agent": "Mozilla/5.0 PalaceNewsBot/1.0"
}


def get_cpfc_articles():
    response = requests.get(
        NEWS_URL,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = {}

    for link in soup.find_all("a", href=True):

        href = link["href"]

        if not href.startswith("/news/"):
            continue

        parts = href.strip("/").split("/")

        # we're looking for:
        # /news/category/article-name/
        if len(parts) < 3:
            continue

        url = urljoin(BASE_URL, href)

        # Prevent processing the same article multiple times
        if url in articles:
            continue

        title = link.get_text(" ", strip=True)

        if not title:
            continue

        # parts[0] is "news", parts[1] is the category segment,
        # e.g. /news/first-team/some-article-name/ -> "first-team"
        # the club already categorises stories which is massively helpful
        category = parts[1]
 
        articles[url] = {
            "title": title,
            "url": url,
            "category": category
        }
 
    return list(articles.values())
 
 
articles = get_cpfc_articles()
 
for article in articles:
    print(f"[{article['category']}] {article['title']}")
