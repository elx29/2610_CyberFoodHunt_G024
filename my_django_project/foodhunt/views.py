from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event,User, Restaurant, Post, Review 
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg, F



#-----Event List(ELX): Show all active events
def event_list(request):
    today  = timezone.now().date()
    #Only get events that haven't expired yet (end_date >= today)
    events = Event.objects.filter(end_date__gte=today).order_by("end_date")
    return render(request, "foodhunt/event_list.html", {"events": events})
    #Send event data to HTML page so user can see it.

#-----Event Detail(ELX): Show 1 single event details
def event_detail(request, event_id):
    today = timezone.now().date()
    #looks for event with matching event_id, or shows 404 error if not found
    event = get_object_or_404(Event, event_id=event_id)

    #Go back to the list if types expired event
    if event.end_date < today:
        return redirect("event_list")
    
    days_left = (event.end_date - today).days
    return render(request, "foodhunt/event_detail.html", {
        "event": event,
        "days_left": days_left,
        "login_user_id": request.session.get("user_id"), #the one who create the post can delete/edit button
    })


#-----Event Create(ELX): Logged-in: Post a new event
def event_create(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    if request.method == "POST": #asking for data from form
        current_user = User.objects.get(user_id=user_id)
        Event.objects.create(
            user           = current_user,
            event_name     = request.POST.get("event_name"),
            event_location = request.POST.get("event_location"),
            description    = request.POST.get("description"),
            start_date     = request.POST.get("start_date"),
            end_date       = request.POST.get("end_date"),
            image          = request.FILES.get("image"),
    )

        return redirect("event_list") #send user back to event list after creating new event
    return render(request, "foodhunt/event_form.html") #if no data is sent, show the form to create a new event
   

#-----Event Delete(ELX): Logged-in: Delete own event
def event_delete(request, event_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    current_user = User.objects.get(user_id=user_id)
    # SECURITY CHECK: Only fetch the event if it exists AND belongs to the ogged-in user.
    # user can only view or edit their own event
    event = get_object_or_404(Event, event_id=event_id, user=current_user)  
    

    if request.method == "POST":
        event.delete() #permanently remove database
        return redirect("event_list")
    
    return render(request, "foodhunt/event_detail.html", {"event": event}) 

#-----open now function(akisha)
import re
from datetime import datetime

def is_restaurant_open(opening_hours_str):
    if not opening_hours_str:
        return False
    
    hours_clean = opening_hours_str.lower().strip()
    
    # Handle common 24-hour identifiers
    if any(x in hours_clean for x in ["24 hours", "24h", "24/7"]):
        return True
        
    # Match standard times like "10:00am", "10am", "10:00 am", "10 pm", "22:00"
    time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'
    matches = re.findall(time_pattern, hours_clean)
    
    if len(matches) >= 2:
        try:
            current_time = datetime.now().time()
            
            has_ampm = 'am' in hours_clean or 'pm' in hours_clean
            
            # Helper to convert a parsed match to a 24-hour time object
            def to_time(hour_str, min_str, period, is_end_time=False, start_hour=None):
                h = int(hour_str)
                m = int(min_str) if min_str else 0
                
                # Smart PM heuristic: if no AM/PM is specified anywhere, and the end hour is smaller than the start hour
                # (e.g., "7 to 1" or "9 to 5"), assume the end hour is in the afternoon (PM)
                if not has_ampm and is_end_time and start_hour is not None and h < start_hour and h < 12:
                    h += 12
                elif period == 'pm' and h < 12:
                    h += 12
                elif period == 'am' and h == 12:
                    h = 0
                return datetime.strptime(f"{h}:{m}", "%H:%M").time()
            
            start = to_time(matches[0][0], matches[0][1], matches[0][2])
            end = to_time(matches[1][0], matches[1][1], matches[1][2], is_end_time=True, start_hour=int(matches[0][0]))
            
            if start <= end:
                return start <= current_time <= end
            else:
                # Handle overnight ranges (e.g. 6:00pm to 2:00am)
                return current_time >= start or current_time <= end
        except Exception:
            return False
            
    return False

#------Search+Filter (ELX + AKISHA): Search bar and filter at search page
def search(request):
    restaurants = Restaurant.objects.all()

    #Filter by name
    q = request.GET.get("q") # If someone searches "KFC", the URL becomes /search/?q=KFC
    if q:
        restaurants = restaurants.filter(restaurant_name__icontains=q) #case insensitive

    #filter by cuisine
    cuisine = request.GET.get("cuisine")
    if cuisine:
        restaurants = restaurants.filter(cuisine__iexact = cuisine)

    #filter by transport
    transport = request.GET.get("transport")
    if transport:
        restaurants = restaurants.filter(transport_mode__icontains = transport)

    #filter by Halal/Non halal
    is_halal = request.GET.get("is_halal")
    if is_halal:
        restaurants = restaurants.filter(is_halal = 1)

    #filter by price range
    price = request.GET.get("price")
    if price == "$":
        restaurants = restaurants.filter(max_price__lte=15) #lte= less than or equal to
    elif price == "$$":
        restaurants = restaurants.filter(max_price__gte=15, max_price__lte=30)
    elif price == "$$$":
        restaurants = restaurants.filter(min_price__gte=30)

    #filter by Open Now (AKISHA)
    open_now = request.GET.get("open_now")
    if open_now:
        restaurants = [r for r in restaurants if is_restaurant_open(r.opening_hours)]

    #filter for rating (ELX)
    sort_by = request.GET.get("sort", "top_rated")#default sorting is by top rated

    if sort_by == "top_rated":
        restaurants = restaurants.annotate(avg_rating=Avg('review__rating')).order_by(F('avg_rating').desc(nulls_last=True))# calculate average rating and sort by it, with unrated restaurants at the end
    elif sort_by == "low_rated":
        restaurants = restaurants.annotate(avg_rating=Avg('review__rating')).order_by(F('avg_rating').asc(nulls_last=True))# ascending
    elif sort_by == "newest":
        restaurants = restaurants.order_by("-restaurant_id") #newest first based on restaurant_id

    return render(request, "foodhunt/search.html", {
        "restaurants": restaurants,
        "sort": sort_by,
    })

#------Home Page (ELX): Show active events + restaurant recommendations
def home(request):
    today   = timezone.now().date()#get active events for banner
    events  = Event.objects.filter(end_date__gte=today).order_by("end_date")[:3] 
    restaurant = Restaurant.objects.all().order_by("-restaurant_id")[:6]

    is_student = False
    user_email = request.session.get("email")
    if user_email and user_email.strip().lower().endswith("@student.mmu.edu.my"):
        is_student = True

    student_promos = []
    if is_student:
        student_promos = Restaurant.objects.filter(is_student_promo=True).order_by("-restaurant_id")[:6]

    return render(request, 'foodhunt/main.html', {
        "events": events,
        "restaurants": restaurant,
        "today": today,
        "is_student": is_student,
        "student_promos": student_promos,
    })

#------User Profile (ELX): Show user details, badges, recent posts/events
def userprofile(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    current_user = get_object_or_404(User, user_id=user_id)
    post_count = Post.objects.filter(user=current_user).count() #get number of posts by user
    event_count= Event.objects.filter(user=current_user).count() #get number of event posts by user
    
    #Recent post and events that will appear on user profile page
    today = timezone.now().date()
    recent_events = Event.objects.filter(user=current_user, end_date__gte=today).order_by("-event_id")[:5]
    recent_posts = Post.objects.filter(user=current_user).order_by("-created_at")[:5]

    badges = [] #empty list

    #Badges
    if post_count >= 1:
        badges.append({"name": "Rookie Hunter", "icon": "restaurant", "desc": "Posted first food spot"})
    if post_count >= 5:
        badges.append({"name": "Food Scout", "icon": "explore", "desc": "Posted 5 food spots"})  
    if post_count >= 15:
        badges.append({"name": "Cyber Hunter", "icon": "swords", "desc": "Posted 15 food spots"}) 
    if post_count >= 30:
        badges.append({"name": "Legend", "icon": "crown", "desc": "Posted 30 food spots"})

    # Event badges
    if event_count >= 1:
        badges.append({"name": "Event Starter", "icon": "celebration", "desc": "Posted first event"})
    if event_count >= 5:
        badges.append({"name": "Detective", "icon": "search", "desc": "Posted 5 events"})

    return render(request, 'foodhunt/userprofile.html', {
        "current_user":  current_user,  #this is for userprofile to show actual username
        "badges": badges,
        "post_count": post_count,
        "event_count": event_count,
        "recent_events": recent_events,
        "recent_posts": recent_posts,
    })

#------User Registration (AYRA)
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email    = request.POST.get("email")
        password = request.POST.get("password")
        confirm  = request.POST.get("confirm_password")

        if not username or not email or not password or not confirm:
            return render(request, "foodhunt/register.html", {"error": "All fields are required!"})
        if password != confirm:
            return render(request, "foodhunt/register.html", {"error": "Passwords do not match!"})
        if User.objects.filter(username=username).exists():
            return render(request, "foodhunt/register.html", {"error": "Username already taken!"})
        if User.objects.filter(email=email).exists():
            return render(request, "foodhunt/register.html", {"error": "Email already registered!"})

        User.objects.create(
            username = username,
            email    = email,
            password = make_password(password),
        )
        return redirect("login")
    return render(request, "foodhunt/register.html")

#------User Login (AYRA)
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            request.session["user_id"] = user.user_id
            request.session["email"] = user.email
            return redirect("home")

        return render(request, "foodhunt/login.html", {
            "error": "Invalid email or password!"
        })

    return render(request, "foodhunt/login.html")

#------User Logout (AYRA)
def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('login')
  
#------Restaurant Detail (AYRA)
def restaurant_detail(request, restaurant_id):
    from django.db.models import Avg
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_at")

    # Fetch the original post to find which User account created this restaurant
    first_post = Post.objects.filter(restaurant=restaurant).first()
    creater_id = first_post.user.user_id if first_post else None

    # Calculate average rating of all reviews
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'foodhunt/restaurant_detail.html', {
        'restaurant': restaurant,
        'reviews': reviews,
        'creater_id': creater_id,
        'average_rating': average_rating,
        'login_user_id': request.session.get("user_id"), #the one who create the post can delete/edit button
    })


#------Review Create (AYRA)
def review_create(request, restaurant_id=None, event_id=None):
    restaurants = Restaurant.objects.all()
    selected_restaurant = None
    selected_event = None
    
    if restaurant_id:
        selected_restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    elif event_id:
        selected_event = get_object_or_404(Event, event_id=event_id)
    else:
        # Fallback to query parameters
        restaurant_id_param = request.GET.get('restaurant_id')
        event_id_param = request.GET.get('event_id')
        if restaurant_id_param:
            selected_restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id_param)
        if event_id_param:
            selected_event = get_object_or_404(Event, event_id=event_id_param)
    
    return render(request, 'foodhunt/review.html', {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'selected_event': selected_event
    })

#------Review Submit (AYRA+ELX): Handle review form submission, limit to 1 review per user per restaurant/event, compulsary photo, rating
def review_submit(request):
    if request.method == "POST":

        user_id = request.session.get("user_id")#grab user id from custom login system
        if not user_id:
            return redirect("login")
        
        current_user = get_object_or_404(User, user_id=user_id)
        restaurant_id = request.POST.get("restaurant")
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        image = request.FILES.get("image")

        
        #For compulsary photo
        if not image:
            return render(request, "foodhunt/review.html",{
                "error":"Please upload photo as proof of visit.",
                "restaurants": Restaurant.objects.all(),
                "selected_restaurant": restaurant,
            })
        
         #Check if user rated
        if not rating or rating == "0":
            return render(request, "foodhunt/review.html",{
                "error": "Please provide a rating.",
                "restaurants": Restaurant.objects.all(),
                "selected_restaurant": restaurant,
            })

        if Review.objects.filter(user=current_user, restaurant=restaurant).exists():
            return render(request, "foodhunt/review.html",{
                "error": "You have already reviewed this restaurant.",
                "restaurants": Restaurant.objects.all(),
                "selected_restaurant": restaurant,
                })
        
        Review.objects.create(
            user=current_user,
            restaurant=restaurant,
            rating=int(rating),
            comment=comment,
            image=image,
            created_at=timezone.now()
        )
        return redirect("restaurant_detail", restaurant_id=restaurant.restaurant_id)
    return redirect("review_create")

#------Password Recovery (AKISHA)
def password_recovery(request):
    return render(request, 'foodhunt/passwordrecovery.html')


#------(AYRA) Foodspots — share a new restaurant / food spot
CUISINE_CHOICES = ["Fast Food", "Western", "Chinese", "Malay", "Indian", "Cafe", "Bubble Tea", "Other"]
TRANSPORT_CHOICES = ["Walking Distance", "Public Transport", "Grab/Taxi", "Personal Vehicle"]

def foodspot_create(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    """Display the food-spot submission form (GET) and process it (POST)."""

    context = {
        "cuisine_choices": CUISINE_CHOICES,
        "transport_choices": TRANSPORT_CHOICES,
    }

    if request.method == "POST":
        # --- collect raw values ---
        restaurant_name = request.POST.get("restaurant_name", "").strip()
        cuisine         = request.POST.get("cuisine", "").strip()
        location        = request.POST.get("location", "").strip()
        transport       = request.POST.get("transport", "").strip()
        opening_hours   = request.POST.get("opening_hours", "").strip()
        description     = request.POST.get("description", "").strip()
        halal_raw       = request.POST.get("halal", "0")
        min_price_raw   = request.POST.get("min_price", "").strip()
        max_price_raw   = request.POST.get("max_price", "").strip()
        photo           = request.FILES.get("photo")
        is_student_promo_raw = request.POST.get("is_student_promo")
        is_student_promo = True if is_student_promo_raw else False
        student_promo_desc = request.POST.get("student_promo_desc", "").strip()

        # --- validation ---
        errors = []
        if not restaurant_name:
            errors.append("Restaurant name is required.")
        if not cuisine or cuisine == "Select cuisine":
            errors.append("Please select a cuisine type.")
        if not location:
            errors.append("Location is required.")

        min_price, max_price = None, None
        if min_price_raw:
            try:
                min_price = int(min_price_raw)
                if min_price < 0:
                    errors.append("Min price cannot be negative.")
            except ValueError:
                errors.append("Min price must be a whole number.")
        if max_price_raw:
            try:
                max_price = int(max_price_raw)
                if max_price < 0:
                    errors.append("Max price cannot be negative.")
            except ValueError:
                errors.append("Max price must be a whole number.")
        if min_price is not None and max_price is not None and min_price > max_price:
            errors.append("Min price cannot be greater than max price.")

        # --- re-render form with errors & sticky values ---
        if errors:
            context.update({
                "errors": errors,
                "form_data": request.POST,
            })
            return render(request, "foodhunt/foodspots.html", context)

        # --- save Restaurant ---
        halal_value = int(halal_raw) if halal_raw in ("0", "1", "2") else 0
        restaurant = Restaurant.objects.create(
            restaurant_name = restaurant_name,
            location        = location,
            opening_hours   = opening_hours or None,
            transport_mode  = transport or None,
            cuisine         = cuisine,
            is_halal        = halal_value,
            min_price       = min_price,
            max_price       = max_price,
            description     = description or None,
            is_student_promo = is_student_promo,
            student_promo_desc = student_promo_desc or None,
            image           = photo,  # Save photo directly to Restaurant
        )

        # --- save Post (links photo + description to the restaurant) ---
        # Use logged-in user from session, fall back to first user for now
        current_user = get_object_or_404(User, user_id=user_id)

        Post.objects.create(
            user       = current_user,
            restaurant = restaurant,
            title      = restaurant_name,
            description= description or None,
            image      = photo if photo else None,
            created_at = timezone.now(),
        )

        context["success"] = True
        return render(request, "foodhunt/foodspots.html", context)

    # GET — just show the blank form
    return render(request, "foodhunt/foodspots.html", context)

#------ Restaurant Delete and Edit (only by the user who posted it)
def restaurant_delete(request, restaurant_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('home')
    return redirect('restaurant_detail', restaurant_id=restaurant_id)

#------Restaurant Edit (AYRA): Only the user who posted the restaurant can edit it
def restaurant_edit(request, restaurant_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)

    if request.method == 'POST':
        restaurant.restaurant_name = request.POST.get('restaurant_name', restaurant.restaurant_name)
        restaurant.location        = request.POST.get('location', restaurant.location)
        restaurant.cuisine         = request.POST.get('cuisine', restaurant.cuisine)
        restaurant.opening_hours   = request.POST.get('opening_hours', restaurant.opening_hours)
        restaurant.transport_mode  = request.POST.get('transport', restaurant.transport_mode)
        restaurant.description     = request.POST.get('description', restaurant.description)
        restaurant.is_halal        = request.POST.get('halal', restaurant.is_halal)
        
        photo = request.FILES.get("photo")
        if photo:
            restaurant.image = photo

        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        if min_price: restaurant.min_price = int(min_price)
        if max_price: restaurant.max_price = int(max_price)
        restaurant.save()
        return redirect('restaurant_detail', restaurant_id=restaurant.restaurant_id)

    return render(request, 'foodhunt/foodspots.html', {
        'cuisine_choices': CUISINE_CHOICES,
        'transport_choices': TRANSPORT_CHOICES,
        'form_data': restaurant,
        'editing': True,
        'restaurant': restaurant,
    })