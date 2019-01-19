# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 21:17:37 2019

@author: Philippe
"""

import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from discreteMarkovChain import markovChain
import json
"""
import pickle
import networkx as nx

with open('graph.pickle','rb') as file:
    G = pickle.load(file)
A = nx.adjacency_matrix(G)
A = A.toarray()
K=3
num_sample=5
labels = clustering2(A,0.9,K,2)
labels_split=[np.where(labels==i) for i in range(K)]
nodes = np.array(G.nodes())
nodes_split = [nodes[labels_split[i]] for i in range(K)]

perm = [np.random.permutation(len(nodes_split[i])) for i in range(K)]

sample = [nodes_split[i][perm[i][:num_sample]] for i in range(K)]

tweet_sample=[[] for i in range(K)]

with open('json_tweets.json','r') as file:
    data_tweet = json.load(file)

for k in range(K):
    for i in range(len(data_tweet)):
        user = data_tweet[i]['user_id']
        twt = data_tweet[i]['tweet_text']
        if user in sample[k]:
            tweet_sample[k].append(twt)

G_i=[G.subgraph(nodes_split[i]) for i in range(K)]
A_i=[nx.adjacency_matrix(G_i[i]).toarray() for i in range(K)]
in_degrees = [np.sum(A_i[i],axis=0).reshape(-1) for i in range(K)]
most_seen = [np.array(G_i[i].nodes())[np.argsort(in_degrees[i])[-10:]] for i in range(K)]
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
                most_seen_dict[k][j]['user_id']=userla

        
"""
def clustering(A,K):
    # basé sur l'artcle weighted noramlizes cut
    T = np.array(np.sum(A,axis=1).reshape(-1))
    T[T==0]=1
    T_12 = 1/np.sqrt(T)
    D_12 = np.diag(T_12)
    HB = (1/2)*(1-D_12@(A+A.T)@D_12)
    
    eigenValues, eigenVectors = np.linalg.eig(HB)
    idx = eigenValues.argsort()
    eigenVectors = eigenVectors[:,idx]
    
    Y = eigenVectors[:,:K-1]
    X = D_12@Y
    kmeans = KMeans(n_clusters=2).fit(X)
    
    return kmeans.labels_

def clustering2(G,alpha=0.9,K=2,n_vec=1):
    # basé sur l'article de fragkiskos mallarios
    A = nx.adjacency_matrix(G)
    A = A.toarray()

    T = np.array(np.sum(A,axis=1).reshape(-1))
    T[T==0]=1
    D_1 = np.diag(1/T)
    P = D_1@A
    
    P2=alpha*P+(1-alpha)*(1/A.shape[0])*np.ones(A.shape)
    mc = markovChain(P2)
    mc.computePi('eigen')
    Pi12 = np.sqrt(mc.pi)
    Pi_12 = 1/Pi12
    Pi12 = np.diag(Pi12)
    Pi_12 = np.diag(Pi_12)
    
    L=np.eye(*A.shape)-(1/2)*(Pi12@P@Pi_12+Pi_12@P.T@Pi12)

    eigenValues, eigenVectors = np.linalg.eig(L)
    idx = eigenValues.argsort()
    eigenVectors = eigenVectors[:,idx]
    
    X = eigenVectors[:,1:n_vec+1]
    kmeans = KMeans(n_clusters=K).fit(X)
    
    return kmeans.labels_
    
    
        
        
    
    
    
    