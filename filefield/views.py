from django.shortcuts import render
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from filefield.forms import UploadForm
from filefield.models import Upload

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('filefield.views.upload'))
    else:
        form = UploadForm() # A empty, unbound form
    return TemplateResponse(request, 'filefield/upload.html', {'form': form})

