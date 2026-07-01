from django.contrib import admin
from .models import Bookmark, Event, Restaurant, User, Post, Review 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ["user_id", "username", "email"]
    search_fields = ["username", "email"]

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display  = ["restaurant_id", "restaurant_name", "location", "cuisine", "is_halal"]
    list_filter   = ["is_halal", "cuisine"]
    search_fields = ["restaurant_name", "location"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ["post_id", "title", "user", "restaurant", "created_at"]
    search_fields = ["title", "description"]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ["event_id", "event_name", "event_location", "start_date", "end_date", "user"]
    list_filter   = ["end_date", "start_date"]
    search_fields = ["event_name", "event_location"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ["review_id", "user", "restaurant", "rating", "created_at"]
    list_filter   = ["rating"]
    search_fields = ["user__username"]

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display  = ["bookmark_id", "user", "restaurant", "saved_at"]
    search_fields = ["user__username"]
