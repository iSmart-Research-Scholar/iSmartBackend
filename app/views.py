from urllib import response
from django.shortcuts import render,HttpResponse


# Create your views here.


def home(request):    
    return render(request,'index.html')

def search(request):
    if request.method=='POST':
        query=request.POST.get('search_query')
        return HttpResponse(query)



