# -*- coding: utf-8 -*-
"""HILDA_M_RUPERE_R216904R WEB MINING ASSI 3

Original file is located at
    https://colab.research.google.com/drive/1x1D5X7rplOY2RwnOYwRsIopwx_Dyh2u2

**QUESTION** **1**
"""

# importing necessary libraries
import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
!pip install scrapy
!pip install streamlit
!pip install newspaper3k
!pip install feedparser

import scrapy
import logging

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = [
        "nytimes.com",  # Example 1
        "bbc.com",      # Example 2
        "cnn.com",      # Example 3
        "theguardian.com" # Example 4
    ]

    start_urls = [
        "https://www.nytimes.com/section/business",
        "https://www.bbc.com/news/business",
        "https://www.cnn.com/business",
        "https://www.theguardian.com/business",
        "https://www.nytimes.com/section/politics",
        "https://www.bbc.com/news/politics",
        "https://www.cnn.com/politics",
        "https://www.theguardian.com/politics",
        "https://www.nytimes.com/section/arts",
        "https://www.bbc.com/culture", # BBC uses a different structure for Arts/Culture
        "https://www.cnn.com/entertainment", # CNN's Arts/Culture is under Entertainment
        "https://www.theguardian.com/culture",
        "https://www.nytimes.com/section/sports",
        "https://www.bbc.com/sport",
        "https://www.cnn.com/sport",
        "https://www.theguardian.com/sport"
    ]

    custom_settings = {
        'LOG_LEVEL': logging.WARNING  # Adjust logging level as needed
    }

    def parse(self, response):
        # Determine category based on URL
        if "business" in response.url.lower():
            category = "Business"
        elif "politics" in response.url.lower():
            category = "Politics"
        elif "arts" in response.url.lower() or "culture" in response.url.lower() or "entertainment" in response.url.lower():
            category = "Arts/Culture/Celebrities"
        else:
            category = "Sports"

import csv

# Sample data (replace with your actual data from the Google Sheet)
data = [
    ['Category', 'Title', 'Content'],  # Header row
    ['Business', 'Article Title 1', 'Article Content 1'],
    ['Politics', 'Article Title 2', 'Article Content 2'],
    ['Arts/Culture/Celebrities', 'Article Title 3', 'Article Content 3'],
    ['Sports', 'Article Title 4', 'Article Content 4'],
]


def write_to_csv(data, filename='news_data.csv'):
    """Writes data to a CSV file.

    Args:
      data: A list of lists representing the data.
      filename: The name of the CSV file.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


write_to_csv(data)


def write_to_separate_csv_files(data):
  """Writes data to separate CSV files based on category."""
  categories = {}
  for row in data[1:]:  # Skip the header row
      category = row[0]
      if category not in categories:
          categories[category] = []
      categories[category].append(row)

  for category, rows in categories.items():
      filename = f"{category.replace('/', '_')}.csv"
      write_to_csv([data[0]] + rows, filename)  # Include header in each file

# Example usage
write_to_separate_csv_files(data)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_stories(csv_filepath, num_clusters=4):
    """
    Clusters news stories based on their content using KMeans clustering.

    Args:
        csv_filepath: Path to the CSV file containing news stories.
        num_clusters: The desired number of clusters.

    Returns:
        A pandas DataFrame with an added 'Cluster' column representing cluster assignments.
    """
    try:
        # Load data
        df = pd.read_csv(csv_filepath)

        # Combine title and content for vectorization
        df['text'] = df['Title'] + ' ' + df['Content']

        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english')  # Remove common English words
        vectors = vectorizer.fit_transform(df['text'])

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        df['Cluster'] = kmeans.fit_predict(vectors)

        return df

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return None

# Example usage
# Assuming your combined CSV file is named 'news_data.csv'
clustered_df = cluster_stories('news_data.csv')

if clustered_df is not None:
 clustered_df
    #Further processing or analysis of the clustered DataFrame

# prompt: from the already existing code above  generate code to Create a web based platform that displays a cluster and the urls of related stories in that cluster using streamlit

import streamlit as st
import pandas as pd

# Assuming 'clustered_df' is the DataFrame from the previous code
# Replace 'news_data.csv' with the actual path to your combined CSV
# clustered_df = cluster_stories('news_data.csv')

# Sample clustered data (replace with your actual clustered_df)
data = {
    'Category': ['Business', 'Politics', 'Arts/Culture/Celebrities', 'Sports', 'Business', 'Politics'],
    'Title': ['Article Title 1', 'Article Title 2', 'Article Title 3', 'Article Title 4', 'Article Title 5', 'Article Title 6'],
    'Content': ['Content 1', 'Content 2', 'Content 3', 'Content 4', 'Content 5', 'Content 6'],
    'Cluster': [0, 1, 2, 0, 1, 2],
    'URL': ['url1', 'url2', 'url3', 'url4', 'url5', 'url6'] # Add a URL column
}

clustered_df = pd.DataFrame(data)


st.title("Story ClustersNews ")
st.subheader("News Stories categorized into Business, Politics, Arts/Culture/Celebrities, and Sports")
st.subheader("Hilda Rupere r216904r  web assignment 3")

# Sidebar for cluster selection
selected_cluster = st.sidebar.selectbox("Select Cluster", clustered_df['Cluster'].unique())

# Filter DataFrame for the selected cluster
cluster_data = clustered_df[clustered_df['Cluster'] == selected_cluster]

# Display cluster information
st.write(f"## Cluster {selected_cluster}")

# Display stories in the selected cluster
for index, row in cluster_data.iterrows():
    st.write(f"**{row['Category']}**: [{row['Title']}]({row['URL']})")
    st.write(row['Content'])
    st.write("---") # separator between stories