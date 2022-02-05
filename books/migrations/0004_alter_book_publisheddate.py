# Generated by Django 4.0.1 on 2022-02-04 13:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_publisheddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishedDate',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(-3000, message='Impossible year'), django.core.validators.MaxValueValidator(2023, message='Impossible year za duży')]),
        ),
    ]