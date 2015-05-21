from django.template.response import TemplateResponse

def upload(request):
    if request.method == "POST":
        import ipdb; ipdb.set_trace()
        return TemplateResponse(request, 'upload.html')
    else:
        return TemplateResponse(request, 'upload.html')
