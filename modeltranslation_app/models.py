from django.db import models
from django.conf import settings


# Create your models here.

def default_language_dict ():
    # check languages array in settings.py and return dict with default language
    return {lang[0]: '' for lang in settings.LANGUAGES}


class Article(models.Model):
    title = models.JSONField('Article title', default=default_language_dict)

    def __str__(self):
        return self.title.get(settings.DEFAULT_LANGUAGE)

class Blog(models.Model):
    blog_title = models.JSONField('Blog title', default=default_language_dict)
    description = models.JSONField('Article Description', default=default_language_dict, blank=True, null=True)
    author = models.CharField('Author', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.blog_title.get(settings.DEFAULT_LANGUAGE)