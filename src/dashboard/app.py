import pandas as pd
import streamlit as st
import plotly.express as px

from src.analysis.executive_summary import generate_summary

DATA_PATH = "data/processed/enriched_automotive_news.csv"

df = pd.read_csv(DATA_PATH)

st.set_page_config(
    page_title="AI Automotive Market Intelligence",
    layout="wide"
)

st.title("AI Automotive Market Intelligence Dashboard")
st.caption("Market intelligence dashboard for Chinese EV and automotive news.")

# =========================
# Sidebar filters
# =========================

st.sidebar.header("Filters")

brands = sorted(df["primary_brand"].dropna().unique())
topics = sorted(df["primary_topic"].dropna().unique())
sentiments = sorted(df["sentiment"].dropna().unique())

selected_brands = st.sidebar.multiselect(
    "Brand",
    brands,
    default=brands
)

selected_topics = st.sidebar.multiselect(
    "Topic",
    topics,
    default=topics
)

selected_sentiments = st.sidebar.multiselect(
    "Sentiment",
    sentiments,
    default=sentiments
)

search_query = st.sidebar.text_input("Search articles")

filtered_df = df[
    df["primary_brand"].isin(selected_brands)
    & df["primary_topic"].isin(selected_topics)
    & df["sentiment"].isin(selected_sentiments)
]

if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            search_query,
            case=False,
            na=False
        )
        | filtered_df["summary"].str.contains(
            search_query,
            case=False,
            na=False
        )
    ]

# =========================
# Executive Summary
# =========================

st.subheader("Market Intelligence Brief")

with st.container(border=True):
    st.markdown(generate_summary(filtered_df))

st.divider()

# =========================
# KPI Cards
# =========================

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "Total Articles",
    len(filtered_df)
)

col2.metric(
    "Brands",
    filtered_df["primary_brand"].nunique()
)

col3.metric(
    "Topics",
    filtered_df["primary_topic"].nunique()
)

top_brand = (
    filtered_df["primary_brand"]
    .value_counts()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)

col4.metric(
    "Top Brand",
    top_brand
)

positive_share = (
    round(
        (
            filtered_df["sentiment"] == "Positive"
        ).mean() * 100,
        1
    )
    if not filtered_df.empty
    else 0
)

col5.metric(
    "Positive Share",
    f"{positive_share}%"
)

average_sentiment = (
    round(
        filtered_df["sentiment_score"].mean(),
        3
    )
    if not filtered_df.empty
    else 0
)

col6.metric(
    "Avg. Sentiment",
    average_sentiment
)

st.divider()

# =========================
# Brand and Topic Charts
# =========================

left, right = st.columns(2)

with left:
    st.subheader("Articles by Brand")

    brand_counts = (
        filtered_df["primary_brand"]
        .value_counts()
        .reset_index()
    )

    brand_counts.columns = [
        "Brand",
        "Articles"
    ]

    fig_brand = px.bar(
        brand_counts,
        x="Brand",
        y="Articles",
        text="Articles",
        title="Brand Coverage"
    )

    fig_brand.update_layout(
        xaxis_title="Brand",
        yaxis_title="Articles"
    )

    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )

with right:
    st.subheader("Articles by Topic")

    topic_counts = (
        filtered_df["primary_topic"]
        .value_counts()
        .reset_index()
    )

    topic_counts.columns = [
        "Topic",
        "Articles"
    ]

    fig_topic = px.bar(
        topic_counts,
        x="Topic",
        y="Articles",
        text="Articles",
        title="Topic Coverage"
    )

    fig_topic.update_layout(
        xaxis_title="Topic",
        yaxis_title="Articles"
    )

    st.plotly_chart(
        fig_topic,
        use_container_width=True
    )

st.divider()

# =========================
# Sentiment Analysis
# =========================

st.subheader("Sentiment Analysis")

sentiment_left, sentiment_right = st.columns(2)

with sentiment_left:

    sentiment_counts = (
        filtered_df["sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Articles"
    ]

    fig_sentiment = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Articles",
        text="Articles",
        title="Overall Sentiment Distribution"
    )

    fig_sentiment.update_layout(
        xaxis_title="Sentiment",
        yaxis_title="Articles"
    )

    st.plotly_chart(
        fig_sentiment,
        use_container_width=True
    )

with sentiment_right:

    sentiment_by_brand = (
        filtered_df
        .groupby(
            ["primary_brand", "sentiment"]
        )
        .size()
        .reset_index(
            name="Articles"
        )
    )

    fig_brand_sentiment = px.bar(
        sentiment_by_brand,
        x="primary_brand",
        y="Articles",
        color="sentiment",
        barmode="group",
        title="Sentiment by Brand"
    )

    fig_brand_sentiment.update_layout(
        xaxis_title="Brand",
        yaxis_title="Articles",
        legend_title="Sentiment"
    )

    st.plotly_chart(
        fig_brand_sentiment,
        use_container_width=True
    )

st.divider()

# =========================
# Top Market Headlines
# =========================

st.subheader("Top Market Headlines")

if filtered_df.empty:

    st.info(
        "No articles match the selected filters."
    )

else:

    for _, row in filtered_df.head(8).iterrows():

        st.markdown(
            f"""
**{row['title']}**

`{row['primary_brand']}` ·
`{row['primary_topic']}` ·
`{row['sentiment']}` ·
{row['source']}

[Read article]({row['link']})
"""
        )

st.divider()

# =========================
# Article Database
# =========================

st.subheader("Article Database")

st.dataframe(
    filtered_df[
        [
            "source",
            "title",
            "primary_brand",
            "primary_topic",
            "sentiment",
            "sentiment_score",
            "published",
            "link",
        ]
    ],
    use_container_width=True,
)