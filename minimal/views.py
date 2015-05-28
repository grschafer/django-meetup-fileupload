from django.conf import settings
from django.template.response import TemplateResponse
import os

def upload(request):
    if request.method == "POST":
        upload = request.FILES['file']
        print(type(upload))
        save_path = os.path.join(settings.MEDIA_ROOT, upload.name)
        if upload.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            os.rename(upload.temporary_file_path(), save_path)

            # use chunks() if processing the file inline (but remember it's >2.5 MB)
            # default chunk_size of 64 KB
            for chunk in upload.chunks():
                pass
        else:
            with open(save_path, 'wb') as f:
                f.write(upload.read())

        return TemplateResponse(request, 'minimal/upload.html')
    else:
        return TemplateResponse(request, 'minimal/upload.html')
