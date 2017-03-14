import re
import bs4
import json
import sys
import csv
import util
import json
import urllib3
import time 
import csv
import pandas as pd
import requests
import math


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
    Match each category to its url
    
    Input: category url
    Return: list of list [category, url]

    '''
    time.sleep(5)

    r = requests.get(category_url)
    soup = bs4.BeautifulSoup(r.text, 'lxml') 
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


#
#
#l0 = get_dict(cat_url[0])
#l1 = get_dict(cat_url[1])
#l2 = get_dict(cat_url[2])
#l3 = get_dict(cat_url[3])
#l4 = get_dict(cat_url[4]) 
#l5 = get_dict(cat_url[5])
#l7 = get_dict(cat_url[7])
#l6 = get_dict(cat_url[6])
#
#list_cat_url = l0 + l1+l2+l3+l4+l5+l6+l7
#list_cat_url = [list(l) for l in (set(tuple(l) for l in list_cat_url))]
#
#ll1 = list_cat_url[:30]
#ll2 = list_cat_url[31:60]
#ll3 = list_cat_url[61:90]
#ll4 = list_cat_url[91:120]
#ll5 = list_cat_url[121:150]
#ll6 = list_cat_url[151:180]
#

#
## Build csv  
#with open("dicurl.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in list_cat_url:
#        csv_writer.writerow([k,v])
#        
#        
#        
#with open('dicurl.csv', mode='r') as infile:
#    reader = csv.reader(infile)
#    with open('dicurl_new.csv', mode='w') as outfile:
#        writer = csv.writer(outfile)
#        urls = {rows[0]:rows[1] for rows in reader}
#        
#        
#with open("d1.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll1:
#        csv_writer.writerow([k,v])     
#        
#        
#with open("d2.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll2:
#        csv_writer.writerow([k,v])
#        
#with open("d3.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll3:
#        csv_writer.writerow([k,v])        
#        
#        
#with open("d4.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll4:
#        csv_writer.writerow([k,v])
#        
#with open("d5.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll5:
#        csv_writer.writerow([k,v])        
#
#with open("d6.csv", 'w') as outfile:
#   csv_writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
#   for k,v in ll6:
#        csv_writer.writerow([k,v])


def get_one_page_products(page_url):
    '''
    Input:
        url: a string, representing url for a page
    Output:
        products: a list of dictionaries, each dictionary contains summarized
            information of a certain product on that page
        pages: an integer, representing the number of pages in this subcategory
    '''
    time.sleep(5)
    r = requests.get(page_url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    tag_list = soup.find_all('script', type='text/json')
    level_2 = json.loads(tag_list[5].text)
    products = level_2['products']
    print ('~~~~~~')
    pages = math.ceil(level_2['total_products'] / level_2['page_size'])

    tag_list2 = soup.find_all('script', type="application/ld+json")
    product2 = json.loads(tag_list2[1].text)


    
    return products, product2, pages



def get_category_products(csv_filename):
    '''
    Input:
        subcategory_url: a string, representing a url for a certain subcategory
    Output:
        rv: a list of dictionaries, each dictionary contains summarized
            information of a certain product of that subcategory
    '''
    with open(csv_filename, mode='r') as infile:
        reader = csv.reader(infile)
        with open('coors_new.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
        urls = {rows[0]:rows[1] for rows in reader}

    products_sim = []
    product2_sim = []

    for category, subcategory_url in urls.items():

        page_url1 = subcategory_url + '?currentPage=1'
        print(category)
        products, product2, pages = get_one_page_products(page_url1)
    
        if pages > 1:
            for i in range(1, pages):
                next_page_url = subcategory_url + '?currentPage=' + str(i+1)
                more_products, more_products2, pages = get_one_page_products(next_page_url)
                products += more_products
                product2 += more_products2
        
                products_sim += products
                product2_sim += product2


    df1 = pd.DataFrame(products_sim)
    df1['sku_number'] = df1['derived_sku'].apply(lambda x: x['sku_number'])
    df2 = pd.DataFrame(product2_sim)
    df2['price'] = df2['offers'].apply(lambda x: x['price'])
    df = pd.concat([df2['category'], df1['brand_name'], df2['name'], df2['price'], df1['sku_number'], \
        df1['id'], df1['rating'], df2['url']],axis = 1)
    df = df.drop(result1.columns[[0]], axis=1)
    df = df.drop_duplicates(subset=['category','id','url'], keep='first').reset_index()

    df.to_csv('final.csv')
 
    return


