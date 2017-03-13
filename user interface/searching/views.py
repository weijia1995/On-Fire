from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from operator import and_
from products import find_products
from products import result_csv
from products import plots
from functools import reduce


# Create your views here.


NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
        category = 'Category',
        brand_name = 'Brand',
        name = 'Name',
        num_review = 'Number of Reviews',
        price = 'Price',
        rating = 'Rating',
        score = 'Score',
        similarity_score = 'Similarity Score',
        similarity_rank = 'Similarity Rank',
        word = 'Key Word',
        dfidf = 'TF-IDF',
        Unnamed = 'Index')


def _load_column(filename, col=0):
    """Loads single column from csv file"""
    with open(filename,"rU") as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)
    
    
def _load_res_column(filename, col=0):
    """Load column from resource directory"""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Converts a list to (value, caption) tuples"""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]


CATEGORY = _build_dropdown([None] + _load_res_column('category_list.csv'))
RATING_CRITERIA = _build_dropdown(_load_res_column('criteria_list.csv'))


class SearchForm(forms.Form):

    category = forms.ChoiceField(label='Category', choices=CATEGORY, required=True)
    focus = forms.ChoiceField(label='Main Consideration',
                                     choices=RATING_CRITERIA,
                                     required=True)
    show_args = forms.BooleanField(label='Show Searching Criteria ',
                                   required=False)


def index(request):
    context = {}
    res = None
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            args = {}
            category = form.cleaned_data['category']
            if category:
                args['category'] = category
            focus = form.cleaned_data['focus']
            if focus:
                args['focus'] = focus
                    
            if form.cleaned_data['show_args']:
                context['args'] = 'Searching Criteria for Recommendation' \
                       + json.dumps(args, indent=2)
            
            try:
                res = find_products(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_products:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()
    
    # different responses
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
        #cols = None
    else:
        columns, result = res
    
        context['result'] = result
        context['num_results'] = int(len(result)/5)
        context['columns'] = [COLUMN_NAMES.get(x, x) for x in columns]
        #context['content_analysis'] = 
        
    context['form'] = form     
    
    
        
    return render(request, 'home.html', context)


def general(request):
    context = {}
    return render(request, 'general.html', context)