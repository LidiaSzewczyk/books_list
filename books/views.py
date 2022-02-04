from django.db.models import Q
from django.shortcuts import redirect
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

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'title')
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(BooksListView, self).get_context_data()

        ctx['filtering'] = self.request.GET.get('filtering', '')
        ctx['select_type'] = self.request.GET.get('type', '')
        ctx['min_y'] = self.request.GET.get('min', '')
        ctx['max_y'] = self.request.GET.get('max', '')
        ctx['ordering'] = self.request.GET.get('ordering', 'title')

        return ctx

    def get_queryset(self):
        search_text = self.request.GET.get('filtering', [])
        select_type = self.request.GET.get('type', [])
        min_y = self.request.GET.get('min', [])
        min_y = int(min_y) - 1 if min_y else min_y
        max_y = self.request.GET.get('max', [])
        max_y = int(max_y) + 1 if max_y else max_y

        title = Q(title__icontains=search_text)
        authors = Q(authors__icontains=search_text)
        language = Q(language__icontains=search_text)
        min_year = Q(publisheddate__gt=min_y)
        max_year = Q(publisheddate__lt=max_y)

        qs = super().get_queryset()
        if select_type == '1':
            qs = qs.filter(title)
        if select_type == '2':
            qs = qs.filter(authors)
        if select_type == '3':
            qs = qs.filter(language)
        if select_type == '4':
            qs = qs.filter(title | authors | language)
        if min_y:
            qs = qs.filter(min_year)
        if max_y:
            qs = qs.filter(max_year)
        return qs

    def post(self, request, *args, **kwargs):
        text_search = self.request.POST.get('text_search', '')
        select_type = self.request.POST.get('select_type', '')
        min_year = self.request.POST.get('min_year', '')
        max_year = self.request.POST.get('max_year', '')

        s_type = f'{"&type=" + select_type + "&" if select_type else "&type=4&"}'
        filtering = f'{"filtering=" + text_search + s_type if text_search else ""}'
        min_y = f'{"min=" + min_year + "&" if min_year else ""}'
        max_y = f'{"max=" + max_year + "&" if max_year else ""}'

        redirect_url = reverse('books:bookslist')
        return redirect(f'{redirect_url}?{filtering}{min_y}{max_y}')


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookslist')


class BookUpdateView(UpdateView):
    model = Book
    fields = ('__all__')
    template_name = 'books/bookcreate.html'

    def get_success_url(self):
        return reverse_lazy('books:bookslist')


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books:bookslist')
