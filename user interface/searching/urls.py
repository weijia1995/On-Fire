from django.conf.urls import url
from django.contrib import admin
from searching import views
import os

cur_path = os.path.split(os.path.abspath(__file__))[0]

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^$', views.general, name='general'),
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', 
        {'document_root':os.path.join(cur_path, 'static')}),
]