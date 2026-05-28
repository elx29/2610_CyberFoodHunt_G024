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

    def test_is_restaurant_open_helper(self):
        from foodhunt.views import is_restaurant_open
        from datetime import datetime

        # Test 24-hour spots
        self.assertTrue(is_restaurant_open("24 Hours"))
        self.assertTrue(is_restaurant_open("24h"))
        self.assertTrue(is_restaurant_open("Open 24/7"))

        # Test empty / None values
        self.assertFalse(is_restaurant_open(""))
        self.assertFalse(is_restaurant_open(None))

        # Test dynamically built current time range to ensure it evaluates to True
        current_hour = datetime.now().hour
        start_hour = (current_hour - 1) % 24
        end_hour = (current_hour + 1) % 24

        def format_to_12hr(h):
            period = "am" if h < 12 else "pm"
            h_12 = h if h <= 12 else h - 12
            if h_12 == 0:
                h_12 = 12
            return f"{h_12:02d}:00 {period}"

        open_str = f"{format_to_12hr(start_hour)} - {format_to_12hr(end_hour)}"
        # Since it wraps the current hour, it should be open
        self.assertTrue(is_restaurant_open(open_str))

    def test_search_open_now_filter(self):
        from django.test import Client
        from datetime import datetime

        # Create one restaurant that is open and one that is closed
        current_hour = datetime.now().hour
        
        open_start = (current_hour - 1) % 24
        open_end = (current_hour + 1) % 24
        
        closed_start = (current_hour + 2) % 24
        closed_end = (current_hour + 4) % 24

        def format_to_12hr(h):
            period = "am" if h < 12 else "pm"
            h_12 = h if h <= 12 else h - 12
            if h_12 == 0:
                h_12 = 12
            return f"{h_12:02d}:00 {period}"

        open_hours = f"{format_to_12hr(open_start)} - {format_to_12hr(open_end)}"
        closed_hours = f"{format_to_12hr(closed_start)} - {format_to_12hr(closed_end)}"

        Restaurant.objects.create(
            restaurant_name="Open Burger",
            location="MMU Cyberjaya",
            opening_hours=open_hours
        )
        Restaurant.objects.create(
            restaurant_name="Closed Pizza",
            location="MMU Cyberjaya",
            opening_hours=closed_hours
        )

        client = Client()
        
        # Test without open_now parameter (should return both)
        response = client.get('/search/')
        self.assertEqual(response.status_code, 200)
        names = [r.restaurant_name for r in response.context['restaurants']]
        self.assertIn("Open Burger", names)
        self.assertIn("Closed Pizza", names)

        # Test with open_now=on parameter (should only return Open Burger)
        response_open = client.get('/search/?open_now=on')
        self.assertEqual(response_open.status_code, 200)
        open_names = [r.restaurant_name for r in response_open.context['restaurants']]
        self.assertIn("Open Burger", open_names)
        self.assertNotIn("Closed Pizza", open_names)

