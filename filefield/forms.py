# -*- coding: utf-8 -*-
from django import forms
from filefield.models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
    # if not ModelForm
    #file = forms.FileField(
    #    label='Select a file',
    #    help_text='max. 42 megabytes'
    #)
