## Project setup

django-admin startproject file\_upload
cd file\_upload
django-admin startapp minimal
django-admin startapp filefield
django-admin startapp chunked


## Database Setup

python3 manage.py migrate


## To use

Run the server with `python3 manage.py runserver 0.0.0.0:8000`.

Visit /minimal/ or /filefield/ for html form-based uploading.

Run `python3 chunked/client.py <filename>` to upload a file in a chunked fashion.
