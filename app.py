import streamlit as st
import snscrape.modules.twitter as sntwitter

def fetch_tweets(username, num_tweets=5):
    try:
        tweets = []
        scraper = sntwitter.TwitterUserScraper(username)

        # Debugging: Show scraper initialized message
        st.write(f"Scraper initialized for user: {username}")

        # Fetch tweets and store them in a list
        for i, tweet in enumerate(scraper.get_items()):
            if i >= num_tweets:
                break
            tweets.append(tweet.content)

        # Debugging: Show raw tweets data
        st.write(f"🔹 Raw Tweets Data: {tweets}")

        if not tweets:
            st.error(f"⚠️ No tweets found for {username}. The scraper might be blocked or the account is private.")
            return None
        
        return tweets
    
    except Exception as e:
        st.error(f"❌ Error fetching tweets: {e}")
        return None

def main():
    st.title("Twitter Sentiment Analysis")

    # Option to input text or fetch tweets
    option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])
    
    if option == "Input text":
        text_input = st.text_area("Enter text to analyze sentiment")
        if st.button("Analyze"):
            st.write(f"Sentiment: [Logic Needed]")  # Replace with actual model

    elif option == "Get tweets from user":
        username = st.text_input("Enter Twitter username")
        if st.button("Fetch Tweets"):
            tweets = fetch_tweets(username, num_tweets=5)
            if tweets:
                for tweet in tweets:
                    st.write(f"📢 {tweet}")  # Display tweets as raw text

if __name__ == "__main__":
    main()
