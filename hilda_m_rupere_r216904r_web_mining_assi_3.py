import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# Classify news based on keywords
def classify_news(title, summary):
    keywords = {
       
        'Politics': ['politics', 'election', 'senate', 'congress', 'law'],
        'Celebrities/Arts/Culture': ['art', 'movie', 'celebrity', 'theatre', 'culture'],
         'Business': ['economy', 'business', 'stocks', 'market', 'trade'],
        'Sports': ['sports', 'game', 'tournament', 'match', 'Olympics']
    }
    text = title.lower() + ' ' + summary.lower()
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category
    return 'Uncategorized'


# Fetch and parse the RSS feed
def fetch_news():
    url = 'https://feeds.bbci.co.uk/news/rss.xml'
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries:
        title = entry.get('title', 'No Title Available')
        link = entry.get('link', 'No URL Available')
        summary = entry.get('summary', entry.get('description', 'No Summary Available'))
        category = classify_news(title, summary)
        news_list.append({'title': title, 'link': link, 'summary': summary, 'category': category})
    return pd.DataFrame(news_list)


# Load data
news_df = fetch_news()

# Streamlit App
def main():
    st.title("a web based platform that displays a cluster and the urls of related stories in that cluster.")
    st.subheader("News Stories categorized into Business, Politics, Arts/Culture/Celebrities, and Sports")
    st.subheader("tinashe zigara r207669d assignment 3")

    # Display categories
    category_choice = st.sidebar.selectbox("Choose Category", ['Arts/Culture/Celebrities', 'Politics',  'Sports', 'Uncategorized','Business'])
    filtered_data = news_df[news_df['category'] == category_choice]

    for index, row in filtered_data.iterrows():
        st.write(f"**{row['title']}**")
        st.write(f"{row['summary']}")
        st.markdown(f"[Read more]({row['link']})")

if __name__ == '__main__':
    main()
