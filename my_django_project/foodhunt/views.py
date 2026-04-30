from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event, User, Restaurant #The User is added just to test event_create
from django.contrib.auth.decorators import login_required


#-----Show all active events
def event_list(request):
    today  = timezone.now().date()
    #Only get events that haven't expired yet (end_date >= today)
    events = Event.objects.filter(end_date__gte=today).order_by("end_date")
    return render(request, "foodhunt/event_list.html", {"events": events})
    #Send event data to HTML page so user can see it.

#-----Show 1 single event details
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
    })


#-----Logged-in: Post a new event
#@login_required(will be put back after testing) #deceorater to require login
def event_create(request):
    if request.method == "POST": #asking for data from form
        event_name     = request.POST.get("event_name")
        event_location = request.POST.get("event_location")
        description    = request.POST.get("description")
        end_date       = request.POST.get("end_date")

        #Add this just to test, remove it once Ayra done with login system
        current_user = User.objects.first()   #get(username=request.user.username)  will be put back afetr test

        Event.objects.create(
            user           = current_user, #after login system done, change this to request.user
            event_name     = event_name,
            event_location = event_location,
            description    = description,
            end_date       = end_date,
            image          = request.FILES.get("image") #<-- newly added line 
        )
        return redirect("event_list")
        #send user back to event list after creating new event
    
    return render(request, "foodhunt/event_form.html")
    #if no data is sent, show the form to create a new event

#-----Logged-in: Delete own event
#@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, event_id=event_id) #, user= request.user) 
    # SECURITY CHECK: Only fetch the event if it exists AND belongs to the ogged-in user.
    # user can only view or edit their own event

    if request.method == "POST":
        event.delete() #permanently remove database
        return redirect("event_list")
    
    return render(request, "foodhunt/event_detail.html", {"event": event}) 

#------Search page (basically dashboard)
def search(request):
    restaurants = Restaurant.objects.all()

    #Filter by name
    q = request.GET.get("q") # If someone searches "KFC", the URL becomes /search/?q=KFC
    if q:
        restaurants = restaurants.filter(restaurant_name__icontains=q) #case insensitive

    #filter by cuisine
    cuisine = request.GET.get("cuisine")
    if cuisine:
        restaurants = restaurants.filter(cuisine = cuisine)

    #filter by transport
    transport = request.GET.get("transport")
    if transport:
        restaurants = restaurants.filter(transport_mode = transport)

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

    return render(request, "foodhunt/search.html", {"restaurants": restaurants})




