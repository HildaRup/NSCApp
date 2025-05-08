# app_complete.py
import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os

# Define RSS feeds for four newspapers
RSS_FEEDS = {
    'BBC': 'https://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'Reuters': 'http://feeds.reuters.com/reuters/topNews',
    'NYTimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

# Classification function
def classify_news(title, summary):
    keywords = {
        'Politics': ['politics', 'election', 'senate', 'congress', 'law'],
        'Celebrities/Arts/Culture': ['art', 'movie', 'celebrity', 'theatre', 'culture'],
        'Business': ['economy', 'business', 'stocks', 'market', 'trade'],
        'Sports': ['sports', 'game', 'tournament', 'match', 'Olympics']
    }
    text = (title + ' ' + summary).lower()
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category
    return 'Uncategorized'

# Fetch news from all feeds
def fetch_all_news():
    all_news = []
    for name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            summary = entry.get('summary', '')
            category = classify_news(title, summary)
            all_news.append({
                'source': name,
                'title': title,
                'link': link,
                'summary': summary,
                'category': category
            })
    return pd.DataFrame(all_news)

# Save to CSV
def save_to_csv(df, filename='news_data.csv'):
    df.to_csv(filename, index=False)

# Apply clustering
def cluster_news(df, n_clusters=4):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['summary'])
    model = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = model.fit_predict(X)
    return df

# Streamlit App
def main():
    st.title("Clustered News Stories Viewer")
    st.write("Assignment by Tinashe Zigara - R207669D")

    news_df = fetch_all_news()
    save_to_csv(news_df)

    clustered_df = cluster_news(news_df)

    st.sidebar.title("Cluster Explorer")
    cluster_id = st.sidebar.selectbox("Select Cluster", sorted(clustered_df['cluster'].unique()))
    cluster_data = clustered_df[clustered_df['cluster'] == cluster_id]

    st.write(f"### News Stories in Cluster {cluster_id}")
    for _, row in cluster_data.iterrows():
        st.markdown(f"{row['title']}**  \n{row['summary']}  \n[Read more]({row['link']})  \n_Category: {row['category']}_")
        st.markdown("---")

    with open('news_data.csv', 'rb') as file:
        st.download_button("Download CSV", file, file_name="news_data.csv")

if _name_ == '_main_':
    main()
