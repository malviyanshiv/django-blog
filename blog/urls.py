from django.contrib import admin
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path("", admin.site.urls),
]
