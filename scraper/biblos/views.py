from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse



def dashboard(request):
    
    # add list of already fetched persons' articles 
    
    return render(request, 'biblos/dashboard.html',dict())

def search(request):
    # page for results, there will be an button to redirect to main page
    
    if request.method == 'POST':
        # loading page and redirecting or task in the background
        print(request)
        
    return render(request, 'biblos/search.html')