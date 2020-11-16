from django.core.exceptions import *
from django.db import *
from django.test import TestCase
from django.utils import timezone
from .models import *
from .scrapers import *

# Create your tests here.

class AuthorModelTests(TestCase):
    
    def test_no_arguments_raises_exception(self):
        """
        A new Author instance with no arguments should raise an IntegrityError
        exception
        """
        with self.assertRaises(IntegrityError):
            Author.objects.create()
    
    def test_null_name_raises_exception(self):
        """
        An Author instance with a null name should raise an IntegrityError
        exception
        """
        with self.assertRaises(IntegrityError):
            Author.objects.create(name=None)
class ArticleModelTests(TestCase):

    def test_no_arguments_raises_exception(self):
        """
        A new Article instance with no arguments should raise an IntegrityError
        exception
        """
        with self.assertRaises(IntegrityError):
            Article.objects.create()
    
class ScrapersModuleTests(TestCase):

    def test_no_duplicates_created(self):
        """
        create_article() shouldn't create duplicate articles, a duplicate being
        another article with the same headline inside the same newspaper
        """
        newspaper = Newspaper.objects.create(newspaper_name="Newspaper")
        create_article(newspaper,"HEADLINE","CATEGORY",None,timezone.now(),"")
        create_article(newspaper,"HEADLINE","CATEGORY2",None,timezone.now(),"")
        self.assertEqual(Article.objects.all().count(),1)