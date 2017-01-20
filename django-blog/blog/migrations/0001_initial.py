# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=500, unique=True, verbose_name='标题')),
                ('slug', models.SlugField()),
                ('content_raw', models.TextField(verbose_name='内容')),
                ('content', models.TextField(default='', blank=True, null=True, verbose_name='内容显示')),
                ('click', models.IntegerField(default=0, verbose_name='浏览次数')),
                ('hidden', models.BooleanField(default=False, verbose_name='是否隐藏')),
                ('order', models.IntegerField(default=10, verbose_name='排序')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发布日期')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='名称')),
                ('status', models.IntegerField(default=0, choices=[(0, '正常'), (1, '草稿'), (2, '删除')], verbose_name='状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'ordering': ['-update_time'],
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ForeignKey(blank=True, verbose_name='标签', to='blog.Tag'),
        ),
    ]
