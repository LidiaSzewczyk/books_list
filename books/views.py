from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from books.models import Book


class BooksList(ListView):
    model = Book
    template_name = 'books/bookslist.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    fields = ('__all__')
    template_name = 'books/bookdetail.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookdetail', kwargs={'pk': self.object.pk})


class BookUpdateView(UpdateView):
    model = Book
    fields = ('__all__')
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookdetail', kwargs={'pk': self.object.pk})


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books:bookslist')
