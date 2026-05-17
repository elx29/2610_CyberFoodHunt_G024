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
    path('review/', views.review, name='review'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-recovery/', views.password_recovery, name='password_recovery'),
]

