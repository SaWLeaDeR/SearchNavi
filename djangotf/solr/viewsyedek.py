from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
import requests
import nltk
import json
import re

    

# Create your views here.
def index(request):
    
    context = {'title': "SearchNavi", 'caption': "SearchNavi" }
    return render(request, 'solr/index.html', context)

def resultset(request):
    querytext = request.POST['query']
    my_list = []


    qparams = {'q': querytext, 'wt': 'json'}
    req = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ querytext+'&wt=json')
    
    numFound = req.json()['response']['numFound']
    #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
    print(numFound)
    docs = req.json()['response']['docs']
    
    lst3= [item['Id'] for item in docs]
    
    id = ""
    print(lst3)
    print(len(lst3))
    for i in lst3:
        i = str(i)
        i = i[:-1]
        i = i[1:]
        my_list.append(i)
    print ("fatih")
    print(i)
    print(my_list)
    for t in my_list:
        qparams2 = {'q': querytext, 'wt': 'json'}
        req2 = requests.get('http://solr:8983/solr/tags/select?indent=on&q=Id:'+ t +'&wt=json')
    
        numFound2 = req2.json()['response']['numFound']
    #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
        print(numFound2)
        tags = req2.json()['response']['docs']
        print(tags)
    
    
    
    
    context = {'numFound': numFound, 'docs' : docs ,'lst3' : lst3 ,'tags' : tags ,'numFound2': numFound2}

    return render(request, 'solr/resultset.html', context)
def searchtree(request):
    context = {'title': "SearchNavi", 'caption': "SearchNavi" }
    return render(request, 'solr/searchtree.html', context)

    #django nasıl kurulur
    #nltk : django tutorial
    #django solr arat
    #solr answerlar
