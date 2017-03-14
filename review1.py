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

'''
----------------------------------------------------------------------------------------
    Helper function
----------------------------------------------------------------------------------------
'''

def get_review(review_link, pages_to_crawl):
    '''
    This is an function that takes a link for review page or a product and 
    returns customer review and rating of that product.
    Input:
        review_link: a string
    Output:
        reviews: a list of strings
        rate: a list of rating
    '''
    rv = []
    if pages_to_crawl > 100:
        pages_to_crawl = 100
    
    for i in range(pages_to_crawl):
        page_url = review_link + '&page=' + str(i+1)
        r = requests.get(page_url)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        tag_list_all = soup.find_all('div', class_ = "BVRRReviewTextContainer" )
        rate_list =  soup.find_all('span', class_='BVRRNumber BVRRRatingNumber')[3:]

        for j in range(len(tag_list_all)):
            rv.append((tag_list_all[j].text.strip(), rate_list[j].text))  
    return rv


def get_content(product_url):
    '''
    This is an auxiliary function that takes a product_url and returns description
    and comments on that page.
    Input:
        product_url: a string, representing the product page
    Output:
        a dictionary, with one key for official dessciption and one key for
        tuple of (customers' review and rating)
    '''
    # request the html
    r = requests.get(product_url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    
    # get the official description
    product_tag_list = soup.find_all('div', id='details')
    description = product_tag_list[0].text.strip()

    # get the number of pages of review
    pages_tag_list = soup.find_all('span', class_='u-linkComplexTarget')
    raw_num_review = pages_tag_list[1].text
    num_review = int(re.findall('(\n\s+)(\d+)(.*)', raw_num_review)[0][1].strip())
    num_pages = math.ceil(num_review / 5)
    # get the review page
    review_tag_list = soup.find_all('div', id='pdp-reviews')
    review_link = re.findall('(iframe src=\")(.*)(\")(.*)(\")(.*)(\")', str(review_tag_list[0]))[0][1].strip()
    reviews = get_review(review_link, num_pages)

    return description, reviews

def get_num_review(product_url):
    '''
    get the number of review of the product
    Input:
        product_url: a string, representing the product page
    Output:
        number:integer
        if has index error, return null
        a dictionary, with one key for official dessciption and one key for
        tuple of (customers' review and rating)
    '''
    # request the html
    time.sleep(2)
    r = requests.get(product_url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    # get the number of pages of review
    pages_tag_list = soup.find_all('span', class_='u-linkComplexTarget')
    try:
        raw_num_review = pages_tag_list[1].text
        num_review = int(re.findall('(\n\s+)(\d+)(.*)', raw_num_review)[0][1].strip())

    except IndexError:
        num_review = 'null'    
    return num_review


def update_num_review(filename):
    '''
    Add number of review column to the previous dataframe

    Input: csv file

    Output: csv file
    '''
    products = pd.read_csv('final.csv', usecols = [2,3,4,5,8,9])
    num_review = []
    for i in range(len(products)):
        url = products.url[i]
        num = get_num_review(url)
        num_review.append(num)
        products['num_review'] = num_review

        #dropna
        products['num_review'] = products['num_review'].replace('null',np.nan)
        products = products.dropna()    
        products.to_csv('update_final.csv')

    return products


def crawl_reveiws(result, ranking_crit):
    '''
    input top5 product dataframe and ranking_crit(price/num_review/rating)
     and crawl the reveiws of all the product in DataFrame

    Input :  
    string (price/num_review/rating)
    top5_df : dataframe

    '''

    for i in range(len(result['url'])):
        content = get_content(result['url'][i])
        des = content[0]
        reviews = ''

        for review, rate in content[1]:
            reviews += review

            if ranking_crit == 'price':
                with open('price/{}_des.txt'.format(i), 'a') as f:
                    f.write(des)
                with open('price/{}_rev.txt'.format(i), 'a') as f:
                    f.write(reviews)
            elif ranking_crit == 'num_review':
                with open('num_review/{}_des.txt'.format(i), 'a') as f:
                    f.write(des)
                with open('num_review/{}_rev.txt'.format(i), 'a') as f:
                    f.write(reviews)
            else:
                with open('rating/{}_des.txt'.format(i), 'a') as f:
                    f.write(des)
                with open('rating/{}_rev.txt'.format(i), 'a') as f:
                    f.write(reviews)
    return 


def get_dfidf(ranking_crit):
    '''
    Input the ranking criterion: price/num_review/rating and get word feature by dfidf.

    Input : string (price/num_review/rating)
    Output : the word and dfidf dataframe

    '''
    lst = []
    word_lst = []
    index_lst = []
    value_lst = []
    df_word = pd.DataFrame()
    for i in range(275):

        if ranking_crit == 'price':
            if os.path.isfile ('price/{}_rev.txt'.format(i)):
                lst.append(open('price/{}_rev.txt'.format(i)).read())
            else:
                lst.append('NaN')

        elif ranking_crit == 'num_review':
            if os.path.isfile ('num_review/{}_rev.txt'.format(i)):
                lst.append(open('num_review/{}_rev.txt'.format(i)).read())
            else:
                lst.append('NaN')
        else:
            if os.path.isfile ('rating/{}_rev.txt'.format(i)):
                lst.append(open('rating/{}_rev.txt'.format(i)).read())
            else:
                lst.append('NaN')

    df = pd.DataFrame(lst)

    #turn the training dataset into a tf-idf matrix
    stop_words = text.ENGLISH_STOP_WORDS.union(('kat', 'von','purposes','blender'))
    TFVectorizer = TfidfVectorizer(max_df = 0.5, min_df= 0, stop_words = stop_words, norm='l2')
    TFVects = TFVectorizer.fit_transform(df.iloc[:, 0])
    tfdf = pd.DataFrame(TFVects.toarray())
    tfdf

    for i in range(len(tfdf)):
        temp = np.argpartition(-tfdf.iloc[i], 5)
        result_args = temp[:5]
        #higest value
        temp = np.partition(-tfdf.iloc[i], 5)
        result = -temp[:5]

        feature_name = [TFVectorizer.get_feature_names()[x] for x in result_args]
        dic = dict(zip(feature_name, result))

        for word, dfidf in dic.items():
            index_lst.append(i)
            word_lst.append(word)
            value_lst.append(dfidf)
    df_word['index'] = index_lst
    df_word['word'] = word_lst
    df_word['dfidf'] = value_lst
    return df_word



def merge_nltk_df(ranking_crit):
    '''
    Input the ranking criterion: price/num_review/ rating
    get the final csv dataframe merge with the similarity and feature word.

    Input: 
    ranking criterion: price/num_review/ rating: string
    dfidf_frame: dataframe

    '''

    products = pd.read_csv('update_final.csv', usecols = [1,2,3,4,5,6,7], encoding='utf-8').replace('null', 0)
    price = products.price.replace('\$','',regex=True).astype(float).astype(int)
    products['total_score'] = products.rating.astype(int) + price + products.num_review.astype(int)

    if ranking_crit == 'price':
        products['score'] = (products.rating.astype(int) * 2.5 + price * 5 + products.num_review.astype(int) * 2.5)/products['total_score']
    elif ranking_crit =='num_review':
        products['score'] = (products.rating.astype(int) * 2.5 + price * 5 + products.num_review.astype(int) * 5)/products['total_score']
    else:
        products['score'] = (products.rating.astype(int) * 5 + price * 5 + products.num_review.astype(int) * 2.5)/products['total_score']

    results = []
    for cat in products.category.unique():
        topprods = products.sort_values('score',ascending=0).groupby('category').get_group(cat)[:5]
        results.append(topprods)

    #result = pd.concat(results).set_index('category')
    result = pd.concat(results).reset_index(drop = True)
    result = result.drop('total_score', 1)

    #from the top5 result dataframe, crawl the revews
    crawl_reveiws(result, ranking_crit)

    ###
    #we manually use the reveiw and description txt file into our simiparity module to get
    #'similarity_{}.txt'.format(ranking_crit)

    ##
    similarity = pd.read_csv('similarity_{}.txt'.format(ranking_crit), names = ['similarity_score'])
    result['similarity_score'] = similarity['similarity_score']

    ##merge dfidf
    result = result.reset_index()
    dfidf_df = get_dfidf(ranking_crit)
    merge_df = pd.merge(result, dfidf_df, on='index')
    df = merge_df.drop('url', 1)
    df = df.drop('index', 1)
    df.to_csv('{}_top5.csv'.format(ranking_crit))

    return

def result_csv(filename='update_final.csv'):

    products = pd.read_csv(filename, usecols = [1,2,3,4,5,6,7], encoding='utf-8').replace('null', 0)
    
    
    price = products.price.replace('\$','',regex=True).astype(float).astype(int)
    
    products['price'] = price
    
    products['score'] = products.rating.astype(int) * 0.1 + price * 0.1 + products.num_review.astype(int) * 0.8
    
    results = []
    for cat in products.category.unique():
        topprods = products.sort_values('score',ascending=0).groupby('category').get_group(cat)[:5]
        results.append(topprods)
    
    result = pd.concat(results).set_index('category')
    return result

def overallview(result):    
    '''
    Generate plots for overall view
    
    Input:
        result: dataframe reading from 'final_result.csv'
    
    Return:
        Plots
    '''

    # Plots for overall
    sns.set_palette("hls", 4)
    sns.set(style='darkgrid')
    
    # Top brands on list for all category
    plt.figure()
    plt.title('Top Brand on Board')
    topbrand = sns.countplot(y = result['brand_name'], order=result.brand_name.value_counts().iloc[:10].index)
    plt.ylabel('Brand Name')
    plt.xlabel('Number of time recommended')
    output_path = os.path.join(output_dir, "Top brand on board.png")
    plt.savefig(output_path, bbox_inches='tight')
    
    
    # Top Prouct by num_review
    plt.figure()
    plt.title('Brands with highest number of review')
    rank = result.reset_index(0).sort_values(by='num_review',ascending=False,inplace=False).iloc[:10]
    
    sns.barplot(x =rank['num_review'], y=rank['brand_name'].str.cat(rank['name'], sep=' | '), palette="BuPu")
    plt.xlabel('Mean Number of review')
    plt.ylabel('Product Name')
    output_path = os.path.join(output_dir, "Top brand on reviews.png")
    plt.savefig(output_path, bbox_inches='tight')
    
    
    # Most worth it
    plt.figure()
    plt.title('Best cost performance') 
    result['cost_performance'] = result['price']/result['rating']
    data = result.reset_index(0).sort_values(by='cost_performance',ascending=True,inplace=False).iloc[:10].reset_index(0)
    fig = sns.barplot(x =data.index, y=data['brand_name'].str.cat(data['name'], sep=' '), palette="PuRd")
    plt.xticks(fig.get_xticks(), fig.get_xticks()+1)
    plt.xlabel('Cost Performance Rank')
    plt.ylabel('Product')
    output_path = os.path.join(output_dir, "Cost Performance.png")
    plt.savefig(output_path, bbox_inches='tight')
    
    





      
