import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from ntscraper import Nitter

# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    try:
        with open('model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading model/vectorizer: {e}")
        return None, None

# Define sentiment prediction function
def predict_sentiment(text, model, vectorizer, stop_words):
    if not model or not vectorizer:
        return "Error: Model or vectorizer not loaded."
    
    # Preprocess text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower().split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text = vectorizer.transform([text])

    # Predict sentiment
    sentiment = model.predict(text)
    return "Negative" if sentiment == 0 else "Positive"

# Function to initialize the Nitter scraper with error handling
@st.cache_resource
def initialize_scraper():
    instances = [
        "https://nitter.privacydev.net",
        "https://nitter.fdn.fr",
        "https://nitter.kavin.rocks"
    ]
    
    for instance in instances:
        try:
            scraper = Nitter(instance=instance, log_level=1)
            return scraper
        except Exception as e:
            st.warning(f"Failed to connect to {instance}. Trying another instance...")
    
    st.error("All Nitter instances are unreachable. Please try again later.")
    return None

# Function to create a colored card for tweets
def create_card(tweet_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    return f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{tweet_text}</p>
    </div>
    """

# Main app logic
def main():
    st.title("Twitter Sentiment Analysis")

    # Load required resources
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()
    scraper = initialize_scraper()

    # Check if resources loaded successfully
    if not model or not vectorizer:
        st.error("Failed to load sentiment analysis model. Please check your files.")
        return

    # User input: either text input or Twitter username
    option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])
    
    if option == "Input text":
        text_input = st.text_area("Enter text to analyze sentiment")
        if st.button("Analyze"):
            sentiment = predict_sentiment(text_input, model, vectorizer, stop_words)
            st.write(f"Sentiment: {sentiment}")

    elif option == "Get tweets from user":
        username = st.text_input("Enter Twitter username")
        if st.button("Fetch Tweets"):
            if not scraper:
                st.error("Scraper is not available. Please try again later.")
                return
            
            try:
                tweets_data = scraper.get_tweets(username, mode='user', number=5)
                if tweets_data and 'tweets' in tweets_data and tweets_data['tweets']:
                    for tweet in tweets_data['tweets']:
                        tweet_text = tweet.get('text', 'No text available')
                        sentiment = predict_sentiment(tweet_text, model, vectorizer, stop_words)
                        st.markdown(create_card(tweet_text, sentiment), unsafe_allow_html=True)
                else:
                    st.warning("No tweets found for this user.")
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")

if __name__ == "__main__":
    main()
