import tweepy
import json
import csv

consumer_key = 'L8tNdzu2q3n1JnBWn3CsetBuN'
consumer_secret = 'xu6Ys6W757EI0mcEHKNpux7qrIClslsolwoHRLlwDCHRslzQMS'
access_token = '1043037626695991296-ocEyZgIVQ6hcVpxiEPAqi5uEckzmag'
access_token_secret = 'Uh0nYzErw5hU136psP4oP8v2pIVUkxulTZalWB1R9bjQR'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name)

#####
# Opening Spotify Data <-- Top 100 tracks of 2017
#####

with open('top_spotify.json') as f:
  spot_data = json.load(f)


#####
# Open past twitter json file
#####
  
#do not forget the new tweets

td = [['id', 'author', 'text', 'in_reply']]

#with open('tweet_data.json') as f:
 # tweet_data = json.load(f)


###FINDS THE USERS THAT HAVE MENTIONED THE BOT


####
# Define the search
#####
query = '@jesslightsupli1'
max_tweets = 100

####
# Do the search
#####
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait                                                                                                                 
        # to keep things simple, we will give up on an error                                                                                                                          
        break


####
# Iterate over the search
#####
for status in searched_tweets:
  # do something with all these tweets                                                                                                                                                
  print	(status.text)

  #if(status.id in tweet_data['id']): ## check the tweets that already exist, if it does. ignore
  #  continue

  count = 0
  for i in spot_data:


    #INTENT NUMBER ONE <--- FIND THE SINGER FOR A SONG <-- uses entities
    #what is the singer for I don't want to live forever?
    #what is the artist that sang Stay with Me?

    if("artist" in status.text or "singer" in status.text):
      #api.update_status('what song? @' + status.author.screen_name, status.id_str)
      if('for' in status.text):
        song = status.text.split('for ')
        song_n = song[1]
        if(song_n in i["name"]):
          obj = i['artist']
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)
      if('sang' in status.text):
        song = status.text.split('sang ')
        song_n = song[1]
        if(song_n in i['name'].ignoreCase()):
          obj = i['artist']
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)



    #INTENT NUMBER TWO <--- FIND THE SONG BY SINGER <-- uses entities
    # what in the top of 2017 is a song by Zedd?
    # whst 2017 song featured Alessia Cara?
    if('song' in status.text and ('featured' in status.text or 'by' in status.text)):
      if('featured' in status.text):
        feat = status.text.split('featured ')
        artist_feat = feat[1]
        if(artist_feat in i["name"]):
          obj = i['name']
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)
      if('by' in status.text):
        art = status.text.split('by ')
        artist_n = art[1]
        if(artist_n in i['artist']):
          obj = i['name']
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)



    #INTENT NUMBER THREE <--- WHAT IS THE DANCIBILITY OF "Unforgettable"
    # can i dance to Unforgetable?
    # what is the danceability of Unforgetable?
    if("dance" in status.text and ('of' in status.text or 'to' in status.text)):
      if('to' in status.text):
        song_n = status.text.split('to ')
        song_name = song_n[1]
        if(song_name in i['name']):
          obj = 'yes'
          if(i['danceability'] < 0.5): 
            obj = 'no'
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)
      if('by' in status.text):
        song_n = status.text.split('of ')
        song_name = song_n[1]
        if(song_name in i['name']):
          obj = i['danceability']
          api.update_status(obj+' @' + status.author.screen_name, status.id_str)



    #INTENT NUMBER FOUR <--- HIGHEST RANKED SONG
    # what is the best song in 2017?
    # what is the highest ranked song in 2017?
    if("best" in status.text or ("highest" in status.text and "rank" in status.text)):
      obj = '----'
      if(count == 0):
        obj = i['name']
      api.update_status(obj,' @' + status.author.screen_name, status.id_str)


    #INTENT NUMBER FIVE <--- LOWEST RANKED SONG
    # what is the worst song in 2017?
    # what is the lowest ranked song in 2017?
    if("worst" in status.text or ("lowest" in status.text and "rank" in status.text)):
      obj = '----'
      if(count == 100):
        obj = i['name']

      api.update_status(obj,' @' + status.author.screen_name, status.id_str)

  count += 1
  
  ts = [status.id, status.author, status.text, status.in_reply_to_status_id]
  td.append(ts)

## uncomment to save file of old tweets
#with open('output_tweet.csv', 'w', newline='') as csvfile:
#  writer = csv.writer(csvfile)
#  writer.writerows(td)

#csvfile = open('output_tweet.csv', 'rt', encoding = 'utf-8')
#jsonfile = open('tweet_data.json', 'w')

#fieldnames = ('id','author','text','in_reply')
#reader = csv.DictReader(csvfile, fieldnames)
#for row in reader:
#    json.dump(row, jsonfile)
#    jsonfile.write('\n')

  #with open('tweet_data.json', 'w') as outfile:
  #json.dump(tweet_data, outfile)


