from django.urls import path
from . import views


urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("new/", views.event_create, name="event_create"),
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("search/", views.search, name="search"),
    path("home/", views.home, name="home"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path("restaurant/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("review/<int:restaurant_id>/", views.review_create, name="review_create"),
    path("review/", views.review_create, name="review_create_blank"),
    path("review/submit/", views.review_submit, name="review_submit"),
]

