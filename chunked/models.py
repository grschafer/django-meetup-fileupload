# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Upload(models.Model):
    file = models.FileField(null=False, blank=False)
    num_chunks = models.PositiveIntegerField(null=False, blank=False)
    filesize = models.PositiveIntegerField(null=False, blank=False)
    chunk_size = models.PositiveIntegerField(null=False, blank=False)
    # TODO: status, checksum

class Chunk(models.Model):
    upload = models.ForeignKey(Upload, null=False, blank=False, related_name='chunks')
    index = models.PositiveIntegerField(null=False, blank=False)
    size = models.PositiveIntegerField(null=False, blank=False)
