import credentials as cred
import tweepy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--to", help="Twitter screen name of the user to send to.")
parser.add_argument("--text", help="Tweet text.")
args = parser.parse_args()
text = argparse.REMAINDER

def tweet(to, text):
  auth = tweepy.OAuthHandler(cred.consumerKey, cred.consumerSecret)
  auth.set_access_token(cred.accessToken, cred.accessTokenSecret)
  api = tweepy.API(auth)
  api.send_direct_message(screen_name=to, text=text)

tweet(args.to, args.text)

