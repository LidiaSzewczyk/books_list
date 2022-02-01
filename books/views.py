from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from books.forms import FilterForm
from books.models import Book


class BooksListView(FormMixin, ListView):
    model = Book
    template_name = 'books/bookslist.html'
    context_object_name = 'books'
    paginate_by = 4
    ordering = ['title']
    form_class = FilterForm

    # def get_ordering(self):
    #     ordering = self.request.GET.get('ordering', 'authors')
    #     return ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        print(self.request.GET.get('filtering', []))
        print(20*'*')
        ctx = super(BooksListView, self).get_context_data()
        # ctx['title'] = Book.objects.all()
        # ctx['author'] = self.request.GET.get('ordering', 'title')
        ctx['filtering'] = self.request.GET.get('filtering', [])
        print('ctx', ctx)
        return ctx
    #
    def get_queryset(self):
        filters = self.request.GET.get('filtering',[])
        print('filters', filters)
        qs = super().get_queryset()
        if filters and filters != '[]':
            print(filters)
            qs = qs.filter(title__contains=filters)

        print('qs', qs)
        return qs

    def post(self, request, *args, **kwargs ):
        cats = self.request.POST.get('title', [])
        print('cats',cats)
        redirect_url = reverse('books:bookslist')
        return redirect(f'{redirect_url}?filtering={cats}')

# class BookDetailView(DetailView):
#     model = Book
#     fields = ('__all__')
#     template_name = 'books/bookdetail.html'
#     context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookslist')
        # return reverse_lazy('books:bookslist', kwargs={'pk': self.object.pk})


class BookUpdateView(UpdateView):
    model = Book
    fields = ('__all__')
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookslist')
        # return reverse_lazy('books:bookslist', kwargs={'pk': self.object.pk})


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books:bookslist')
