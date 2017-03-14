import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


cur_path = os.path.split(os.path.abspath(__file__))[0]
output_fldr = 'searching/static/images'
output_dir = os.path.join(cur_path, output_fldr)
if not os.access(output_dir, os.F_OK):
    os.makedirs(output_dir)


def result_csv(filename='update_final.csv'):
    '''
    This is an auxiliary function to the plotting function
    '''

    products = pd.read_csv(filename, usecols = [1,2,3,4,5,6,7], encoding='utf-8').replace('null', 0)
    
    
    price = products.price.replace('\$','',regex=True).astype(float).astype(int)
    
    products['price'] = price
    
    products['score'] = products.rating.astype(int) * 0.1 + price * 0.1 + products.num_review.astype(int) * 0.8
    
    results = []
    for cat in products.category.unique():
        topprods = products.sort_values('score',ascending=0).groupby('category').get_group(cat)[:5]
    #    topprods2 = topprods[topprods.columns.difference(['url'])]
        results.append(topprods)
    
    result = pd.concat(results).set_index('category')
    
    
    return result
    

def plots(category, wordfile):
    '''
    Generate plots for overall view
    
    Input:
        result: dataframe reading from 'final_result.csv'
    
    Return:
        Plots
    '''

    result = result_csv()
    data = result.loc[category]
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    
    sns.barplot(x = 'price', y = 'brand_name', data=data, palette="Blues", ax=ax1)
    ax1.set_xticks([])
    
    sns.barplot(x = 'num_review', y = 'brand_name', data=data, palette="Blues", ax = ax2)
    ax2.set_xticks([])
    
    sns.barplot(x = 'rating',  y = 'brand_name', data=data, palette="Blues", ax = ax3)
    ax3.set_xticks([])

    output_path = os.path.join(output_dir, "category_summary.png")
    plt.savefig(output_path, bbox_inches='tight')
    
    
    words = pd.read_csv(wordfile, usecols=[1,9,10]).set_index('category')
    
    worddata = words.loc[category]
    
    plt.figure()
    cat = ' '.join(worddata['word'])
    wc = WordCloud(background_color = 'white', mode="RGBA", scale = 2).generate(cat)
    
    plt.imshow(wc)
    plt.axis("off")

    output_path = os.path.join(output_dir, "category_wordcloud.png")
    plt.savefig(output_path, bbox_inches='tight')

#    plt.show()


def find_products(args_from_ui):
    '''
    This function is used to read-in the stored product information and provide
    corresponding information as is required by the input dictionary.
    
    Inputs:
        query_d: a dictionary, containing requirement of the query
        focus: a string, indicating the main consideration of the user
    Returns:
        rv: a list of lists, whose first row contains column names and the rest
            rows contain required product information
    '''
    file_name = ''
    
    if args_from_ui['focus'] == 'Average Rating':
        file_name = 'rating_top5.csv'
    elif args_from_ui['focus'] == 'Price':
        file_name = 'price_top5.csv'
    else:
        file_name = 'num_review_top5.csv'
    
    df = pd.read_csv(file_name, usecols=range(1,11), dtype={'rating':np.float,'num_review':np.int,'score':np.float,'similarity_score':np.float, 'dfidf':np.float})
    df = df.round({'rating':1, 'score': 6, 'similarity_score':6, 'dfidf':6})
    headers = list(df)

    df = df[df['category'] == args_from_ui['category']]
    data = df.values.tolist()
    
    plots(args_from_ui['category'], file_name)
    
    return headers, data

