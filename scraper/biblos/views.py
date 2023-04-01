from django.shortcuts import render, redirect
from .scraper.scraper import get_articles_by_person, extract_data
# Create your views here.
from .models import *

from django.http import HttpResponse


def dashboard(request):

    # add list of already fetched persons' articles

    return render(request, 'biblos/dashboard.html', dict())

# change name to results


def search(request):
    # page for results, there will be an button to redirect to main page

    if request.method == 'POST':
        author = request.POST.get('author')
        raw_articles = get_articles_by_person(author)
        articles = extract_data(raw_articles)

        for article in articles:

            query_name = [n for n in article.authors if author in n]

            if Author.objects.filter(name=query_name).exists():
                author_object = Author.objects.filter(name=query_name[0])
            else:
                author_object = Author.objects.create(name=query_name[0])

            # concatenate exteranal authors with pk 
            Article.objects.create(
                author=author_object, title=article.title, release_data=article.release_data, typ=article.typ, series=article.series,points=article.points)

        context = {"articles": articles}

    return render(request, 'biblos/search.html', context=context)


# view for certain person data
