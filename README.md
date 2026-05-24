# Cyber Food Hunt

Cyber Food Hunt is a Django web application for discovering food spots and food-related events around MMU Cyberjaya and the wider Cyberjaya area. The app helps users search for restaurants, filter places by practical student needs such as budget, cuisine, halal status, and transport options, view pop-up food events, submit reviews, and track user contribution badges.

This repository currently contains a working Django project with a SQLite database, Django models, templates, sample schema/seed SQL files, and a Tailwind-powered interface.

## Project Overview

Cyber Food Hunt is designed as a community-driven food discovery platform. Instead of only listing restaurants, it focuses on the type of information students usually care about:

- Where the restaurant or event is located
- What type of cuisine is available
- Whether the place is halal
- Estimated price range
- Available transport options such as walking, shuttle, bus, or e-hailing
- Reviews and ratings from other users
- Short-term food events and pop-ups

The project is implemented using Django and follows a simple server-rendered architecture. Pages are rendered using Django templates, and the database is managed through Django models backed by SQLite during development.

## Main Features

### 1. Home / Discover Page

The home page introduces Cyber Food Hunt and highlights:

- Active food events that have not expired
- Trending or recently added restaurants
- A quick search bar for finding food spots
- Navigation to search, events, profile, and sharing pages

Main template:

```text
my_django_project/foodhunt/templates/foodhunt/main.html
```

Main view:

```text
home()
```

### 2. Restaurant Search and Filtering

Users can browse all restaurants and filter them by:

- Restaurant name
- Cuisine type
- Transport mode
- Halal-only option
- Price range

The search logic is handled in the `search()` view. Results are displayed as restaurant cards with location, transport, cuisine, halal status, and price range.

Main template:

```text
my_django_project/foodhunt/templates/foodhunt/search.html
```

Main view:

```text
search()
```

### 3. Restaurant Detail Page

Each restaurant has a detail page that shows restaurant information and related reviews. Users can navigate from a restaurant listing into the detailed view.

Main template:

```text
my_django_project/foodhunt/templates/foodhunt/restaurant_detail.html
```

Main view:

```text
restaurant_detail()
```

### 4. Reviews and Ratings

Users can create reviews for restaurants. A review can include:

- Rating
- Comment
- Optional image upload
- Associated restaurant
- User who submitted the review

At the moment, the review system uses the first user in the database as a temporary logged-in user until the authentication system is fully connected.

Main templates:

```text
my_django_project/foodhunt/templates/foodhunt/review.html
```

Main views:

```text
review_create()
review_submit()
```

### 5. Food Events / Pop-Ups

The app supports event listings for temporary food events such as bazaars, food truck rallies, and pop-up food stalls.

Users can:

- View active events
- View event details
- Create a new event
- Delete an event

Expired events are filtered out from the active event list. If a user tries to open an expired event detail page, they are redirected back to the event list.

Main templates:

```text
my_django_project/foodhunt/templates/foodhunt/event_list.html
my_django_project/foodhunt/templates/foodhunt/event_detail.html
my_django_project/foodhunt/templates/foodhunt/event_form.html
```

Main views:

```text
event_list()
event_detail()
event_create()
event_delete()
```

### 6. User Profile and Badges

The user profile page shows contribution statistics and achievement badges.

Current badge examples:

- Rookie Hunter: posted first food spot
- Food Scout: posted 5 food spots
- Cyber Hunter: posted 15 food spots
- Legend: posted 30 food spots
- Event Starter: posted first event
- Detective: posted 5 events

The current implementation calculates badges from the number of posts and events created by the user.

Main template:

```text
my_django_project/foodhunt/templates/foodhunt/userprofile.html
```

Main view:

```text
userprofile()
```

### 7. Bookmarks

The database supports bookmarking restaurants. Each bookmark connects a user to a restaurant and records when it was saved.

The database schema prevents the same user from bookmarking the same restaurant more than once.

Current model:

```text
Bookmark
```

## Technology Stack

- Python
- Django
- SQLite
- HTML
- Django Templates
- Tailwind CSS through CDN
- Google Fonts
- Material Symbols

The project was generated with Django 6.0.3 according to the settings file comments.

## Project Structure

```text
2610_CyberFoodHunt_G024/
+-- README.md
+-- .gitignore
+-- .vscode/
+-- cyber_foodhunt/
+-- my_django_project/
    +-- manage.py
    +-- db.sqlite3
    +-- schema.sql
    +-- seed.sql
    +-- cyberfoodhunt/
    |   +-- __init__.py
    |   +-- settings.py
    |   +-- urls.py
    |   +-- asgi.py
    |   +-- wsgi.py
    +-- foodhunt/
        +-- __init__.py
        +-- admin.py
        +-- apps.py
        +-- models.py
        +-- tests.py
        +-- urls.py
        +-- views.py
        +-- migrations/
        |   +-- __init__.py
        |   +-- 0001_initial.py
        +-- templates/
            +-- foodhunt/
                +-- main.html
                +-- search.html
                +-- foodspots.html
                +-- restaurant_detail.html
                +-- review.html
                +-- event_list.html
                +-- event_detail.html
                +-- event_form.html
                +-- registerevent.html
                +-- userprofile.html
                +-- bookmark.html
                +-- login.html
                +-- register.html
                +-- passwordrecovery.html
```

Note: the main active Django project appears to be inside `my_django_project/`.

## Database Models

The app defines the following main models in:

```text
my_django_project/foodhunt/models.py
```

### User

Stores basic user information:

- `user_id`
- `username`
- `email`
- `password`

Current note: this is a custom user-like model and is separate from Django's built-in authentication user model.

### Restaurant

Stores food spot information:

