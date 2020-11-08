from django.db import models

# Create your models here.

class Newspaper(models.Model):
    """
    # Newspaper
    A newspaper class all articles belonging to this newspaper
    point to

    ## Fields:
    newspaper_name: A CharField of max_length=50
    """

    newspaper_name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.newspaper_name

class Author(models.Model):

    name = models.CharField(max_length=100,default="")

    def __str__(self) -> str:
        return self.name

class Article(models.Model):
    """
    # Article
    An article class with various relevant info

    ## Fields:
    - newspaper: a Newspaper instance
    - headline: a CharField of max_length=200
    - author: an Author instance
    - category: a Charfield of max_length=50
    - pub_day: a DateField
    - link: an URLField
    """
    newspaper = models.ForeignKey(Newspaper,on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.CharField(max_length=50)
    pub_day = models.DateField()
    link = models.URLField()

    def __str__(self) -> str:
        return self.headline