from django.shortcuts import render, redirect
from .scraper.scraper import get_articles_by_person, extract_data
# Create your views here.
from .models import *

from django.http import HttpResponse


def dashboard(request):

    # add list of already fetched persons' articles
    
    authors = Author.objects.all()
    
    dict = {}
    
    for author in authors:
        articles = Article.objects.filter(author=author, points__gt=0)
        points = 0
        for article in articles:
            points+=article.points
        dict.update({ author : points })

    return render(request, 'biblos/dashboard.html', context={'dict' : dict})


# change name to results
def search(request):

    if request.method == 'POST':
        author = request.POST.get('author')
        raw_articles = get_articles_by_person(author)
        articles = extract_data(raw_articles)

        for article in articles:

            query_name = [n for n in article.authors if author in n][0].strip().split(',')[0]

            if Author.objects.filter(name__startswith=query_name).exists():
                author_object = Author.objects.filter(name=query_name).first()
            else:
                author_object = Author.objects.create(name=query_name)

            # concatenate exteranal authors with pk
            Article.objects.get_or_create(
                author=author_object, authors=";".join(article.authors), ext_authors=";".join(article.ext_authors), title=article.title, release_data=article.release_data, typ=article.typ, series=article.series, points=article.points)

        context = {"articles": articles}

    return render(request, 'biblos/search.html', context=context)


# view for certain person data
def author_view(request, id):
    
    author = Author.objects.filter(id=id).first()
        
    articles = Article.objects.filter(author=author, points__gt=0)
    points = 0
    for article in articles:
        points+=article.points
    context = dict({ "author" : author, "articles":articles, "points": points })

    return render(request, 'biblos/author_view.html', context=context)

