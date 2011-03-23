import os

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^/?$', 'playcore.views.index', name="main_index"),
    url(r'^search/?$', 'playcore.views.search', name="main_search"),
    
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'css')}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'images')}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'js')}),
)
