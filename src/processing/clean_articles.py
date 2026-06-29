import pandas as pd
import re


INPUT_PATH = "data/raw/automotive_news.csv"
OUTPUT_PATH = "data/processed/cleaned_automotive_news.csv"


EV_KEYWORDS = [
    "ev", "electric", "battery", "charging", "vehicle",
    "automotive", "car", "cars", "byd", "geely", "zeekr",
    "nio", "xpeng", "li auto", "xiaomi", "tesla"
]


def clean_text(text):
    if pd.isna(text):
        return ""

    text = re.sub(r"<.*?>", "", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_relevant_article(row):
    combined_text = f"{row['title']} {row['summary']}".lower()
    return any(keyword in combined_text for keyword in EV_KEYWORDS)


def process_articles():
    df = pd.read_csv(INPUT_PATH, encoding="latin1", on_bad_lines="skip")

    df["title"] = df["title"].apply(clean_text)
    df["summary"] = df["summary"].apply(clean_text)

    df = df.drop_duplicates(subset=["link"])
    df = df[df.apply(is_relevant_article, axis=1)]

    df.to_csv(OUTPUT_PATH, index=False)

    return df


if __name__ == "__main__":
    df = process_articles()

    print(f"Cleaned dataset saved to: {OUTPUT_PATH}")
    print(f"Remaining articles: {len(df)}")
    print(df[["source", "title", "published"]].head())