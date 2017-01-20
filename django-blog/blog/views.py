# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseForbidden, HttpResponse
from blog.models import Post, Tag
from django.shortcuts import get_object_or_404
import json


def archive(request):
    posts = Post.objects.filter(hidden=False).all()
    return render(request, 'archive.html', {'posts': posts, 'title': 'Archive'})


class IndexView(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        return Post.objects.filter(hidden=False).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title = ''
        context['title'] = title
        return context


class TagView(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        t = Tag.objects.get(name=self.kwargs.get('slug'))
        return Post.objects.filter(tag=t, hidden=False).all()

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.filter(status=0).order_by('update_time')
        context = super(ListView, self).get_context_data(**kwargs)
        title = self.kwargs.get('slug')
        context['tag'] = Tag.objects.get(name=title)
        context['title'] = title
        return context


class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_url(request):
        return


    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        current = self.object
        current.increase_click()

        try:
            next_post = current.get_next_by_pub_date()
        except:
            next_post = None

        try:
            previous_post = current.get_previous_by_pub_date()
        except:
            previous_post = None

        context['next'] = next_post
        context['previous'] = previous_post
        context['title'] = current.title

        return context
