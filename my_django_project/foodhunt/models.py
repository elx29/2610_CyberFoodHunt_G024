# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', models.CASCADE, blank=True, null=True)
    saved_at = models.DateTimeField(blank=True, null=True)

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
        return self.restaurant_name  # Or username for the User class

    class Meta:
        managed = True
        db_table = 'restaurant'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, models.CASCADE, blank=True, null=True)
    restaurant_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'review'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    password = models.CharField()

    class Meta:
        managed = True
        db_table = 'user'
