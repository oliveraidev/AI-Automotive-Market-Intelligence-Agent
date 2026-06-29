import feedparser
import pandas as pd
import requests
from datetime import datetime


RSS_FEEDS = {
    "BYD News": "https://news.google.com/rss/search?q=BYD%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "Geely News": "https://news.google.com/rss/search?q=Geely%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "Zeekr News": "https://news.google.com/rss/search?q=Zeekr%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "NIO News": "https://news.google.com/rss/search?q=NIO%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "XPeng News": "https://news.google.com/rss/search?q=XPeng%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "Li Auto News": "https://news.google.com/rss/search?q=Li%20Auto%20electric%20vehicle&hl=en-US&gl=US&ceid=US:en",
    "Xiaomi Auto News": "https://news.google.com/rss/search?q=Xiaomi%20EV&hl=en-US&gl=US&ceid=US:en",
}


def fetch_feed(feed_url):
    response = requests.get(
        feed_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
        verify=False,
    )
    response.raise_for_status()
    return feedparser.parse(response.content)


def collect_news():
    articles = []

    for source, feed_url in RSS_FEEDS.items():
        try:
            feed = fetch_feed(feed_url)
            print(source, len(feed.entries))

            for entry in feed.entries:
                articles.append({
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })

        except Exception as error:
            print(f"Error collecting {source}: {error}")

    return pd.DataFrame(articles)


if __name__ == "__main__":
    df = collect_news()

    if df.empty:
        print("No articles collected. Existing CSV was not overwritten.")
    else:
        df.to_csv("data/raw/automotive_news.csv", index=False)
        print(f"Collected {len(df)} articles.")
        print(df.head())