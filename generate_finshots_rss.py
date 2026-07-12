import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

BASE = "https://finshots.in"
LATEST = "https://finshots.in/latest/"
OUTPUT = "finshots.xml"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(LATEST, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

fg = FeedGenerator()
fg.title("Finshots")
fg.link(href=BASE)
fg.description("Latest Finshots articles")
fg.language("en")

seen = set()

for a in soup.find_all("a", href=True):

    href = a["href"]

    if "/archive/" not in href:
        continue

    if href in seen:
        continue

    seen.add(href)

    title = a.get_text(" ", strip=True)

    if len(title) < 10:
        continue

    url = urljoin(BASE, href)

    try:
        article = requests.get(url, headers=headers, timeout=30)
        article.raise_for_status()

        art = BeautifulSoup(article.text, "html.parser")

        meta_desc = art.find("meta", attrs={"name": "description"})
        desc = meta_desc["content"] if meta_desc else ""

        og = art.find("meta", property="og:image")
        image = og["content"] if og else ""

        entry = fg.add_entry()

        entry.id(url)
        entry.title(title)
        entry.link(href=url)
        entry.description(desc)

        html = desc

        if image:
            html = f'<img src="{image}"><br><br>{desc}'

        entry.content(html, type="html")

    except Exception as e:
        print(e)

fg.rss_file(OUTPUT)

print("Done!")
