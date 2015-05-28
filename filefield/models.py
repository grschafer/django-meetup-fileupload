# -*- coding: utf-8 -*-
from django.db import models

# http://stackoverflow.com/a/8542030
class Upload(models.Model):
    # upload_to optional argument is appended to MEDIA_ROOT
    file = models.FileField(null=False, blank=False)
