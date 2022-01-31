from django.shortcuts import render
from django.views.generic import TemplateView


class BooksList(TemplateView):
    template_name = 'books/bookslist.html'
