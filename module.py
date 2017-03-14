import requests
import bs4
import re
import math
import time
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation
from sklearn.feature_extraction import text
import os
import similarity
import review1



#get all categories url list and use it as global variables
myurl = 'http://www.sephora.com/'

pm = urllib3.PoolManager()
html = pm.urlopen(url=myurl, method="GET").data

soup = bs4.BeautifulSoup(html, 'lxml')
tag_list = soup.find_all('script', type="application/ld+json")

level_1 = json.loads(tag_list[1].text)
cat_url = []
for cat in range(len(level_1)):
    cat_url.append(level_1[cat]['url'])

# Create csv that contains all url

# Since crawling takes too long, we seperate the whole dataset into 6 sections to run get_dict
# and manually combine all lists together
l0 = get_dict(cat_url[0])
l1 = get_dict(cat_url[1])
l2 = get_dict(cat_url[2])
l3 = get_dict(cat_url[3])
l4 = get_dict(cat_url[4]) 
l5 = get_dict(cat_url[5])
l7 = get_dict(cat_url[7])
l6 = get_dict(cat_url[6])


list_cat_url = l0 + l1+l2+l3+l4+l5+l6+l7


# Build csv  
with open("dicurl.csv", 'w') as outfile:
   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
   for k,v in list_cat_url:
        csv_writer.writerow([k,v])


#using category url to get wll products and their infotmation
get_category_products('dicurl.csv')
#update the original dataframe with number of comment
update_num_review('final.csv')
##get the final input csv file
merge_nltk_df('price')
merge_nltk_df('num_review')
merge_nltk_df('rating')

# Overall Plots
result = result_csv()
overallview(result)
