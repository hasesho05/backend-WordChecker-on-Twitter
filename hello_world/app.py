import json
import os
import requests
import tweepy
import collections


def lambda_handler(event, context):

    try:
        query = event["queryStringParameters"]["id"]
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
    item_count = 100

    # tweet_list = [
    #     tweet.text
    #     for tweet in tweepy.Cursor(api.user_timeline, id=query).items(item_count)
    #     if (list(tweet.text)[:2] != ["R", "T"]) & (list(tweet.text)[0] != "@")
    # ]

    tweet_list = [
        tweet.text
        for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en").items(item_count)
        if (list(tweet.text)[:2] != ["R", "T"]) & (list(tweet.text)[0] != "@")
    ]

    temp_tweet = " ".join(tweet_list)
    temp_list = temp_tweet.split(" ")
    remove_list = [
        query,
        "a",
        "to",
        "for",
        "in",
        "of",
        "the",
        "and",
        "is",
        "on",
        "I",
        "you",
        "it",
        "that",
        "this",
        "with",
        "at",
        "from",
        "by",
        "are",
        "as",
        "be",
        "have",
        "or",
        "an",
        "will",
        "my",
        "can",
        "not",
        "but",
        "was",
        "what",
        "your",
        "all",
        "about",
        "there",
        "if",
        "when",
        "how",
        "up",
        "out",
        "so",
        "some",
        "he",
        "she",
        "they",
        "me",
        "we",
        "us",
        "our",
        "their",
        "them",
        "his",
        "her",
        "their",
        "its",
        "am",
        "do",
        "does",
        "did",
        "doing",
        "done",
        "into",
        "than",
        "too",
        "very",
        ".",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "",
    ]

    temp_list = [i for i in temp_list if i not in remove_list]
    counter = collections.Counter(temp_list)
    counter = counter.most_common(10)
    print(counter)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps({"tweetList": tweet_list, "counter": counter}),
    }