- `restaurant_id`
- `restaurant_name`
- `location`
- `opening_hours`
- `transport_mode`
- `cuisine`
- `is_halal`
- `min_price`
- `max_price`

### Event

Stores food event information:

- `event_id`
- `user`
- `event_name`
- `event_location`
- `description`
- `image`
- `start_date`
- `end_date`
- `created_at`

### Post

Stores user-created food posts:

- `post_id`
- `user`
- `restaurant`
- `title`
- `description`
- `image`
- `created_at`

### Review

Stores restaurant, post, or event reviews:

- `review_id`
- `user`
- `post`
- `event`
- `restaurant`
- `comment`
- `image`
- `rating`
- `created_at`

### Bookmark

Stores saved restaurants:

- `bookmark_id`
- `user`
- `restaurant`
- `saved_at`

## URL Routes

The project-level URL file includes the `foodhunt` app at the root path:

```text
my_django_project/cyberfoodhunt/urls.py
```

Application routes are defined in:

```text
my_django_project/foodhunt/urls.py
```

Current app routes:

| URL | View | Purpose |
| --- | --- | --- |
| `/` | `event_list` | Shows active events |
| `/home/` | `home` | Main discover page |
| `/search/` | `search` | Search and filter restaurants |
| `/<event_id>/` | `event_detail` | View one event |
| `/new/` | `event_create` | Create a new event |
| `/<event_id>/delete/` | `event_delete` | Delete an event |
| `/userprofile/` | `userprofile` | View profile and badges |
| `/restaurant/<restaurant_id>/` | `restaurant_detail` | View one restaurant |
| `/review/` | `review_create` | Create a review without preselected target |
| `/review/restaurant/<restaurant_id>/` | `review_create` | Create a review for a restaurant |
| `/review/event/<event_id>/` | `review_create` | Create a review for an event |
| `/review/submit/` | `review_submit` | Submit review form |
| `/admin/` | Django admin | Admin dashboard |

## Setup Instructions

These instructions assume you are running the project locally from the repository root.

### 1. Open the Project Folder

```bash
cd 2610_CyberFoodHunt_G024
```

### 2. Move Into the Django Project

```bash
cd my_django_project
```

### 3. Create a Virtual Environment

If a virtual environment does not already exist, create one:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install Django

If dependencies are not already installed:

```bash
pip install django
```

The settings file was generated using Django 6.0.3, so using Django 6.x is recommended for the closest match.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Optional: Load Sample SQL Data

The repository includes:

```text
schema.sql
seed.sql
```

These files describe and populate the database tables with sample users, restaurants, posts, events, reviews, and bookmarks.

If you are using the existing `db.sqlite3`, sample data may already be present. If you recreate the database manually with SQL, run the schema first and then the seed file.

Example using SQLite CLI:

```bash
sqlite3 db.sqlite3 < schema.sql
sqlite3 db.sqlite3 < seed.sql
```

### 8. Create an Admin User

To access Django admin:

```bash
python manage.py createsuperuser
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Useful pages:

```text
http://127.0.0.1:8000/home/
http://127.0.0.1:8000/search/
http://127.0.0.1:8000/admin/
```

## Admin Panel

The following models are registered in Django admin:

- Bookmark
- Event
- Restaurant
- User
- Post
- Review

Admin registration file:

```text
my_django_project/foodhunt/admin.py
```

After creating a superuser, run the server and visit:

```text
http://127.0.0.1:8000/admin/
```

## Media Uploads

The project is configured for media uploads during local development:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
```

The project URL configuration serves uploaded media files in development using:

```python
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This is suitable for development only. For production, media files should be served using a proper media storage setup.

## Current Development Notes

This project is still in progress. Important notes:

- Authentication is not fully connected yet.
- Some views temporarily use `User.objects.first()` as the current user.
- `@login_required` decorators are commented out in some event-related views for testing.
- The custom `User` model is separate from Django's built-in authentication model.
- Passwords in the custom `User` table are plain text in the current schema and seed data. This should not be used in production.
- Some templates for login, registration, password recovery, bookmarks, and food spots exist but may not yet be fully wired into the URL/view flow.
- The default landing route `/` currently points to the event list, while the main discover page is available at `/home/`.
- Tailwind CSS is loaded through a CDN in templates, which is convenient for development but may need a build step for production.

## Suggested Future Improvements

- Connect the app to Django's built-in authentication system.
- Replace temporary `User.objects.first()` logic with `request.user`.
- Hash passwords properly and avoid storing plain text passwords.
- Add login, logout, registration, and password recovery views.
- Add create/edit/delete flows for restaurant food posts.
- Add bookmark buttons and bookmark listing behavior in the UI.
- Improve review validation, especially rating limits and empty comments.
- Add automated tests for search filters, event expiry, reviews, and profile badges.
- Add static and media file handling suitable for deployment.
- Add a `requirements.txt` file for easier dependency installation.
- Consider changing `/` to the home/discover page if that is intended as the main entry point.

## Testing

There is currently a placeholder test file:

```text
my_django_project/foodhunt/tests.py
```

To run Django tests:

```bash
python manage.py test
```

Recommended test areas:

- Restaurant search by name
- Cuisine filtering
- Halal filtering
- Price filtering
- Active vs expired event filtering
- Review creation
- User badge calculation
- Restaurant detail review listing

## Contributors

This appears to be a group coursework/project repository for Cyber Food Hunt G024. Add team member names, IDs, and roles here if needed.

Example:

```text
Team G024
- Member 1: Role / contribution
- Member 2: Role / contribution
- Member 3: Role / contribution
```

## License

No license file is currently included in the repository. Add one if the project will be shared publicly.
