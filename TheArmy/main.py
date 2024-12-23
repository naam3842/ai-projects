from atproto import Client
from dotenv import load_dotenv
import os
import base64
import hashlib
import os
import re
import json
import requests
import argparse
import tweepy
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session, TokenUpdated

load_dotenv('.env')

def bluesky_post(message: str) -> None:
    """Send a POST request using the Python SDK"""

    login = os.environ['BLUESKY_USERNAME']
    password = os.environ['BLUESKY_PASSWORD']
    client = Client()
    client.login(login, password)
    response = client.send_post(message)

    print(f"POST request sent successfully: {response}")
    return None

def twitter_post(message: str, media='') -> None:
    
    api_key = os.environ['TWITTER_API_KEY']
    api_key_secret = os.environ['TWITTER_API_KEY_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    bearer_token = os.environ['TWITTER_BEARER_TOKEN']

    # Authenticate to Twitter API
    client = tweepy.Client(bearer_token,api_key,api_key_secret,access_token,access_token_secret)

    # Send POST request 
    if media != '':
        response = client.create_tweet(text=message, media_ids=[media])
    else:
        response = client.create_tweet(text=message)

    print(f"POST request sent successfully: {response}")

def twitter_image_upload(path: str):

    api_key = os.environ['TWITTER_API_KEY']
    api_key_secret = os.environ['TWITTER_API_KEY_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)



    media_id = api.media_upload(filename=path).media_id_string
    print(media_id)
    return media_id

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='A script that sends a message to Twitter and Bluesky.')
    parser.add_argument('-m', '--message', help='The message to send.', type=str, required=False)
    parser.add_argument('-p', '--platform', help='The platform to send the message.', type=str, required=False)

    # Parse the arguments
    args = parser.parse_args()

    if args.platform == 'twitter':
        twitter_post(args.message)
    elif args.platform == 'bluesky':
        bluesky_post(args.message)

    twitter_post('Slat')

if __name__ == '__main__':
    main()




















