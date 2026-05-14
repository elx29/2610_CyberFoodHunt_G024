from django.db import models


class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', models.CASCADE, blank=True, null=True)
    saved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} saved {self.restaurant}"

    class Meta:
        managed = True
        db_table = 'bookmark'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    event_name = models.TextField()
    event_location = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.event_name
    
    class Meta:
        managed = True
        db_table = 'event'


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', models.CASCADE, blank=True, null=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'post'


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    restaurant_name = models.TextField()
    location = models.TextField()
    opening_hours = models.TextField(blank=True, null=True)
    transport_mode = models.TextField(blank=True, null=True)
    cuisine = models.TextField(blank=True, null=True)
    is_halal = models.IntegerField(blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)
    max_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.restaurant_name  # username for the User class

    class Meta:
        managed = True
        db_table = 'restaurant'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey('Restaurant', models.CASCADE, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} — {self.rating}★"

    class Meta:
        managed = True
        db_table = 'review'

    

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    password = models.CharField()

    def __str__(self):
        return self.username  # username for the User class
    
    class Meta:
        managed = True
        db_table = 'user'

    
