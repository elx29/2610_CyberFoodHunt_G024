from django.urls import path
from . import views


urlpatterns = [
   
#home & search
    path("search/", views.search, name="search"),
    path("home/", views.home, name="home"),
#user management
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-recovery/', views.password_recovery, name='password_recovery'),
    path("userprofile/", views.userprofile, name="userprofile"),
    path('register/', views.register, name='register'),
#event and foodspot
    path("", views.event_list, name="event_list"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("event/new/", views.event_create, name="event_create"),
    path("event/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("foodspot/create/", views.foodspot_create, name="foodspot_create"),
    path("restaurant/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurant/<int:restaurant_id>/edit/", views.restaurant_edit, name="restaurant_edit"),
    path("restaurant/<int:restaurant_id>/delete/", views.restaurant_delete, name="restaurant_delete"),
    path("restaurant/<int:restaurant_id>/vote/<str:vote_type>/", views.restaurant_vote_toggle, name="restaurant_vote_toggle"),
#review
    path("review/restaurant/<int:restaurant_id>/", views.review_create, name="review_create"),
    path("review/submit/", views.review_submit, name="review_submit"),
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),

#bookmarks
    path("bookmarks/", views.bookmark_list, name="bookmark_list"),
    path("restaurant/<int:restaurant_id>/bookmark/", views.bookmark_toggle, name="bookmark_toggle"),
]

