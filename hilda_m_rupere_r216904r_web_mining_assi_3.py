import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# RSS feeds
RSS_FEEDS = {
    'BBC': 'https://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'Reuters': 'http://feeds.reuters.com/reuters/topNews',
    'NYTimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

# Classification
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

# Fetch news
def fetch_news():
    news_list = []
    for name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            summary = entry.get('summary', '') or entry.get('description', '')
            category = classify_news(title, summary)
            news_list.append({
                'source': name,
                'title': title,
                'link': link,
                'summary': summary,
                'category': category
            })
    return pd.DataFrame(news_list)

# Save CSV
def save_to_csv(df):
    df.to_csv("news_data.csv", index=False)

# Clustering
def cluster_news(df, n_clusters=4):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    df['summary'] = df['summary'].fillna('')
    X = vectorizer.fit_transform(df['summary'])
    model = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = model.fit_predict(X)
    return df

# Streamlit UI
def main():
    st.title("📰 Clustered News Viewer")
    st.caption("Assignment 3: Web-Content Mining — Tinashe Zigara R207669D")

    with st.spinner("Fetching news..."):
        df = fetch_news()
        save_to_csv(df)
        df = cluster_news(df)

    st.sidebar.title("Explore Clusters")
    cluster_id = st.sidebar.selectbox("Choose Cluster", sorted(df['cluster'].unique()))
    cluster_df = df[df['cluster'] == cluster_id]

    st.subheader(f"News in Cluster {cluster_id}")
    for _, row in cluster_df.iterrows():
        st.markdown(f"**{row['title']}**  \n{row['summary']}  \n[🔗 Read more]({row['link']})  \n*Category: {row['category']}*")
        st.markdown("---")

    with open("news_data.csv", "rb") as file:
        st.download_button("📥 Download CSV", file, file_name="news_data.csv")

if __name__ == '__main__':
    main()
