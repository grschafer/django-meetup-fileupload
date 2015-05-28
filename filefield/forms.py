# -*- coding: utf-8 -*-
from django import forms
from filefield.models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'

