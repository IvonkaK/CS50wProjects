from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki_entry, name="wiki"),
    path("newPage", views.create_new_page, name="newPage"),
    path("randomPage", views.random_page, name="randomPage"),
    path("<str:title>/editEntry", views.edit_entry, name="editEntry")
]
