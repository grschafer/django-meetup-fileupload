from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from chunked.models import Upload, Chunk
import io


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT'])
def upload(request):
    filename = request.GET.get('filename', None)
    if request.method == 'GET':
        upload = Upload.objects.get(file=filename)
        needed_chunks = set(range(upload.num_chunks)) - set(chunk.index for chunk in upload.chunks.all())
        return JsonResponse({'missing_chunks': list(needed_chunks)})

    elif request.method == 'POST':
        # NOTE: Should be PUT request, but putting this under POST
        # becaues django doesn't parse multipart data in a PUT
        # Should use rest-framework or similar to make this better
        if request.POST.get('index'):
            upload = Upload.objects.get(file=filename)
            write_file_piece(request, upload)
            return JsonResponse({'status': 'success'})

        else:
            num_chunks = int(request.POST['num_chunks'])
            filesize = int(request.POST['filesize'])
            chunk_size = int(request.POST['chunk_size'])
            upload = Upload.objects.create(
                    file=filename,
                    num_chunks=num_chunks,
                    filesize=filesize,
                    chunk_size=chunk_size,
                    )
            with io.FileIO(upload.file.path, 'wb') as fout:
                fout.truncate(filesize)
            return JsonResponse({'status': 'success'})

def write_file_piece(request, upload):
    # TODO: use a form, to not need int() casting
    index = int(request.POST['index'])
    size = int(request.POST['size'])
    offset = index * upload.chunk_size
    print(request.POST, 'writing chunk', index, 'of size', size, 'at offset', offset)
    fin = request.FILES['file']
    with io.FileIO(upload.file.path, 'r+b') as fout:
        fout.seek(offset)

        for piece in fin.chunks():
            fout.write(piece)

    chunk = Chunk.objects.create(
            upload=upload,
            index=index,
            size=size,
            )


