# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 12:45:36 2018

@author: Philippe
"""
import numpy as np
import json
import io
import os
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def word_model():
    PATH_TO_DATA = "C:/Users/Philippe/Desktop/Projets Deep Learning/Projet 2/nlp_project/nlp_project/data/"
    fr_model = KeyedVectors.load_word2vec_format(os.path.join(PATH_TO_DATA, 'wiki.fr.vec'))
    return fr_model

def get_idf(corpus):
    vec = TfidfVectorizer()
    X = vec.fit_transform(corpus)
    return X, vec.vocabulary_

def embed_data(data,tf_idf,vocab,model):
    L=[]
    #unique_words = list(set(words))
    for i in range(len(data)):
        result = np.zeros((300,))
        count=0
        string = data[i]
        words = string.split(' ')
        for word in words:
            try:
                word_embedding = model[word]
                word_id = vocab[word]
                tfidf=tf_idf[i,word_id]
                result+=tfidf*word_embedding
                count+=tfidf
            except KeyError:
                pass
        if count!=0:
            result=result/count
        else:
            pass
        L.append(result)
    
    return L

