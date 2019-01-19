# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 20:25:00 2019

@author: Philippe
"""

def cluster_analysis(labels,num=5,K=2):
    # function that takes in input a list of labels and returns 
    # a list of the users with the highest in degree in each cluster
    labels_split=[np.where(labels==i) for i in range(K)]
    nodes = np.array(G.nodes())
    nodes_split = [nodes[labels_split[i]] for i in range(K)]
    
    
    G_i=[G.subgraph(nodes_split[i]) for i in range(K)]
    A_i=[nx.adjacency_matrix(G_i[i]).toarray() for i in range(K)]
    in_degrees = [np.sum(A_i[i],axis=0).reshape(-1) for i in range(K)]
    most_seen = [np.array(G_i[i].nodes())[np.argsort(in_degrees[i])[-1*num:]] for i in range(K)]
    most_seen_dict = [[{'tweet':[]} for i in range(len(most_seen[j]))] for j in range(K)]
    
    with open('json_users_for_graph.json','r') as file:
        data_users = json.load(file)
    
    with open('json_tweets.json','r') as file:
        data_tweet = json.load(file)
    
    for k in range(K):
        for j in range(len(most_seen[k])):    
            for i in range(len(data_tweet)):
                user = data_tweet[i]['user_id']
                twt = data_tweet[i]['tweet_text']
                if user==most_seen[k][j]:
                    most_seen_dict[k][j]['tweet'].append(twt)
    
    
    for k in range(K):
        for j in range(len(most_seen[k])):   
            for i in range(len(data_users)):
                user = data_users[i]['user_id']
                if user==most_seen[k][j]:
                    most_seen_dict[k][j]['statuses_count']=data_users[i]['statuses_count']
                    most_seen_dict[k][j]['screen_name']=data_users[i]['screen_name']
                    most_seen_dict[k][j]['user_id']=user
    
    return most_seen_dict

def get_subgraphs(G,labels,K=2):
    labels_split=[np.where(labels==i) for i in range(K)]
    nodes = np.array(G.nodes())
    nodes_split = [nodes[labels_split[i]] for i in range(K)]
    G_i=[G.subgraph(nodes_split[i]) for i in range(K)]
    
    return G_i

def get_high_ranked(G,num):
    pr = nx.pagerank(G, alpha=0.9)
    keys = list(pr.keys())
    values = list(pr.values())
    idx = np.argsort(np.array(values))[-1*num:]
    
    with open('json_users_for_graph.json','r') as file:
        data = json.load(file)

    data_dict = {}
    
    for i in range(len(data)):
        user_id = data[i]['user_id']
        friends = data[i]['friends']
        polarity = data[i]['polarity']
        screen_name = data[i]['screen_name']
        res={}
        res['friends']=friends
        res['screen_name']=screen_name
        res['polarity'] = polarity
        data_dict[user_id]=res
    L=[]
    for i in range(num):
        key = keys[idx[-i-1]]
        screen_name=data_dict[key]['screen_name']
        L.append(screen_name)
    
    return L

def plot_evolution(r_range):
    L=[]
    for i in range(len(r_range)):
        r=r_range[i]
        G=get_graph(r)
        labels= clustering2(G)
        temp = [sum(labels),len(labels)-sum(labels)]
        L.append(min(temp))
    return L

    