#-*- coding: utf-8 -*-
from django import forms


class UploadVideoForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
