from django.contrib import admin
from .models import Bookmark, Event, Restaurant, User, Post, Review 

admin.site.register(Bookmark)
admin.site.register(Event)
admin.site.register(Restaurant)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Review)