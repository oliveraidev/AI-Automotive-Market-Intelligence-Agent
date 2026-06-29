import feedparser
import pandas as pd
from datetime import datetime


RSS_FEEDS = {
    "Electrive": "https://www.electrive.com/feed/",
    "InsideEVs": "https://insideevs.com/rss/news/all/",
    "CleanTechnica": "https://cleantechnica.com/feed/",
}


def collect_news():
    articles = []

    for source, feed_url in RSS_FEEDS.items():
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            articles.append({
                "source": source,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    return pd.DataFrame(articles)


if __name__ == "__main__":
    df = collect_news()
    df.to_csv("data/raw/automotive_news.csv", index=False)

    print(f"Collected {len(df)} articles.")
    print(df.head())