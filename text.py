from wordcloud import WordCloud
from pprint import pprint
import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from collections import Counter

#exclude = ['love', 'like', 'good', 'really', 'even', 'skin', 'foundation', 'look', 'face', 'great', 'looks', 'use', 'also','would','tried','makeup','well', 'time']

stopwords = stopwords.words('english')
stopwords.append("verse")
stopwords.append("chorus")
stopwords.append("choru") 
#stopwords += exclude  

with open('2000comments.txt', 'r', encoding="utf-8") as f:
    lines = ''
    for line in f:
#        print(line.strip().lower())
#        if len(line) > 1:
        lines += line.strip().lower()
        for s in string.punctuation:
            lines = lines.replace(s, ' ')



# defining a couple of helper functions
def clean(sting):
    char_to_rem = ["\n", "'", ",", "]", "[", ")", "("]

    for c in char_to_rem:
        sting = sting.replace(c, "")

    final_sting = []

    for word in sting.split(' '):
        word = word.lower()
#        if word == "fag" or word == "ho" or word == "hoe" or word == "ass":
#            final_sting.append(word)
#            continue
#            
        if len(word) > 3 and word not in stopwords:
            final_sting.append(word)

    return final_sting


words = {}

clean_text_list = clean(lines)

frequent = list(Counter(clean_text_list).most_common(20))

#stemmer = PorterStemmer()
#
#def stem_tokens(tokens, stemmer):
#    stemmed = []
#    for item in tokens:
#        stemmed.append(stemmer.stem(item))
#    return stemmed
#
#tokens = stem_tokens(clean_text_list, stemmer)

#        
#for word in clean_text_list:
#    if word in words:
#        words[word] = words[word] + 1
#    else:
#        words[word] = 1
#             
#
#
#for key, val in sorted(words.items(), key = lambda tup: (tup[1], tup[0]), reverse=True)[:20]:
#     print ("\t", key, "used", val, "times")
#     print ("\n\n")
#
#
#
#
#
#











