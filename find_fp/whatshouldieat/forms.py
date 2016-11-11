#-*- coding: utf-8 -*-
from django import forms

from .models import WhereAreYou


class WhereAreYouForm(forms.ModelForm):
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'WHERE ARE YOU?'}))

    class Meta:
        model = WhereAreYou
        fields = ('location', )
