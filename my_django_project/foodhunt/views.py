from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event


#Show all active events
def event_list(request):
    today  = timezone.now().date()
    #Only get events that haven't expired yet (end_date >= today)
    events = Event.objects.filter(end_date__gte=today).order_by("end_date")
    return render(request, "foodhunt/event_list.html", {"events": events})
    #Send event data to HTML page so user can see it.

#Show 1 single event
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