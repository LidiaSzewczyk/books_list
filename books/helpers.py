from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    page_size = 10


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


def take_from_form(form):
    main_search = '+'.join(form.cleaned_data.get('main_search', '').lower().split())
    select_type = form.cleaned_data.get('select_type', '')
    detail_search = '+'.join(form.cleaned_data.get('detail_search', '').lower().split())
    ebook = form.cleaned_data.get('ebook', '')

    if select_type and detail_search:
        detail_search = f'+{select_type}:{detail_search}'
    if select_type == '' and detail_search != '' and main_search != '':
        detail_search = '+' + detail_search
    if ebook:
        ebook = f'&filter={ebook}'
    search = f'{main_search}{detail_search}{ebook}'
    return search