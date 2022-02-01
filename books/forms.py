from django.forms import forms, CharField, IntegerField, NumberInput


class FilterForm(forms.Form):
    title= CharField(label='Title', required=None)
    # author= CharField(label='Authors', required=None)
    # language= CharField(label='Language', required=None)
    # published = IntegerField(label='Publish date', required=None, widget=NumberInput(attrs={'type':'range', 'step': '1', 'min': '1000', 'max': '2100', 'id':'myRange'}))
