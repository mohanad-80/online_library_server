from django.urls import path
from . import views

urlpatterns = [
    path("", views.getAll),
    path("add/", views.add),
    path("<int:book_id>/", views.getOne),
    path("edit/<int:book_id>/", views.edit),
    path("delete/<int:book_id>/", views.delete),
    path("search/", views.search),
    path("available/", views.getAvailable),
    path("borrow/<int:book_id>/", views.borrow),
    path("borrowed/<int:user_id>/", views.getBorrowed),
]
