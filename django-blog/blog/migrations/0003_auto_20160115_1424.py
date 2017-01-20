# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_raw',
            field=models.TextField(default='', verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
