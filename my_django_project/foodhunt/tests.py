from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from foodhunt.models import Restaurant

class RestaurantModelTest(TestCase):
    def test_create_restaurant_with_image(self):
        # Create a dummy image file for testing
        test_image = SimpleUploadedFile(
            name='test_restaurant.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )

        restaurant = Restaurant.objects.create(
            restaurant_name="Test Tasty Spot",
            location="MMU Cyberjaya Gate B",
            cuisine="Western",
            min_price=10,
            max_price=20,
            image=test_image
        )

        # Retrieve the restaurant from the database
        db_restaurant = Restaurant.objects.get(restaurant_id=restaurant.restaurant_id)

        # Assertions
        self.assertEqual(db_restaurant.restaurant_name, "Test Tasty Spot")
        self.assertTrue(db_restaurant.image.name.startswith("restaurant_images/test_restaurant"))
        self.assertTrue(db_restaurant.image.url.startswith("/media/restaurant_images/test_restaurant"))

    def test_restaurant_detail_average_rating(self):
        from foodhunt.models import Review, User
        import django.utils.timezone as timezone
        
        restaurant = Restaurant.objects.create(
            restaurant_name="Star Spot",
            location="MMU Gate A"
        )
        
        user1 = User.objects.create(username="alice", email="alice@test.com", password="pwd")
        user2 = User.objects.create(username="bob", email="bob@test.com", password="pwd")

        # Create two reviews: one with rating 5, one with rating 3. (Average = 4.0)
        Review.objects.create(user=user1, restaurant=restaurant, rating=5, comment="Amazing!", created_at=timezone.now())
        Review.objects.create(user=user2, restaurant=restaurant, rating=3, comment="Good", created_at=timezone.now())

        # Call the restaurant_detail view
        from django.test import Client
        client = Client()
        response = client.get(f'/restaurant/{restaurant.restaurant_id}/')

        # Assert average_rating in context is exactly 4.0
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['average_rating'], 4.0)
