import pandas as pd

INPUT_PATH = "data/processed/classified_automotive_news.csv"


def generate_summary(df):
    if df.empty:
        return "No market data is available for the selected filters."

    total_articles = len(df)

    brand_counts = df["primary_brand"].value_counts()
    top_brand = brand_counts.idxmax()
    top_brand_count = int(brand_counts.max())
    top_brand_share = top_brand_count / total_articles * 100

    topic_counts = df["primary_topic"].value_counts()
    top_topic = topic_counts.idxmax()
    top_topic_count = int(topic_counts.max())
    top_topic_share = top_topic_count / total_articles * 100

    latest_article = df.iloc[0]["title"]

    return f"""
### Market Intelligence Brief

- **{total_articles}** automotive news articles were analysed.
- **{top_brand}** received the most media attention with **{top_brand_count} articles** ({top_brand_share:.1f}% of coverage).
- The most frequently detected topic was **{top_topic}**, with **{top_topic_count} articles** ({top_topic_share:.1f}%).
- **Latest headline:** {latest_article}
""".strip()


if __name__ == "__main__":
    dataframe = pd.read_csv(INPUT_PATH)
    print(generate_summary(dataframe))