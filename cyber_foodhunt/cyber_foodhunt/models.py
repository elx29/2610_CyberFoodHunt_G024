from django.db import models
# tables from database
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=15)

    class Meta:
        db_table = 'user'
        managed = False  # matches your exact table name in SQLite

    def __str__(self):
        return self.username

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    restaurant_name = models.TextField()
    location = models.TextField()
    opening_hours = models.TextField(null=True, blank=True)
    transport_mode = models.TextField(null=True, blank=True)
    cuisine = models.TextField(null=True, blank=True)
    is_halal = models.IntegerField(null=True, blank=True)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Restaurant'
        managed = False
        
    def __str__(self):
        return self.restaurant_name


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, db_column='restaurant_id')
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)       # stores URL or file path
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post'
        managed = False
        
    def __str__(self):
        return self.title


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    event_name = models.TextField()
    event_location = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event'
        managed = False
        
    def __str__(self):
        return self.event_name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, db_column='post_id')
    event_id = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, db_column='event_id')
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, db_column='restaurant_id')
    comment = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)       # stores URL or file path
    rating = models.IntegerField(null=True, blank=True)   # 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        managed = False

    def __str__(self):
        return f"Review {self.review_id} by User {self.user_id}"