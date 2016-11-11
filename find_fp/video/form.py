# -*- coding: utf-8 -*-
from django import forms

from . import Video


class VideoForm(forms.ModelForm):
    CHOICES = (
        ('URL', 'url'),
        ('file','File'),
    )

    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    video_type = forms.ChoiceField(choices=CHOICES, required=True, label='Example')
    video_file = forms.TextInput(
    widget=attrs={'class': 'form-control'}),
                                        max_length=29)
    video_url = models.URLField(max_length=100)
    description = models.TextField(max_length=500)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')

    class Meta:
        model = Video
        fields = ['title', 'content', 'tags', 'status']
