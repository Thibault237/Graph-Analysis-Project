# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 13:44:06 2018

@author: Philippe
"""

import json
import tweepy
from tweepy import RateLimitError
import time
# Les clés du projet des supelecs plus ma clé en dernier
# 17 clés au total

CONSUMER_KEY = ['dLipeeKq54VbChk24CsV1Sogr', '3v9gKs9KWwfHxAuMmBgIE8jaw', 'qpUp0xtdfiBPBtBMxzbNXMd8h',
                'XpuwAn9OMBcWGeQNvoPZ69QIu', 'NYARbeG6y79N5k7MNt6ueK3L1', 'Qd6ry4NvpAcM2TBprtmNv41Uj',
                'QfXiBks8G6pMHIFDUxeeDLW37', 'C9uM0HndBaYgTx4QuYoSxEpBs', 'PvHynNYscVpbni5s7L6Qdm7MP',
                'A8514W8sACwLukrQqerFz9NFS', '8nXro72VhLCIsXzuR2c2eD0qI', 'RX49BZSjraUq1ER4wcWS6QfsM',
                'yXVeLxbbX1F4z1dAXHxBmKpHO', 'XyWfu0fRqOnR60IxmOASUrjRt', 'TkqwpPUQVeDlob4H5soCiBM6q',
                'O5a4hrLxVjNMfYo6CqQZ8GGs7','lbwD23hqBlUwrnC8KAxquZLWT']

CONSUMER_SECRET = ['l5t23Z1QuXQdGbDcF3JwHgvCqRXVPwyg8ZLQZfbpA8kzYhPpiD', 'sHOTBWvv2msq7Ojat79ECCcdg993PTtV4FJwO2DEepcZhPnqLd',
                   'MGr17cEcy5MZt0UWVOMctg9UFe6hhLAcZPK4ZNCQdc8cAqLCXp', '2915An4yPLcQ2rI6dYjSPZQq9IyYIFmYmDQXKEPg0YQ2xUwRlF',
                   'ySjmDMpoMqqcvHCoOf8lIHBwFzFSN5aUY6DuxkZZ3LPM97XIYf', 'bbiTkBHjjqNQ9xKYFnzcRJVZf0OP7RhbB6y8o4cv8F5pYPlCUA',
                   '8eXtr8U3tdZVzVYu0pGk09EqxBJqARjhF3jzWBRTdDRXJL1pqV', 'uTnQnaDR9lX9CrGL5NivGYsJZOqhoOPnroikSGmL3KYY9o9fNj',
                   'OFVkHTPmjqO7K9ooAl2lwuR4B7jaLrOxTliPnlVjRbK4lXD0Rn', 'kFjECikiOX4Kw5tlDI5bgeGDqkI8PVZBDwNIknZdEBQXWNz4ss',
                   'NPT6fPHtCATaLRxGSe6CC84cHLieu1vaLugkhLCiO9CRFWOWfN', 'jKtG3VMkyputedMMWAgzto1fDZdriI2xyX7avovelE0xhLRZSg',
                   '9fjnHgrUKTh6yjB6s5O70qfUzJzWqdjpQ6gmgiBKPjSEVMadFb', 'xWUEZTElLhNryWfzMLrhyLuYwyaX4L0jW0yAAy604pt5QI2vrh',
                   'nXK2xKwfHlEzc7GefL0Tw2HKvrNdvfdzQ4XGggBWmvXcLBbX5e', 'BQzT4Nfe5b5UQdD9y4Yq8pmhxfc1N2ESYCGd8spfCyRu6PZCv0','mPqTB1v8VFjV50QfxPyCYcXORLj5QjpfLSp001EQp4V3xvUV5P']

num_tweets=1000
max_friends=1500
limit_until_save=50
compteur_tweets=0
max_id=-1

# We'll store the tweets we got from the api in a json file (list of dictionaries)
# each dictionary will have the following keys:
#   'tweet_id'
#   'tweet_text'
#   'user_id'

with open('json_tweets_test.json','w') as file:
    json.dump([],file)

# We won't let the json file open during the whole operation in case we need to stop the program
# However, we won't do an i/o operation each time we retrieve a tweet
# The twitts retrieved will be stored in a temporary list L_tweet which will
# be dumped in th json file when its size reaches 50 and reset to an empty list
L_tweets=[]   

# We create a json file to store informaion about each user we encounter
# We store their friends ids,
# the number of twitts the user has published
# and the user's screen_name
# each element of this json file is a dictionary with the following keys:
#   user_id
#   friends: list containing all of its friends'ids
#   statuses_count: number of twitts he has published in his account
#   screen_name

with open('json_users_test.json','w') as file:
    json.dump([],file)  

# same goes for this file, we create a temporary list L_friends
# which we dump in the json file when its size reaches 50 and reset to
# an empty dictionary
L_users=[]

# To quickly look for a users which we have already seen,
# We use the list L_unique_users to store only the
# unique users_ids we have encountered
L_unique_users=[]

# increment the api number. if we attain the last one (number 16),
# Then we switch back to the first one.
# In order to have the rate limit renewed, we sleep for 15 minutes
# minus the timestamp from the last time we switched to api 1

def increment_api(num_api,first_loop=False):
    if first_loop:
        return num_api
    elif num_api==16:
        print('Changing Api')
        # If the currently used api is the 17th, we will switch back to the first one
        # but since we don't know how much time has passed since the rate limit
        # has been reached for this api, we sleep for 15 minutes
        print('Sleeping for 15 minutes \U0001F634')
        time.sleep(5*60)
        print('\t10 minutes left...')
        time.sleep(5*60)
        print('\t5 minutes left...')
        time.sleep(5*60)
        print('Switching to Api n°0\n')
        return 0
    else:
        print('Changing Api')
        print('Switching to Api n°{}\n'.format(num_api+1))
        return num_api+1

# choose the next api for which the rate_limit is not attained for the relevant category
# (search or friends)
def increment_api2(num_api,category,first_loop=False):
    if first_loop:
        return num_api
    else:
        print('Changing Api\n')
        for i in range(1,18):
            candidate = (num_api+i) %17
            auth = tweepy.AppAuthHandler(CONSUMER_KEY[candidate], CONSUMER_SECRET[candidate])
            api = tweepy.API(auth, compression=True)
            if category=='search':
                rate_limit = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
            else:
                rate_limit = api.rate_limit_status()['resources']['friends']['/friends/ids']['remaining']
            if rate_limit>0:
                print('Switching to Api n°{} with {} remaining {} requests'.format(candidate,rate_limit,category))
                return candidate
        
        print('Sleeping for 15 minutes '+'\U0001F634')
        time.sleep(5*60)
        print('\t10 minutes left...')
        time.sleep(5*60)
        print('\t5minutes left...')
        time.sleep(5*60)
        return num_api
    
    
    
max_id=None  
''' For now, this loop is infinite if there exists less tweets meeting the criterion than
    the variable num_tweets'''

num_api1=0
first_loop_1=True
num_api2=0
while compteur_tweets<num_tweets:
    num_api1 = increment_api(num_api1,first_loop=first_loop_1)
    first_loop_1=False
    # we are sure to have some slack with the new api because of the 15 minutes sleep
    # in the increment_api function
    auth = tweepy.AppAuthHandler(CONSUMER_KEY[num_api1], CONSUMER_SECRET[num_api1])
    api1 = tweepy.API(auth, compression=True)
    
    # tweet_cursor gives a list of pages each containing 100 twitts (maximum allowed by twitter per request)
    # each page equals to one request and the api is allowed to 450 requests every 15/minutes
    # The max_id takes the id of the last tweet
    # of each page.
    # this argument is used to get back to the query at the appropriate page
    # after we had to go out of the while loop to swith api
    tweet_cursor = tweepy.Cursor(api1.search,q='#GiletsJaunes AND -filter:retweets AND -filter:replies'
                                 ,lang='fr',tweet_mode='extended',\
                                 count=100,geocode='48.880695,2.319111,5km',max_id=max_id).pages()
    
    stay_in_loop_1 = True
    while stay_in_loop_1:
        # check if we haven't switched api below in the query to retrieve a user's friends
        try:
            page = tweet_cursor.next()
            max_id=int(page[-1]._json['id_str'])
            for tweet in page:
                if compteur_tweets>=num_tweets:
                    stay_in_loop_1=False
                    break
                
                twt = tweet._json
                twt_id = int(twt['id_str'])
                try:
                    twt_text = twt['full_text']
                except:
                    twt_text = twt['text']
                user_screen_name = twt['user']['screen_name']
                user_id = int(twt['user']['id_str'])
                user_statuses_count = twt['user']['statuses_count']
                    
                dic_tweet = {'tweet_id':twt_id,
                             'tweet_text':twt_text,
                             'user_id':user_id}
                    
                L_tweets.append(dic_tweet)
                    
                if len(L_tweets)==limit_until_save:
                    with open('json_tweets_test.json','r') as file1:
                        data = json.load(file1)
                        with open('json_tweets_test.json','w') as file2:
                            data.extend(L_tweets)
                            json.dump(data,file2)
                    print('\tProcessed {} tweets\n'.format(compteur_tweets))
                    L_tweets=[]
                # At this point we will get the user's friends (with a limit of 1500 friends)
                # We check if the user's friends are already in the user_friends.json file
                user_in_json=False
                if user_id in L_unique_users:
                    user_in_json=True
                    
                # If the user is not know, we get it's friends (i.e people he follows)
                # via the api.friends_ids method
                    
                if not user_in_json:
                    # In the same way, this cursor will let us
                    # keep track of the page we're at if we have to leave the
                    # Cursor iteration to switch API
                    print('Getting friends of user {}'.format(user_screen_name))
                    L_unique_users.append(user_id)
                    friends_num_cursor=-1
                    first_loop_2=True     # num_api2 is incremented when we enter in the
                    got_all_friends=False   # loop so it starts at the same api than above
                    L_friends=[]
                     
                    while not got_all_friends:
                            
                        num_api2 = increment_api(num_api2, first_loop=first_loop_2)
                        first_loop_2=False
                        auth = tweepy.AppAuthHandler(CONSUMER_KEY[num_api2], CONSUMER_SECRET[num_api2])
                        api2 = tweepy.API(auth, compression=True)
                        # limit per request for friends_ids is 200
                        friends_cursor = tweepy.Cursor(api2.friends_ids,id=user_id,count=200,
                                                           cursor=friends_num_cursor).pages()
                        
                        stay_in_loop_2=True
                        while stay_in_loop_2:
                            try:
                                if friends_cursor.next_cursor==0: # happens when all friends have been seen
                                    stay_in_loop_2=False
                                    got_all_friends=True
                                else:
                                    page = friends_cursor.next()
                                    friends_num_cursor = friends_cursor.next_cursor
                                    L_friends.extend(page)
                                    print('\t200 more friends')
                                    if len(L_friends)>max_friends:
                                        print('------- friends limit reached --------')
                                        stay_in_loop_2=False
                                        got_all_friends=True
                            except RateLimitError:
                                stay_in_loop_2=False
                            except StopIteration: # Happens when the user has no friends
                                stay_in_loop_2=False
                                got_all_friends=True
                                
                    print('-------- got friends --------\n')
                    dico_user = {'user_id':user_id,
                                 'friends':L_friends,
                                 'statuses_count':user_statuses_count}
                    L_users.append(dico_user)
                    if len(L_users)==limit_until_save:
                        with open('json_users_test.json','r') as file1:
                            data = json.load(file1)
                            with open('json_users_test.json','w') as file2:
                                data.extend(L_users)
                                json.dump(data,file2)
                        L_users=[]
                
                # At this point we have processed one tweet
                # and updated the user database if needed
                compteur_tweets+=1
            
            # if trying to get the next page we hit the rate_limit
            # we will use this id to start over with a new api from the tweet
        except RateLimitError: # happends when the rate _limit is reached for the api
            stay_in_loop_1=False
        
        
            if len(page)<100:
                print('All tweets retrieved')
                compteur_tweets = num_tweets+1
                stay_in_loop_1=False

# since we got out of the loop, the variables L_tweet and dict_friends
# probably contains values that have not been stored already in the
# relevant files
# these final lines do this
with open('json_tweets_test.json','r') as file1:
    data = json.load(file1)
    with open('json_tweets_test.json','w') as file2:
        data.extend(L_tweets)
        json.dump(data,file2)

with open('json_users_test.json','r') as file1:
    data = json.load(file1)
    with open('json_users_test.json','w') as file2:
        data.extend(L_users)
        json.dump(data,file2)
