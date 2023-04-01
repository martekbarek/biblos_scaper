from django.shortcuts import render, redirect
from .scraper.scraper import get_articles_by_person, extract_data 
# Create your views here.

from django.http import HttpResponse



def dashboard(request):
    
    # add list of already fetched persons' articles 
    
    return render(request, 'biblos/dashboard.html',dict())

# change name to results
def search(request):
    # page for results, there will be an button to redirect to main page
    
    if request.method == 'POST':
        author = request.POST.get('author')
        raw_articles = get_articles_by_person(author)
        articles=extract_data(raw_articles)
        # loading page and redirecting or task in the background
        print(request)
        context = { "articles": articles }
        
    return render(request, 'biblos/search.html', context=context)


# view for certain person data