# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'tag',  'content')   # 搜索功能
    list_filter = ('tag',  'pub_date')  # 添加filter侧栏
    list_display = ('title',  'tag',  'author',  'click', 'pub_date', 'update_date')  # 列表展示字段
    # fields = ('title', 'slug',  'tag', 'content')  # 页面显示字段
    fieldsets = (
        (u'基本信息', {
            'fields': ('title', 'slug',)
            }),
        (u'MarkDown格式内容', {
            'fields': ('content_raw',)
            }),
        (u'MarkDown内容显示', {
            'fields': ('content',)
            }),
        (u'其他信息', {
            'fields': ('author', 'tag',  'click', 'hidden', 'order',)
            }),

    )
    date_hierarchy = 'pub_date'  # 另外一种过滤日期的方式,先安装pytz， pip install pytz
    ordering = ['-pub_date', '-update_date']

    def save_model(self, request, obj, form, change):
        if change:  # 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)
        else:  # 新增的时候
            obj_original = None

        obj.user = request.user
        obj.save()


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',   'status', 'update_time')
    list_filter = ('update_time',)
    fields = ('name',  'status')


class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)


