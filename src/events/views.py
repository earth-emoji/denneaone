from django.shortcuts import render, get_object_or_404, redirect

from .forms import EventForm
from .models import Event
from accounts.models import Customer, Vendor

# Create your views here.
def events_list(request, template_name='events/events_list.html'):
    events = Event.objects.all()
    data = {}
    data['events'] = events
    return render(request, template_name, data)

def user_events(request, pk, template_name='events/events_list.html'):
    vendor = get_object_or_404(Vendor, pk=pk)
    events = Event.objects.filter(vendor=vendor)
    data = {}
    data['events'] = events
    return render(request, template_name, data)

def event_create(request, template_name='events/events_form.html'):
    form = EventForm(request.POST or None)
    if form.is_valid():
        c = form.save(commit=False)
        c.vendor = request.user.vendor
        c.save()
        return redirect('events:event-view', c.id)
    return render(request, template_name, {'form':form})

def event_details(request, pk, template_name='events/event_details.html'):
    event = get_object_or_404(Event, pk=pk)
    data = {}
    data['event'] = event
    return render(request, template_name, data)