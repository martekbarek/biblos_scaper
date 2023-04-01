from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length = 200, blank=True, null=True, unique = True)
    
    class Meta:
        db_table = 'author'

class Article(models.Model):

    # searched author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    title = models.CharField(max_length = 200, unique = True)
    authors = models.CharField(max_length = 200, blank=True, null=True)
    ext_authors = models.CharField(max_length = 200, blank=True, null=True)
    typ = models.CharField(max_length = 200, blank=True, null=True)
    series = models.CharField(max_length = 200, blank=True, null=True)
    release_data = models.CharField(max_length = 200, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    mnisw_list = models.CharField(max_length = 200, blank=True, null=True)
    impact = models.CharField(max_length = 200, blank=True, null=True)
    
    
    class Meta:
        db_table = 'article'
        
        
    
    