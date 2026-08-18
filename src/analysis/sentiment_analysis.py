import pandas as pd
from textblob import TextBlob


INPUT_PATH = "data/processed/classified_automotive_news.csv"
OUTPUT_PATH = "data/processed/enriched_automotive_news.csv"


def get_sentiment_score(text):
    text = str(text)

    if not text.strip():
        return 0.0

    return TextBlob(text).sentiment.polarity


def get_sentiment_label(score):
    if score > 0.1:
        return "Positive"

    if score < -0.1:
        return "Negative"

    return "Neutral"


def analyse_sentiment():
    df = pd.read_csv(INPUT_PATH)

    df["combined_text"] = (
        df["title"].fillna("") + " " + df["summary"].fillna("")
    )

    df["sentiment_score"] = df["combined_text"].apply(
        get_sentiment_score
    )

    df["sentiment"] = df["sentiment_score"].apply(
        get_sentiment_label
    )

    df = df.drop(columns=["combined_text"])

    df.to_csv(OUTPUT_PATH, index=False)

    return df


if __name__ == "__main__":
    sentiment_df = analyse_sentiment()

    print(f"Enriched dataset saved to: {OUTPUT_PATH}")
    print("\nSentiment distribution:")
    print(sentiment_df["sentiment"].value_counts())

    print("\nAverage sentiment score:")
    print(round(sentiment_df["sentiment_score"].mean(), 3))

    print("\nPreview:")
    print(
        sentiment_df[
            [
                "title",
                "primary_brand",
                "primary_topic",
                "sentiment",
                "sentiment_score",
            ]
        ].head()
    )