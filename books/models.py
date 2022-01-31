from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publishedDate = models.IntegerField()
    ISBN_13 = models.CharField(max_length=13)
    pageCount = models.IntegerField()
    canonicalVolumeLink = models.CharField(max_length=200)
    language = models.CharField(max_length=5)

    def __str__(self):
        return self.title

