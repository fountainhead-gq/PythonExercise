# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from tinymce.models import HTMLField
import mistune


STATUS = {
        0: u'正常',
        1: u'草稿',
        2: u'删除',
}


class Tag(models.Model):
    name = models.CharField(max_length=50,  unique=True, verbose_name=u'名称')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name=u'状态')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新日期')

    class Meta:
        verbose_name_plural = verbose_name = u'标签'
        ordering = ['-update_time']  # 按时间降排序

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=500, unique=True, verbose_name=u'标题')
    slug = models.SlugField(default='')
    content_raw = models.TextField(default='', verbose_name=u'内容')
    content = models.TextField(default='', null=True, blank=True, verbose_name=u'内容显示')
    # content_raw = HTMLField(verbose_name=u'内容')
    # content = HTMLField(default='', null=True, blank=True, verbose_name=u'内容显示')
    author = models.ForeignKey(User, verbose_name=u'作者')
    # tag = models.ManyToManyField('Tag', blank=True, verbose_name=u'标签')
    tag = models.ForeignKey(Tag, blank=True, verbose_name=u'标签')

    click = models.IntegerField(default=0, verbose_name=u'浏览次数')
    hidden = models.BooleanField(default=False, verbose_name=u'是否隐藏')
    order = models.IntegerField(default=10, verbose_name=u'排序')
    pub_date = models.DateTimeField('发布日期', auto_now_add=True)
    update_date = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'文章'
        ordering = ['-pub_date']

    def increase_click(self):
        Post.objects.filter(id=self.id).update(click=F('click') + 1)

    def save(self, *args, **kwargs):
        self.content = mistune.markdown(self.content_raw)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):  # __str__ on Python3
        return self.title



