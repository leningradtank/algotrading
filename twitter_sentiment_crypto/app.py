# Import dependencies
import re
import tweepy
import pandas as pd
from alpaca.data import CryptoDataStream
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Alpaca API Credentials
APCA_API_KEY = ''
APCA_SECRET_KEY = ''
trading_client = TradingClient(APCA_API_KEY, APCA_SECRET_KEY, paper=True)
crypto_stream = CryptoDataStream(APCA_API_KEY, APCA_SECRET_KEY, raw_data=True)

# Twitter API Credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define variables
num_tweets = 80
keyword = '$ETHUSD'
keyword_to_asset = {
    '$ETHUSD': 'ETHUSD'
}


# Check whether account currently holds symbol
def check_positions(symbol):
    positions = trading_client.get_all_positions()
    if symbol in str(positions):
        return 1
    return 0

# Clean the tweet content using regex
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Retrieve tweets from Twitter using keyword
def get_tweets(query, count):
    tweets = set()
    fetched_tweets = api.search(q=query, count=count)
    for tweet in fetched_tweets:
        cleaned_tweet = clean_tweet(tweet.text)
        if cleaned_tweet not in tweets:
            tweets.add(cleaned_tweet)
    return tweets

# Calculating the polarity of each tweet using nltk
def calculate_polarity(tweets):
    scores = []
    for tweet in tweets:
        pol_score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        pol_score['tweet'] = tweet
        scores.append(pol_score)
    return scores

# Placing trades based on the polarity of the tweets
def twitter_bot(symbol, close, qty=10):
    position = check_positions(symbol=symbol)
    tweets = get_tweets(keyword, num_tweets)
    scores = calculate_polarity(tweets)

    mean = pd.DataFrame.from_records(scores).mean()
    compound_score = mean['compound']
    print (f"Sentiment score: {round(compound_score, 3)}")

    if compound_score >= 0.05 and position==0:
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC)

        trading_client.submit_order(
            order_data=market_order_data)
        print(f"Bought {symbol} at approx. {close}")

    elif compound_score <= -0.05 and position==1:
        trading_client.close_position(symbol_or_asset_id=symbol)
        print(f"Sold {symbol} at approx. {close}")

    return True


# Live streaming of crypto pricing data
async def quote_data_handler(data):
    close = data['c']
    twitter_bot(keyword_to_asset[keyword], close, qty=10)

crypto_stream.subscribe_bars(quote_data_handler, keyword_to_asset[keyword])
crypto_stream.run()