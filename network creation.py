# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 13:19:52 2019

@author: Philippe
"""

import networkx as nx
import numpy as np
import json 


def get_graph(r):
    with open('json_users_for_graph.json','r') as file:
        data = json.load(file)
    
    
    for i in range(len(data)):
        polarities = data[i]['polarity']
        data[i]['polarity'] = np.mean(polarities)
        data[i]['tweet_count'] = len(polarities)
    
    for i in range(len(data)):
        res=0
        friends = data[i]['friends']
        for j in range(len(data)):
            if data[j]['user_id'] in friends:
                res+=data[i]['tweet_count']
        data[i]['friends_tweet_count']=res
    
    data_dict = {}
    
    for i in range(len(data)):
        user_id = data[i]['user_id']
        friends = data[i]['friends']
        polarity = data[i]['polarity']
        screen_name = data[i]['screen_name']
        tweet_count = data[i]['tweet_count']
        friends_tweet_count = data[i]['friends_tweet_count']
        vec = data[i]['vec']
        res={}
        res['friends']=friends
        res['screen_name']=screen_name
        res['polarity'] = polarity
        res['tweet_count']=tweet_count
        res['friends_tweet_count']=friends_tweet_count
        res['vec']=vec
        data_dict[user_id]=res
    
    
    def weight(vec1,vec2,r):
        x1 = np.array(vec1)
        x2 = np.array(vec2)
        cosine = np.dot(x1,x2)/(np.linalg.norm(x1)*np.linalg.norm(x2))
        return np.exp((1+cosine)/r)
    
    edges = []
    for user in data_dict:
        L=[]
        user_vec = data_dict[user]['vec']
        for friend in data_dict[user]['friends']:
            friend_vec = data_dict[friend]['vec']
            weight(user_vec,friend_vec,r)
            tup = (user,friend,weight)
            L.append(tup)
        edges.extend(L)
    
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    
    for user in data_dict:
        try:
            G.nodes[user]['screen_name'] = data_dict[user]['screen_name']
        except KeyError:
            pass
    
    return G

