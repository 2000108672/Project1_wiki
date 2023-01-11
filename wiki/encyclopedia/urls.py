from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("create", views.create_entry, name="create"),
    path("search", views.search_entry, name="search"),
    path("random", views.random_entry, name="random"),
    path("edit/<title>", views.edit_entry, name="edit"),
]
