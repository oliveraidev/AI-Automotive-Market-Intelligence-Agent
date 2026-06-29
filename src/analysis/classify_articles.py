import pandas as pd


INPUT_PATH = "data/processed/cleaned_automotive_news.csv"
OUTPUT_PATH = "data/processed/classified_automotive_news.csv"


BRAND_KEYWORDS = {
    "BYD": ["byd"],
    "Geely": ["geely"],
    "Zeekr": ["zeekr"],
    "NIO": ["nio"],
    "XPeng": ["xpeng"],
    "Li Auto": ["li auto"],
    "Xiaomi Auto": ["xiaomi"],
    "Tesla": ["tesla"],
}


TOPIC_KEYWORDS = {
    "Battery": ["battery", "charging", "range", "lithium", "cell"],
    "Expansion": ["factory", "plant", "europe", "export", "global", "market", "launch"],
    "Autonomous Driving": ["autonomous", "self-driving", "adas", "driver assistance"],
    "Financial Results": ["sales", "revenue", "profit", "earnings", "deliveries"],
    "Regulation": ["tariff", "regulation", "policy", "subsidy", "government"],
    "Product Launch": ["new model", "launch", "unveil", "suv", "sedan"],
}


def classify_text(text, keyword_dict):
    text = str(text).lower()
    matches = []

    for label, keywords in keyword_dict.items():
        if any(keyword in text for keyword in keywords):
            matches.append(label)

    return ", ".join(matches) if matches else "Other"


def classify_articles():
    df = pd.read_csv(INPUT_PATH)

    df["combined_text"] = df["title"].fillna("") + " " + df["summary"].fillna("")

    df["brand"] = df["combined_text"].apply(lambda x: classify_text(x, BRAND_KEYWORDS))
    df["topic"] = df["combined_text"].apply(lambda x: classify_text(x, TOPIC_KEYWORDS))

    df = df.drop(columns=["combined_text"])

    df.to_csv(OUTPUT_PATH, index=False)

    return df


if __name__ == "__main__":
    df = classify_articles()

    print(f"Classified dataset saved to: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(df[["source", "title", "brand", "topic"]].head())