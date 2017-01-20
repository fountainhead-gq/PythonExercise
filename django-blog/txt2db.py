#!/usr/bin/env python
#coding:utf-8


'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.

下方是两种不同的解决方法
'''


'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djanblog.settings")

def main():
    from blog.models import Tag
    f = open('oldtext.txt')

    BlogList = []
    for line in f:
        parts = line.split('****')
        BlogList.append(Tag(name=parts[0], status=parts[1], update_time=parts[2]))

    # 以上四行 也可以用 列表解析 写成下面这样
    # BlogList = [Tag(name=line.split('****')[0], status=line.split('****')[1], update_time=line.split('****')[2]) for line in f]

    Tag.objects.bulk_create(BlogList)  # 执行一条SQL存入多条数据，速度更快

if __name__ == "__main__":
    main()
    print('Done!')

'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djanblog.settings")

import django
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def main():
    from blog.models import Tag
    f = open('oldtext.txt')
    for line in f:
        name, status, update_time = line.split('****')
        Tag.objects.create(name=name, status=status, update_time=update_time)
        # Tag.objects.get_or_create(name=name, status=status, update_time=update_time)  # 判断解决导入的数据是否重复，新建时返回 True, 存在时返回 False
    f.close()

if __name__ == "__main__":
    main()
    print('Done!')



