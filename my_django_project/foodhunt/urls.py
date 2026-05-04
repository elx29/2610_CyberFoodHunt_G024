from django.urls import path
from . import views


urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("new/", views.event_create, name="event_create"),
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("search/", views.search, name="search"),

]

