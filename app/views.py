from urllib import response
from django.shortcuts import render,HttpResponse
from scripts.searcher import searcher 
from django.http import JsonResponse
from scripts import ranking
import requests,environ,re

se = searcher()

# Create your views here.

def home(request):    
    return render(request,'index.html')

def search(request):
    if request.method=='GET':
        query=request.GET.get('search_query')
        title=request.GET.get('title')
        author=request.GET.get('author')
        if query is None:
            query = ''
        if title is None:
            title = ''
        if author is None:
            author = ''
        result=se.searchIEEE(query,title,author)
        return JsonResponse(result, safe=False)

