from turtle import title
from urllib import response
from django.shortcuts import render,HttpResponse
from scripts.searcher import searcher 
from django.http import JsonResponse
from scripts import ranking

# Create your views here.
se=searcher()

def home(request):    
    return render(request,'index.html')

def search(request):
    if request.method=='POST':
        query=request.POST.get('search_query')
        title=request.POST.get('title')
        author=request.POST.get('author')
        result=se.searchIEEE(query,title,author)
        return JsonResponse(result, safe=False)

