from datetime import datetime
from django.core.validators import MaxValueValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.db import models

from books.validators import validate_isnumeric, validate_not_numeric, validate_is_in_db


class Book(models.Model):
    title = models.CharField(max_length=1000)
    authors = models.CharField(max_length=500, blank=True, null=True)
    publisheddate = models.IntegerField(verbose_name='Published year',
                                        validators=[MinValueValidator(-3000, message='Impossible year'),
                                                    MaxValueValidator(int(datetime.now().strftime('%Y')) + 1,
                                                                      message='Impossible year')],
                                        null=True, blank=True)
    ISBN_10 = models.CharField(max_length=10, blank=True, null=True,
                               validators=[MinLengthValidator(10, message='Incorrect data - 10 characters are needed.'),
                                           MaxLengthValidator(10,
                                                              message='Incorrect data - 10 characters are needed.')])
    ISBN_13 = models.CharField(max_length=13, blank=True, null=True,
                               validators=[MinLengthValidator(13, message='Incorrect data - 13 characters are needed.'),
                                           MaxLengthValidator(13, message='Incorrect data - 13 characters are needed.')]
                               )
    pageCount = models.CharField(verbose_name='Number of pages', max_length=6, validators=[validate_isnumeric],
                                 blank=True, null=True)
    canonicalVolumeLink = models.URLField(verbose_name='Link', null=True, blank=True)
    language = models.CharField(validators=[validate_not_numeric], max_length=20, null=True, blank=True)
    google_id = models.CharField(max_length=20, validators=[validate_is_in_db], null=True, blank=True)


    def __str__(self):
        return self.title
