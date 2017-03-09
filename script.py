##!/usr/bin/env python3
## -*- coding: utf-8 -*-


import re
import bs4
import queue
import json
import sys
import csv
import util
import json
import urllib3
import pandas as pd
import time
import requests


myurl = 'http://www.sephora.com/'

pm = urllib3.PoolManager()
html = pm.urlopen(url=myurl, method="GET").data

soup = bs4.BeautifulSoup(html, 'lxml')
tag_list = soup.find_all('script', type="application/ld+json")



level_1 = json.loads(tag_list[1].text)
cat_url = []
for cat in range(len(level_1)):
    cat_url.append(level_1[cat]['url'])



def get_dict(category_url):
    '''
    '''
    time.sleep(5)


    #pm = urllib3.PoolManager()
    html = pm.urlopen(url=category_url, method="GET").data
    soup = bs4.BeautifulSoup(html, 'lxml')
    tag_list = soup.find_all('script', id='searchResult')
    loaded_dict = json.loads(tag_list[0].text)
    rv = loaded_dict['categories']['sub_categories']
    
    
    dic = {}
    if category_url == 'http://www.sephora.com/nails-makeup':
        for item in rv['sub_categories']:
            item_url = util.convert_if_relative_url('http://www.sephora.com/', item['seo_path'])
            dic['{}'.format(item['name'])] = item_url
    
    else:
        for i in rv:
            if 'sub_categories' in i:
                for item in i['sub_categories']:
                    item_url = util.convert_if_relative_url('http://www.sephora.com/', item['seo_path'])
                    dic['{}'.format(item['name'])] = item_url
            else:
                item_url = util.convert_if_relative_url('http://www.sephora.com/', i['seo_path'])
                dic['{}'.format(i['name'])] = item_url

    final_lst = []
    for category in dic:
        url = dic[category]
        final_lst.append([category,url]) 
    return final_lst




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
        
        
with open('dicurl.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('dicurl_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        urls = {rows[0]:rows[1] for rows in reader}
        

#def get_second_level_url(sub_category_url):
#    l = []
#    for value in dic.values():
#        l.append(get_dict(category_url))
#        
#    return l
#    
##
#def get_item(category_url):
#    '''
#    get whole products information under sub_category
#    '''
#
#    dic_url = get_dict(category_url)
#    for category in dic_url:
#        url = dic_url[category]
#        pm = urllib3.PoolManager()
#        html = pm.urlopen(url=url, method="GET").data
#        soup = bs4.BeautifulSoup(html, 'lxml')
#        tag_list = soup.find_all('script', type="application/ld+json")
#        product_lst = json.loads(tag_list[0].text)
#        
#
#        product_dic = {}
#
#        for product in product_lst:
#            tuple_product = '{}'.format(product['brand']),'{}'.format(product['name'])
#            product_dic[tuple_product] = {} 
#            product_dic[tuple_product]['price'] = product['price']
#            product_dic[tuple_product]['availability'] = product['offers']['availability']
#            product_dic[tuple_product]['url'] = product['url']
#            product_dic[tuple_product]['category'] = product['category']
#
#    return product_dic


#def get_item(urls):
#    '''
#    get whole products information under sub_category
#    '''
#
##    dic_url = get_dict(category_url)
#    for category in urls:
#        time.sleep(5)
#        url = urls[category]
#        print(url)
#        pm = urllib3.PoolManager()
#        html = pm.urlopen(url=url, method="GET").data
#        print('*******')
#        soup = bs4.BeautifulSoup(html, 'lxml')
#        tag_list = soup.find_all('script', type="application/ld+json")
#        product_lst = json.loads(tag_list[0].text)
##        print(product_lst)
#
#        product_dic = {}
#
#        for product in product_lst:
#            tuple_product = '{}'.format(product['brand']),'{}'.format(product['name'])
#            product_dic[tuple_product] = {} 
#            product_dic[tuple_product]['price'] = product['price']
#            product_dic[tuple_product]['availability'] = product['offers']['availability']
#            product_dic[tuple_product]['url'] = product['url']
#            product_dic[tuple_product]['category'] = product['category']
#        
##        print(product_dic)
#
#    return product_dic
#
#



def get_num_review(product_url):
    '''
    This is an auxiliary function that takes a product_url and returns description
    and comments on that page.
    Input:
        product_url: a string, representing the product page
    Output:
        a dictionary, with one key for official dessciption and one key for
        customers' review
    '''
    # request the html
    time.sleep(5)
    
    r = requests.get(product_url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    # get the number of pages of review
    pages_tag_list = soup.find_all('span', class_='u-linkComplexTarget')
    raw_num_review = pages_tag_list[1].text
    num_review = int(re.findall('(\n\s+)(\d+)(.*)', raw_num_review)[0][1].strip())
 
    
    return num_review



products = pd.read_csv('first1000.csv', usecols = [1,2,3,4,5,6,7]).replace('null', 0)

num_review = []
num_review2 = []
for i in range(50,1000):
    url = products.url[i]
    num = get_num_review(url)
    num_review2.append(num)
    
    


price = products.price.replace('\$','',regex=True).astype(float).astype(int)

products['score'] = products.rating.astype(int) * 0.3 + price * 0.3 + products.num_review.astype(int) * 0.4

results = []
for cat in products.category.unique():
    topprods = products.sort_values('score',ascending=0).groupby('category').get_group(cat)[:10]
    topprods2 = topprods[topprods.columns.difference(['url'])]
    results.append(topprods2)

result = pd.concat(results).set_index('category')

result.to_csv('1000result.csv')



















































