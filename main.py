import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


import csv
import time


print("\n\nTwitter:")
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'jOT9AAdiLdPnbxjRtZ5AOckMb'
        consumer_secret = 'DRfAWHxnJri8JeDZ9oc7mzJ3fGcjiahEnOxlJq8cECLd6y2Lu0'
        access_token = '953467833438101504-39gE6N6oVYO1DLobQYb6rX04KGcJ8pR'
        access_token_secret = 'MbWnzxJG5g1gwGGkstuCo2iGbcvGWrsnK5Q5AT4sJyNZk'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def term_analyzer(self, tweets):
      print('test')

    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                parsed_tweet['retweets'] = tweet.retweet_count
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets \
    col_list = ["budget", "company", "country", "director", "genre", "gross", "name", "rating", "released", "runtime", "score", "star", "votes", "writer", "year"]
    df = pd.read_csv('movieSETT.csv', usecols = col_list, encoding="cp1252")

    print(df['name'])

    testMovies = df.name.tolist()

    #testMovies = ['Once Upon A Time In Hollywood', 'Invisible Man', 'Iron Man', 'Jaws', 'Back To the Future']

    movieCount = 0
    
    finaldata=[]

    #initialize w option for string inputs, and count adjustment
    fuckUp = True
    if fuckUp == True:
        time.sleep(900)
        #15min?

    #for loop MOIES IN MOVIESET>>>>>>>>>>>>> feed 
    for movie in testMovies:

      movieCount+=1
      print("Movie Number {0}".format(movieCount))
      if movieCount%17 == 0:
        time.sleep(91)
        


      tweets = api.get_tweets(movie, count = 500) 

      #print(tweets) #array of [{text, sentiment, rtweets,..?}, ...]
      #print(len(tweets))

      retweetcount = 0
      #retweetcount
      for tweet in tweets:
        retweetcount += tweet['retweets']
      print("Retweet Count: {}".format(retweetcount))
      #DIVIDE BY POS AND NEG RETWEETS????

      l = 1 if len(tweets) == 0 else len(tweets)



      # picking positive tweets from tweets 
      ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
      # percentage of positive tweets 
      print("Positive tweets percentage: {} %".format(100*len(ptweets)/l)) 
      posretweetcount = 0
      #retweetcount
      for tweet in ptweets:
        posretweetcount += tweet['retweets']
      print("Positive Retweet Count: {}".format(posretweetcount))



      # picking negative tweets from tweets 
      ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
      # percentage of negative tweets 
      print("Negative tweets percentage: {} %".format(100*len(ntweets)/l)) 
      negretweetcount = 0
      #retweetcount
      for tweet in ntweets:
        negretweetcount += tweet['retweets']
      print("Negative Retweet Count: {}".format(negretweetcount))



      #percentage of neutral tweets 
      print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/l)) 


      #MOVIE NAME, tweets parsed, retweets, etc
      movieTuple = movie, len(tweets), retweetcount, (100*len(ptweets)/l), posretweetcount, (100*len(ntweets)/l), negretweetcount, (100*(len(tweets) - len(ntweets) - len(ptweets))/l)

      
      print(movieTuple)
      print("\n\n\n")

      finaldata.append(movieTuple)








    with open('output.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['name','tweets analyzed','total retweets', 'positive percentage', 'positive retweets','negative percentage', 'negative retweets', 'neutral tweets'])
        for row in finaldata:
            csv_out.writerow(row)

  
    # printing first 5 positive tweets 
    #print("\n\nPositive tweets:") 
    #for tweet in ptweets[:10]: 
    #    print(tweet['text']) 
  
    # printing first 5 negative tweets 
    #print("\n\nNegative tweets:") 
    #for tweet in ntweets[:10]: 
    #    print(tweet['text'])

if __name__ == "__main__": 
    # calling main function 
    main()