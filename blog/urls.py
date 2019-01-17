from django.contrib import admin
from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path("", views.blog_home, name="blog_home"),
    path("post/<int:day>/<int:month>/<int:year>/<slug:slug>", views.post_detail, name="post_detail"),
    path("post/<int:day>/<int:month>/<int:year>/<slug:slug>/share", views.post_share, name="post_share"),
    path("post/<int:day>/<int:month>/<int:year>/<slug:slug>/download",views.post_share, name="post_download"),
    path("post/<int:day>/<int:month>/<int:year>/<slug:slug>/like", views.post_like, name="post_like")
]
