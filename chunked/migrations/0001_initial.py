# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('index', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(upload_to='')),
                ('num_chunks', models.PositiveIntegerField()),
                ('filesize', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='chunk',
            name='upload',
            field=models.ForeignKey(to='chunked.Upload', related_name='chunks'),
        ),
    ]
