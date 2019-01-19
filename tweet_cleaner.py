# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 09:32:30 2018

@author: Philippe
"""

import json
import re

with open('json_tweets.json') as file:
    data = json.load(file)

# tweets to test the functions
tweet1 = data[3]['tweet_text']
tweet2 = data[5]['tweet_text']
tweet3 = data[7]['tweet_text']
tweet4 = data[9]['tweet_text']
tweet5 = data[11]['tweet_text']

def clean_composed_hashtags(txt):
    def fixup_composed_hashtags(m):
        L = re.findall('[A-Z][a-z0-9éèàùô]+',m.group())
        result = ''
        for string in L:
            result+= ' '+string
        return result.strip()
    
    return re.sub('#(?:[A-Z][a-zéèàùô]+)+',fixup_composed_hashtags,txt)

def clean_tweet_total(txt):
    txt = re.sub('http\S+','',txt)
    txt = clean_composed_hashtags(txt)
    txt = txt.replace('#','')
    txt = re.sub('\W',' ',txt)
    txt = re.sub('\s+',' ',txt)
    txt = txt.strip()
    txt = txt.lower()
    return txt
                      
                      