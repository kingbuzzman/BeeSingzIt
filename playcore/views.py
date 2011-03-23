from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from datetime import datetime

from playcore.forms import TrackForm

import json
import math, urllib

def index(request):
    return search(request)

def search(request):
    data = {
        'error': True,
        'message': 'Please submit a valid request',
        'data': None
    }
    
    # valid request
    if request.method == "POST":
        seach_form = TrackForm(request.POST)
    else:
        seach_form = TrackForm(request.GET)
        
    # validate valid form
    if seach_form.is_valid():
        page = seach_form.cleaned_data['page']
        search = seach_form.cleaned_data['search']
        results = seach_form.get_results()
        
        # if there is only one page, worth of results - it returns '0'
        if results['total'] == '0':
            results['total'] = len(results['tracks'])
        
        try:
            pageRange = range(1, int(math.ceil(float(results["total"])/10))+1)
            pageRangeLast = pageRange[-1]
            pageRangeFall = [x for x in pageRange[::10] if x <= page][-1]
            pageRange = pageRange[(pageRangeFall-1):(pageRangeFall-1)+10]
        except IndexError:
            pageRangeLast = 0
            pageRange = []
        
        # data context
        data_context = {
            'results': results,
            'search': search,
            'page': page,
            'pagenext': (page+1),
            'pageprev': (page-1),
            'pagelast': pageRangeLast,
            'paging': pageRange
        }
        
        if request.is_ajax():
            data = {
                'error': False,
                'message': '',
                'data': render_to_string('base.listings.html', data_context)
            }
            
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data_context['csrf_token'] = csrf(request)["csrf_token"]
            return render_to_response("listings.html", data_context)
        
    # not valid
    else:
        if request.is_ajax():
            return HttpResponse(json.dumps(data), mimetype="application/json")
    
    if request.is_ajax():
        return HttpResponse(json.dumps(data), mimetype="application/json")
    else:
        return render_to_response("listings.html", {
            'csrf_token': csrf(request)["csrf_token"],
            'page': 1
        })