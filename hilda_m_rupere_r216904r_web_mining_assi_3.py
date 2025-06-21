import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# === UI Text ===
APP_TITLE = "🗞️ News Article Clusters"
SIDEBAR_TITLE = "🧭 Cluster Navigator"
DOWNLOAD_LABEL = "⬇️ Export News as CSV"

# === RSS Feeds ===
RSS_FEEDS = {
    'BBC': 'https://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'Reuters': 'http://feeds.reuters.com/reuters/topNews',
    'NYTimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

# === Categorization by Keywords ===
def classify_news(title, summary):
    keywords = {
        'Politics': ['politics', 'election', 'senate', 'congress', 'law'],
        'Celebrities/Arts/Culture': ['art', 'movie', 'celebrity', 'theatre', 'culture'],
        'Business': ['economy', 'business', 'stocks', 'market', 'trade'],
        'Sports': ['sports', 'game', 'tournament', 'match', 'olympics']
    }
    text = (title + ' ' + summary).lower()
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category
    return 'Uncategorized'

# === Fetching News ===
def fetch_news():
    all_articles = []
    for name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            summary = entry.get('summary', '') or entry.get('description', '')
            category = classify_news(title, summary)
            all_articles.append({
                'source': name,
                'title': title,
                'link': link,
                'summary': summary,
                'category': category
            })
    return pd.DataFrame(all_articles)

# === Save to CSV ===
def save_to_csv(df):
    df.to_csv("news_data.csv", index=False)

# === Clustering ===
def cluster_news(df, n_clusters=4):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    df['summary'] = df['summary'].fillna('')
    X = vectorizer.fit_transform(df['summary'])
    model = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = model.fit_predict(X)
    return df

# === UI: Cluster Display ===
def display_clusters(df):
    grouped = df.groupby('cluster')

    for cluster_id, group in grouped:
        st.markdown(f"### Cluster {cluster_id} ({len(group)} articles)")
        st.markdown("<ul>", unsafe_allow_html=True)
        for _, row in group.iterrows():
            st.markdown(f"<li><a href='{row['link']}' target='_blank'>{row['title']}</a></li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("---")

# === Main App ===
def main():
    st.set_page_config(page_title="News Clustering App", layout="wide")
    st.title(APP_TITLE)
    st.caption("Developed by Hilda Rupere r216904r — Web Content Mining Assignment 3")

    with st.spinner("⏳ Fetching latest headlines..."):
        df = fetch_news()
        save_to_csv(df)
        df = cluster_news(df)

    st.sidebar.title(SIDEBAR_TITLE)
    st.sidebar.info("Explore articles grouped by cluster below")

    display_clusters(df)

    with open("news_data.csv", "rb") as file:
        st.download_button(DOWNLOAD_LABEL, file, file_name="news_data.csv")

if __name__ == '__main__':
    main()
