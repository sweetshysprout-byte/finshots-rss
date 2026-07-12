import feedparser
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import requests
from datetime import datetime

SOURCE_FEED = "https://finshots.in/archive/rss.xml"
OUTPUT_FILE = "finshots.xml"


def clean_html(html):
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(separator="\n").strip()


def fetch_article_image(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        meta = (
            soup.find("meta", property="og:image")
            or soup.find("meta", attrs={"name": "twitter:image"})
        )

        if meta:
            return meta.get("content")

    except Exception:
        pass

    return None


feed = feedparser.parse(SOURCE_FEED)

fg = FeedGenerator()
fg.title("Finshots")
fg.link(href="https://finshots.in")
fg.description("Automatically generated Finshots RSS feed")
fg.language("en")

for item in feed.entries:
    fe = fg.add_entry()

    fe.id(item.link)
    fe.title(item.title)
    fe.link(href=item.link)

    if hasattr(item, "published_parsed") and item.published_parsed:
        fe.pubDate(datetime(*item.published_parsed[:6]))

    summary = clean_html(getattr(item, "summary", ""))

    image = fetch_article_image(item.link)

    if image:
        html = f"""
        <p><img src="{image}"></p>
        <p>{summary}</p>
        """
    else:
        html = f"<p>{summary}</p>"

    fe.content(html, type="CDATA")
    fe.description(summary)

fg.rss_file(OUTPUT_FILE, pretty=True)

print("Generated", OUTPUT_FILE)
