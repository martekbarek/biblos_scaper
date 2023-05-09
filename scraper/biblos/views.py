from django.shortcuts import render, redirect
from .scraper.scraper import get_articles_by_person, extract_data
from .models import *

def dashboard(request):

    authors = Author.objects.all()

    dict = {}

    for author in authors:
        articles = Article.objects.filter(author=author, points__gt=0)
        points = 0
        for article in articles:
            points += article.points
        articles_count = articles.count()
        if points > 0:
            dict.update({author: [points, articles_count]})

    return render(request, 'biblos/dashboard.html', context={'dict': dict})


def search(request):

    if request.method == 'POST':
        author = request.POST.get('author')
        try:
            raw_articles = get_articles_by_person(author)
            articles = extract_data(raw_articles)

            if not articles:
                return render(request, 'biblos/error.html', context=dict({"query": author}))


            for article in articles:
                try:
                    list_name = [
                        n for n in article.authors if author in n][0].strip().split(',')
                    surname = list_name[0]
                    name = list_name[1].strip()[0]
                    query_name = surname + " " + name
                except:
                    continue

                if Author.objects.filter(name__startswith=query_name).exists():
                    author_object = Author.objects.filter(
                        name=query_name).first()
                else:
                    author_object = Author.objects.create(name=query_name)

                if not Article.objects.filter(title=article.title, author=author_object).exists():
                    Article.objects.create(author=author_object, authors=";".join(article.authors), ext_authors=";".join(
                        article.ext_authors), title=article.title, release_date=article.release_date, typ=article.typ, series=article.series, points=article.points)

            context = {"articles": articles}
        except:
            return render(request, 'biblos/error.html', context=dict({"query": author}))

    return render(request, 'biblos/search.html', context=context)


def author_view(request, id):

    author = Author.objects.filter(id=id).first()

    articles = Article.objects.filter(author=author, points__gt=0)
    points = 0
    new_points = 0
    for article in articles:
        if article.release_date:
            if int(article.release_date)>=2019:
                new_points += article.points
            else:
                points += article.points
        else:
            points += article.points
            
    context = dict({"author": author, "articles": articles, "points": points, "new_points": new_points})

    return render(request, 'biblos/author_view.html', context=context)


def delete_articles_by_author(request, id):

    Author.objects.filter(id=id).first().delete()

    return redirect("/")
