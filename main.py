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
  
    def clean_tweet(self, tweet, movieName): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
                '''

        #print("BEFORE CLEAN TWEET:::::" + tweet)
        #print("movie name::: " + movieName)        
        query = tweet
        stop = movieName.lower()
        stopwords = stop.split()
        querywords = query.split()

        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        result = ' '.join(resultwords)
        #print("AFTER TWEET CLEANED::::::" + result)

        # + "movie"?!?!?!?!?

        #REMOVE RETWEETS
        # WHY REMOVING NUMBERS>>>???
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", result).split()) 
  
    def get_tweet_sentiment(self, tweet, movieName): 
        analysis = TextBlob(self.clean_tweet(tweet, movieName)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

        #also return subjectivity
  
    def term_analyzer(self, tweets):
      print('test')

    def get_tweets(self, query, count = 500): 
        tweets = [] 
        movTweets = []

        #append term(s) "movie" to query?!?!?!

        #if final list to return not full, get more tweets
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 
            tweetCounter = 0
            movTweetCounter = 0 #\/same!?
            movieTermCounter = 0
            for tweet in fetched_tweets: 
                parsed_tweet = {}
                movieSpec_tweet = {} 
                #assign variables if does not contain RT!!!!
                if 'RT' not in tweet.text:
                  parsed_tweet['text'] = tweet.text 
                  #log nummber of times movie in tweets
                  if 'movie' in tweet.text:
                    movieTermCounter += 1
                  elif 'Movie' in tweet.text:
                    movieTermCounter += 1  
                  elif 'film' in tweet.text:
                    movieTermCounter += 1    
                  elif 'Film' in tweet.text:
                    movieTermCounter += 1  
                  elif 'cinema' in tweet.text:
                    movieTermCounter += 1    
                  elif 'Cinema' in tweet.text:
                    movieTermCounter += 1  
                  elif 'Netflix' in tweet.text:
                    movieTermCounter += 1    
                  elif 'netflix' in tweet.text:
                    movieTermCounter += 1 
                  elif 'Hulu' in tweet.text:
                    movieTermCounter += 1    
                  elif 'hulu' in tweet.text:
                    movieTermCounter += 1 
                  parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text, query) 
                  parsed_tweet['retweets'] = tweet.retweet_count
                  tweetCounter+= 1
                  tweets.append(parsed_tweet) 
                #redundant???
                # if tweet.retweet_count > 0: 
                #     if 'RT' not in parsed_tweet['text'] and parsed_tweet not in tweets:
                #         tweets.append(parsed_tweet) 
                if 'RT' not in tweet.text:
                  containsMovieTerm = False
                  movieSpec_tweet['text'] = tweet.text 
                  #log nummber of times movie in tweets
                  if 'movie' in tweet.text:
                    containsMovieTerm = True
                  elif 'Movie' in tweet.text:
                    containsMovieTerm = True
                  elif 'film' in tweet.text:
                    containsMovieTerm = True
                  elif 'Film' in tweet.text:
                    containsMovieTerm = True
                  elif 'cinema' in tweet.text:
                    containsMovieTerm = True
                  elif 'Cinema' in tweet.text:
                    containsMovieTerm = True
                  elif 'Netflix' in tweet.text:
                    containsMovieTerm = True
                  elif 'netflix' in tweet.text:
                    containsMovieTerm = True
                  elif 'Hulu' in tweet.text:
                    containsMovieTerm = True
                  elif 'hulu' in tweet.text:
                    containsMovieTerm = True

                  if containsMovieTerm == True:
                    movieSpec_tweet['sentiment'] = parsed_tweet['sentiment']
                    movieSpec_tweet['retweets'] = parsed_tweet['retweets']
                    movTweetCounter+=1
                    movTweets.append(movieSpec_tweet) 


                else: 
                    continue

            test = True
            if test == True:
              count = len(tweets)-len(movTweets) 
              print(count) 

              query += " movie" # TRY OTHER TERMS???
              print(query)

              fetched_tweets = self.api.search(q = query, count = count)

              for tweet in fetched_tweets: 
                PmS_tweet = {}
                #assign variables if does not contain RT!!!!
                if 'RT' not in tweet.text:
                  PmS_tweet['text'] = tweet.text 
                  print("\n\n\nfull only movies tweets:" + PmS_tweet['text'])
                  PmS_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text, query) 
                  PmS_tweet['retweets'] = tweet.retweet_count
                  movTweets.append(PmS_tweet) 

            
            print(tweets)
            print("\nmovieterm counter:::: " + str(movieTermCounter))
            print("\nmovietweet counter:::: " + str(movTweetCounter))
            print("\ntweet counter:::: " + str(tweetCounter)) #should match\/
            print("length of returned tweets: " + str(len(tweets)))

            return tweets, tweetCounter, movieTermCounter, movTweets, movTweetCounter
  
        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets \
    col_list = ["budget", "company", "country", "director", "genre", "gross", "name", "rating", "released", "runtime", "score", "star", "votes", "writer", "year"]
    df = pd.read_csv('movieSETT2016.csv', usecols = col_list, encoding="cp1252")

    print(df['name'])

    testMovies = df.name.tolist()

    #testMovies = ['Once Upon A Time In Hollywood', 'Invisible Man', 'Iron Man', 'Jaws', 'Back To the Future']

    # tweet = 'words and rworadf rt sdfjsf something twitter something somethinf Cradle 2 the Grave'
    # movieName = testMovies[0]
    # print("movie name::: " + movieName) 
    # print("BEFORE CLEAN TWEET:::::" + tweet)        
    # query = tweet
    # stop = movieName.lower()
    # stopwords = stop.split()
    # querywords = query.split()
    # print(stopwords)
    # resultwords  = [word for word in querywords if word.lower() not in stopwords]
    # result = ' '.join(resultwords)
    # print("AFTER TWEET CLEANED::::::" + result)


    movieCount = 0
    
    finaldata=[]
    mfinaldata=[]

    #initialize w option for string inputs, and count adjustment
    fuckUp = False
    if fuckUp == True:
        time.sleep(850)
        #15min?

    #for loop MOIES IN MOVIESET>>>>>>>>>>>>> feed 
    for movie in testMovies:

      movieCount+=1
      print("Movie Number {0}".format(movieCount))
      if movieCount%17 == 0:
        time.sleep(91)
        
      tweets, tweetCounter, movieTermCounter, movTweets, movTweetCounter = api.get_tweets(movie, count = 500) 



      ###################BASE movie set########################

      #print(tweets) #array of [{text, sentiment, rtweets,..?}, ...]
      #print(len(tweets))

      retweetcount = 0
      #retweetcount
      for tweet in tweets:
        retweetcount += tweet['retweets']
      #print("Retweet Count: {}".format(retweetcount))
      #DIVIDE BY POS AND NEG RETWEETS????

      l = 1 if len(tweets) == 0 else len(tweets)



      # picking positive tweets from tweets 
      ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
      # percentage of positive tweets 
      #print("Positive tweets percentage: {} %".format(100*len(ptweets)/l)) 
      posretweetcount = 0
      #retweetcount
      for tweet in ptweets:
        posretweetcount += tweet['retweets']
      #print("Positive Retweet Count: {}".format(posretweetcount))



      # picking negative tweets from tweets 
      ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
      # percentage of negative tweets 
      #print("Negative tweets percentage: {} %".format(100*len(ntweets)/l)) 
      negretweetcount = 0
      #retweetcount
      for tweet in ntweets:
        negretweetcount += tweet['retweets']
      #print("Negative Retweet Count: {}".format(negretweetcount))



      #percentage of neutral tweets 
      #print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/l)) 


      #MOVIE NAME, tweets parsed, retweets, etc
      movieTuple = movie, len(tweets), tweetCounter, movieTermCounter, retweetcount, (100*len(ptweets)/l), posretweetcount, (100*len(ntweets)/l), negretweetcount, (100*(len(tweets) - len(ntweets) - len(ptweets))/l)

      
      print(movieTuple)
      print("\n\n\n")

      finaldata.append(movieTuple)

      if movieCount%1 ==0:
        with open('output.csv','w') as out:
          csv_out=csv.writer(out)
          csv_out.writerow(['name','tweets analyzed', 'tweetCounter', 'movieTermCount', 'total retweets', 'positive percentage', 'positive retweets','negative percentage', 'negative retweets', 'neutral tweets'])
          for row in finaldata:
              csv_out.writerow(row)



      ###################SAME FOR movSET########################


      mretweetcount = 0
      #retweetcount
      for mtweet in movTweets:
        mretweetcount += mtweet['retweets']
      #print("Retweet Count: {}".format(retweetcount))
      #DIVIDE BY POS AND NEG RETWEETS????

      l = 1 if len(movTweets) == 0 else len(movTweets)



      # picking positive tweets from tweets 
      mptweets = [mtweet for mtweet in movTweets if mtweet['sentiment'] == 'positive'] 
      # percentage of positive tweets 
      #print("Positive tweets percentage: {} %".format(100*len(ptweets)/l)) 
      mposretweetcount = 0
      #retweetcount
      for mtweet in mptweets:
        mposretweetcount += mtweet['retweets']
      #print("Positive Retweet Count: {}".format(posretweetcount))



      # picking negative tweets from tweets 
      mntweets = [mtweet for mtweet in movTweets if mtweet['sentiment'] == 'negative'] 
      # percentage of negative tweets 
      #print("Negative tweets percentage: {} %".format(100*len(ntweets)/l)) 
      mnegretweetcount = 0
      #retweetcount
      for mtweet in mntweets:
        mnegretweetcount += mtweet['retweets']
      #print("Negative Retweet Count: {}".format(negretweetcount))



      #percentage of neutral tweets 
      #print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/l)) 


      #MOVIE NAME, tweets parsed, retweets, etc
      mmovieTuple = movie, len(movTweets), movTweetCounter, movieTermCounter, mretweetcount, (100*len(mptweets)/l), mposretweetcount, (100*len(mntweets)/l), mnegretweetcount, (100*(len(movTweets) - len(mntweets) - len(mptweets))/l)

      
      print(mmovieTuple)
      print("\n\n\n")

      mfinaldata.append(mmovieTuple)

      if movieCount%1 ==0:
        with open('mOutput.csv','w') as out:
          csv_out=csv.writer(out)
          csv_out.writerow(['name','tweets analyzed', 'movTweetCounter', 'movieTermCount', 'total retweets', 'positive percentage', 'positive retweets','negative percentage', 'negative retweets', 'neutral tweets'])
          for row in mfinaldata:
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