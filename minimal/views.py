from django.conf import settings
from django.template.response import TemplateResponse
import os

def upload(request):
    if request.method == "POST":
        upload = request.FILES['file']
        print(type(upload))
        tmp_path = getattr(upload, 'temporary_file_path', None)
        save_path = os.path.join(settings.MEDIA_ROOT, upload.name)
        if tmp_path:
            # os.link? Tempfile closing doesn't seem to complain that this disappeared
            os.rename(upload.temporary_file_path(), save_path)
            # use chunks() if processing the file inline (but remember it's >2.5mb)
        else:
            with open(save_path, 'wb') as f:
                for chunk in upload.chunks():
                    f.write(chunk)

        return TemplateResponse(request, 'minimal/upload.html')
    else:
        return TemplateResponse(request, 'minimal/upload.html')
