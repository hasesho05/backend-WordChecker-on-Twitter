import json
import os
import requests
import tweepy


def lambda_handler(event, context):

    try:
        user_id = event["queryStringParameters"]["id"]
    except Exception as e:
        print(str(e))
        return {
            "statusCode": 200,
            "body": json.dumps({"message": str(e)}),
        }

    API_KEY = os.getenv("API_KEY")
    API_ACCESS = os.getenv("API_ACCESS")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    # Twitter API credentials
    auth = tweepy.OAuthHandler(API_KEY, API_ACCESS)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    search_words = "python"
    item_count = 10

    try:
        tweets = tweepy.Cursor(api.user_timeline, id=user_id).items(item_count)
    except Exception as e:
        print(str(e))
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "hello world"}),
        }

    tweet_list = [
        tweet.text
        for tweet in tweepy.Cursor(api.user_timeline, id=user_id).items(100)
        if (list(tweet.text)[:2] != ["R", "T"]) & (list(tweet.text)[0] != "@")
    ]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(tweet_list),
    }
