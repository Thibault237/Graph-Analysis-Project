# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 13:19:52 2019

@author: Philippe
"""

from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

def get_sentiment(tweet):
    blob = TextBlob(tweet, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    return blob.sentiment[0]

