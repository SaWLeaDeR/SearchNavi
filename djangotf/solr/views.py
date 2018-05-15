from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
import requests
import nltk
from nltk.tokenize import word_tokenize
import json
import re
import os
import io
import gzip
import sys
import urllib
import re
import urllib3
from bs4 import BeautifulSoup

    

# Create your views here.
def index(request):
    
    context = {'title': "SearchNavi", 'caption': "SearchNavi" }
    return render(request, 'solr/index.html', context)

def resultset(request):
    querytext = request.POST['query']
    id_list = []    
    def getPage(url):
        request = urllib.request(url)
        request.add_header('Accept-encoding', 'gzip')
        request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20')
        response = urllib3.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()
        return data

    def didYouMean(q):
        q = str(str.lower(q)).strip()
        url = "http://www.google.com/search?q=" + urllib.parse.quote(q)
        html = getPage(url)
        soup = BeautifulSoup(html)
        ans = soup.find('a', attrs={'class' : 'spell'})
        try:
            result = repr(ans.contents)
            result = result.replace("u'","")
            result = result.replace("/","")
            result = result.replace("<b>","")
            result = result.replace("<i>","")
            result = re.sub('[^A-Za-z0-9\s]+', '', result)
            result = re.sub(' +',' ',result)
        except AttributeError:
            result = 1
        return result

    
    #response = didYouMean(querytext)
    #print (response)
    text = word_tokenize(querytext)
    asdf = nltk.pos_tag(text)
    print(nltk.pos_tag(text))

    
    
    
    print("BURASI TEXT TAKENİZE EDİLMİŞ")
    querytextsplitted=querytext.split()
    
    a ="Django Haystack Solr facets.fields disappearing"
    
    querytextcommo = ','.join(querytextsplitted)
    
    print(querytextcommo)


    qparams = {'q': querytext, 'wt': 'json'}
    req = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ querytextcommo+'&rows=30'+'&wt=json')



    
    numFound = req.json()['response']['numFound']
    #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
    print(numFound)
    docs = req.json()['response']['docs']
    
    lst3= [item['Id'] for item in docs]
    tag_list= []
    id = ""
    print(lst3)
    print(len(lst3))
    for i in lst3:
        i = str(i)
        i = i[:-1]
        i = i[1:]
        id_list.append(i)
    print ("fatih")
    print(i)
    print(id_list)
    print(id_list[1])
    
    for ids in id_list:
        qparams2 = {'q': querytext, 'wt': 'json'}
        req2 = requests.get('http://solr:8983/solr/tags/select?indent=on&q=Id:'+ ids +'&wt=json')
    
        numFound2 = req2.json()['response']['numFound']
        #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
        print(numFound2)
        for a in range(numFound2):
            tags = req2.json()['response']['docs'][a]['Tag']
            z = str(tags)
            z = z[:-2]
            z = z[2:]
            if z not in tag_list:
                tag_list.append(z)
            print(tags)
        print("innerfor")  
    print("id finished")
    print(tag_list)
    req4 = requests.get('http://solr:8983/solr/searchnavi/select?facet.field=Body&facet.query=Body:'+'django'+'&facet=on&q=Title:python'+ querytextcommo+'&rows=30'+'&wt=json')
    facet = req4.json()['facet_counts']['facet_fields']['Body']
    print(facet)
    print("FACET BURASIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    
    context = {'numFound': numFound, 'docs' : docs ,'lst3' : lst3 ,'tags' : tags ,'numFound2': numFound2 , 'tag_list' : tag_list ,'a' : a} 

    return render(request, 'solr/resultset.html', context)
def searchtree(request):
    context = {'title': "SearchNavi", 'caption': "SearchNavi" }
    return render(request, 'solr/searchtree.html', context)

    #django nasıl kurulur
    #nltk : django tutorial
    #django solr arat
    #solr answerlar

def resultset2(request):
    querytext = request.POST['query2']


    print("YUKARI BAX")
    

    print("Burası 2. fonksiyon hayırlı olsun  ASDASFAS FSF SDFS FEFRREWDWADFWEFR WERF EFEFE FAEFEFSDEDADW WEDAW")
    id_list = []

    querytextsplitted=querytext.split()
    
    
    
    querytextcommo = ','.join(querytextsplitted)


    qparams = {'q': querytext, 'wt': 'json'}
    req = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ querytextcommo+'&wt=json')
    
    

    Id = req.json()['response']['docs'][0]['Id']
    #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
    print(Id)
    print("burası docs")
    text = Id[0]
    print("burası text")
    print(text)
    print("textin sonu")
    text = str(text)
    print(text)

    req5 = requests.get('http://solr:8983/solr/answers/select?indent=on&q=ParentId:'+ text +'&wt=json')

    numFound = req5.json()['response']['numFound']
    print(numFound)
    docs = req5.json()['response']['docs']


    tag_list=[]
    
    req2 = requests.get('http://solr:8983/solr/tags/select?indent=on&q=Id:'+ text +'&wt=json')
    
    numFound2 = req2.json()['response']['numFound']
    #req2 = requests.get('http://solr:8983/solr/searchnavi/select?indent=on&q=Title:'+ req+'&wt=json')
    print(numFound2)
    for a in range(numFound2):
        tags = req2.json()['response']['docs'][a]['Tag']
        z = str(tags)
        z = z[:-2]
        z = z[2:]
        if z not in tag_list:
            tag_list.append(z)
        print(tags)
          
    print("id finished")
    print(tag_list)


    context = {'numFound': numFound, 'docs' : docs ,'Id' : Id , 'tag_list' : tag_list}
    return render(request, 'solr/resultset2.html', context)
