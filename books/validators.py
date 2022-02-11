from django.core.exceptions import ValidationError


def validate_isnumeric(value):
    if not value.isnumeric() and value != '-':
        raise ValidationError('Incorrect data, it should be a number.')


def validate_not_numeric(value):
    if value.isnumeric():
        raise ValidationError('Incorrect data, it is not a number.')


def validate_is_in_db(value):
    from books.models import Book
    if len(Book.objects.filter(google_id=value)) > 0:
        raise ValidationError('This book is already in db')


