import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from ntscraper import Nitter
import random

# Download stopwords once
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Load model and vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Initialize Nitter scraper with fallback
@st.cache_resource
def initialize_scraper():
    try:
        return Nitter()  # No 'instance' argument, uses default
    except Exception as e:
        st.error(f"Error initializing scraper: {e}")
        return None

# Fetch tweets safely
def fetch_tweets(scraper, username, num_tweets=5):
    try:
        tweets_data = scraper.get_tweets(username, mode='user', number=num_tweets)
        if not tweets_data or 'tweets' not in tweets_data or not tweets_data['tweets']:
            return None  # Return None if no tweets found
        return tweets_data['tweets']
    except Exception as e:
        st.error(f"Error fetching tweets: {e}")
        return None

# Sentiment prediction
def predict_sentiment(text, model, vectorizer, stop_words):
    text = re.sub('[^a-zA-Z]', ' ', text).lower().split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text_vectorized = vectorizer.transform([text])
    sentiment = model.predict(text_vectorized)
    return "Negative" if sentiment == 0 else "Positive"

# Create sentiment card
def create_card(tweet_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    return f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{tweet_text}</p>
    </div>
    """

# Main app
def main():
    st.title("Twitter Sentiment Analysis")

    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()
    scraper = initialize_scr
