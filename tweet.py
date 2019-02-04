import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
class twitterclient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'FsVHlydbEgLPqGGeAlA1LAWOX'
        consumer_secret = 'NtKhY2BlsiEEf6AmdBEV553nXwIMRkBdOnSGU924EeGmOiO8gW'
        access_token = '1091545329399287808-tkcoJK3HRu5ozBKUfkm4UJSCpXmyBa'
        access_token_secret = 't4aLBImT5BTR79tvAxxacsToE3bRaLxbvWyBr4AmOSz0S'

        try:
            self.auth=OAuthHandler(consumer_key,consumer_secret)
            self.auth.set_access_token(access_token,access_token_secret)
            self.api=tweepy.API(self.auth)
        except:
            print("Error:Authentication Failed")

    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])\
                                |(\w+:\/\/\S+)"," ",tweet).split())

    def get_tweet_sentiment(self, tweet):
        a=TextBlob(self.clean_tweet(tweet))
        if a.sentiment.polarity>0:
            return 'positive'
        elif a.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
        


    def get_tweets(self,query,count=10):
        tweets=[]
        try:
            fetch_tweet=self.api.search(q=query,count=count)
            for i in fetch_tweet:
                p_t={}
                p_t['text']=i.text
                p_t['sentiment']=self.get_tweet_sentiment(i.text)
                if i.retweet_count>0:
                    if p_t not in tweets:
                        tweets.append(p_t)

            return tweets
        except tweepy.TweepError as e:
            print("error:"+str(e))






def main():
    str1=input("enter name of personality")
    api=twitterclient()
    tweets=api.get_tweets(query=str1,count=200)
    pt=[ i for i in tweets if i['sentiment']=='positive']
    nt=[ i for i in tweets if i['sentiment']=='negative']
    print("Positive tweets percentage: {} %".format(100*len(pt)/len(tweets)))
    print("negative tweets percentage: {} %".format(100*len(nt)/len(tweets)))
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(nt) - len(pt))/len(tweets)))
    print("\n\nPositive tweets:")
    for tweet in pt[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in nt[:10]:
        print(tweet['text'])
 

    
    



if __name__=="__main__":
        main()
        
