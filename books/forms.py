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
