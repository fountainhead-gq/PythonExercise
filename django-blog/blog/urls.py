from django.conf.urls import patterns, url,include
from blog.views import IndexView, TagView, PostView
from django.contrib import admin

urlpatterns = patterns(
    'blog.views',
    url(r'^$', IndexView.as_view(), {'page': 1}, name='index'),

    url(r'^archive/$', 'archive', name='archive'),
    url(r'^posts/(?P<slug>.*?)/$', PostView.as_view(), name='post'),
    url(r'^page/(?P<page>\d+)/$', IndexView.as_view(), name='index'),
    url(
        r'^tag/(?P<slug>.*?)/page/(?P<page>\d+)/$',
        TagView.as_view(),
        name='tag'
    ),
    url(r'^tag/(?P<slug>.*?)/$', TagView.as_view(), name='tag'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^new/$', 'editor', name='new_post'),
    #url(r'^edit/(?P<slug>.*?)/$', 'editor', name='edit_post'),
    #url(r'^feed/$', 'feed', name='feed'),

)
