# Generated by Django 4.0.1 on 2022-02-06 16:28

import books.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_rename_publisheddate_book_publisheddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='canonicalVolumeLink',
            field=models.URLField(blank=True, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pageCount',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[books.validators.validate_isnumeric], verbose_name='Number of pages'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisheddate',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-3000, message='Impossible year'), django.core.validators.MaxValueValidator(2023, message='Impossible year')], verbose_name='Published year'),
        ),
    ]
