# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='chunk_size',
            field=models.PositiveIntegerField(default=5242880),
            preserve_default=False,
        ),
    ]
