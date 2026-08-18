import pandas as pd

INPUT_PATH = "data/processed/classified_automotive_news.csv"

df = pd.read_csv(INPUT_PATH)


def summarize(text):
    if pd.isna(text):
        return ""

    words = str(text).split()

    return " ".join(words[:25]) + "..."


df["ai_summary"] = df["summary"].apply(summarize)

print(df[["title", "ai_summary"]].head())