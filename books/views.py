import json
import urllib.request

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin, FormView

from books.forms import FilterForm, GoogleSearchForm, GoogleSelectForm
from books.models import Book


class BooksListView(FormMixin, ListView):
    model = Book
    template_name = 'books/bookslist.html'
    context_object_name = 'books'
    paginate_by = 10
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


def check_author(data):
    if 'authors' in data['volumeInfo']:
        return ', '.join(author for author in data['volumeInfo']['authors'])
    return ''


def check_key(data, key):
    if key in data['volumeInfo']:
        return data['volumeInfo'][key]
    return ''


def check_isbn(data, idx):
    if 'industryIdentifiers' in data['volumeInfo']:
        for element in data['volumeInfo']['industryIdentifiers']:
            if element['type'] == idx:
                return element['identifier']
    return ''


class GoogleSearchView(FormView):
    template_name = 'books/googlelist.html'
    form_class = GoogleSearchForm
    success_url = reverse_lazy('books:bookslist')
    google_api_url = 'https://www.googleapis.com/books/v1/volumes?q='

    def get_form_class(self):
        return GoogleSelectForm if self.request.session.get('data') else GoogleSearchForm

    def get_form(self, *args, **kwargs):
        data = self.request.session.get('data')
        form = super().get_form(*args, **kwargs)

        if data:
            books = []
            for item in data['items']:
                new_book = [check_key(item, 'title'), check_author(item), check_key(item, 'publishedDate')[:4],
                            check_key(item, 'language'), check_key(item, 'canonicalVolumeLink')]
                new_book = ' - '.join(new_book)
                choice = item['id'], new_book
                books.append(choice)
                form.fields['searched'].choices = books

        return form

    def form_valid(self, form):
        main_search = '+'.join(form.cleaned_data.get('main_search', '').lower().split())
        select_type = form.cleaned_data.get('select_type', '')
        detail_search = '+'.join(form.cleaned_data.get('detail_search', '').lower().split())

        if select_type and detail_search:
            detail_search = f'+{select_type}:{detail_search}'
        if select_type == '' and detail_search != '' and main_search != '':
            detail_search = '+' + detail_search
        # search = unicodedata.normalize('NFKD', f'{main_search}{detail_search}').encode('ASCII', 'ignore')
        search = f'{main_search}{detail_search}'
        print(search)

        if search:
            with urllib.request.urlopen(url=f'{self.google_api_url}{search}') as r:
                response = r.read().decode('UTF-8')
                data = json.loads(response)

            if data.get('totalItems', 0) == 0:
                messages.error(self.request, "No such book. Try again.")
                return redirect(reverse('books:googlesearch'))

            if data.get('totalItems') > 0:
                self.request.session['data'] = data
                return redirect(reverse('books:googlesearch'))

        data = self.request.session.get('data', {})
        self.request.session.clear()
        books = [book for book in data['items'] if book['id'] in form.cleaned_data.get('searched')]

        for element in books:
            if len(Book.objects.filter(google_id=element['id'])) == 0:
                Book.objects.create(title=element['volumeInfo']['title'],
                                    authors=check_author(element),
                                    publisheddate=int(check_key(element, 'publishedDate')[:4]) if check_key(element,
                                                                                                            'publishedDate') else None,
                                    ISBN_10=check_isbn(element, 'ISBN_10'),
                                    ISBN_13=check_isbn(element, 'ISBN_13'),
                                    pageCount=check_key(element, 'pageCount'),
                                    canonicalVolumeLink=check_key(element, 'canonicalVolumeLink'),
                                    language=check_key(element, 'language'),
                                    google_id=element['id'])
                messages.success(self.request, f"'{element['volumeInfo']['title']}' has been added to db")
            else:
                messages.error(self.request, f"'{element['volumeInfo']['title']}' is already in db")
        return redirect(reverse('books:bookslist'))


def delete_session(request):
    try:
        request.session.clear()
    except KeyError:
        pass
    return redirect(reverse('books:googlesearch'))


