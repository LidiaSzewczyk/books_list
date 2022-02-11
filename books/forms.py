from datetime import datetime
from django import forms


class FilterForm(forms.Form):
    min_year = forms.IntegerField(label='min year', required=None,
                                  max_value=int(datetime.now().strftime('%Y')))
    max_year = forms.IntegerField(label='max year', required=None, max_value=int(datetime.now().strftime('%Y')))
    select_type = forms.ChoiceField(label='',
                                    choices=(('1', 'Title'), ('2', 'Author'), ('3', 'Language'),
                                             ('4', ('All'))),
                                    widget=forms.RadioSelect, required=None)
    text_search = forms.CharField(label='', required=None)



class GoogleSearchForm(forms.Form):
    main_search = forms.CharField(label='', required=None)
    select_type = forms.ChoiceField(label='if you want specify, search by:',
                                            choices=(('intitle', 'Title'), ('inauthor', 'Author'), ('inpublisher', 'Publisher'),
                                                     ('subject', 'Subject'), ('isbn', 'ISBN')),
                                            widget=forms.RadioSelect, required=None)
    detail_search = forms.CharField(label='', required=None)
    ebook = forms.ChoiceField(label='',
                                    choices=(('ebooks', 'Ebooks'), ('free-ebooks', 'Free ebooks'), ('paid-ebooks', 'Paid ebooks'),
                                             ),
                                    widget=forms.RadioSelect, required=None)


class GoogleSelectForm(forms.Form):
    searched = forms.MultipleChoiceField(label='Select books', choices=(('1','1')),
                                       widget=forms.CheckboxSelectMultiple, required=None)


