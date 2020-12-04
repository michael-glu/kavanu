from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.core import paginator
from django.contrib import messages

from account.models import Account
from .models import Event
from .forms import CreateEventForm, EditEventForm

EVENTS_PER_PAGE = 1

def index(request):
    context = {}
    query =  ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)
        
    upcoming_event_list = get_event_queryset(query)
    
    #Pagination
    page = request.GET.get('page', 1)
    events_paginator = paginator.Paginator(upcoming_event_list, EVENTS_PER_PAGE)
    
    try:
        upcoming_event_list = events_paginator.page(page)
    except paginator.PageNotAnInteger:
        upcoming_event_list = events_paginator.page(EVENTS_PER_PAGE)
    except paginator.EmptyPage:
        upcoming_event_list = events_paginator.page(events_paginator.num_pages)
    
    context['upcoming_event_list'] = upcoming_event_list
    
    return render(request, 'events/index.html', context)
    
def detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    
    user = request.user

    if request.POST.get("join"):
        if not user.is_authenticated:
            return redirect('must_authenticate')
        if not event.account_set.filter(pk=user.pk).exists():
            event.account_set.add(user)
        
    if request.POST.get("leave"):
        if not user.is_authenticated:
            return redirect('must_authenticate')
        if event.account_set.filter(pk=user.pk).exists():
            event.account_set.remove(user)

        else:
            context['already_playing_message'] = "You are already playing"
            
    return render(request, 'events/detail.html', context)
    
def create(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
        
    form = CreateEventForm(request.POST or None, request.FILES or None,)
    if form.is_valid():
        obj = form.save(commit=False)
        host = Account.objects.filter(email=user.email).first()
        obj.host = host
        obj.save()
        messages.success(request, "Event Created")
        form = CreateEventForm()
        
        if request.POST.get("host_attend", ""):
            obj.account_set.add(user)
            
        return redirect('account')
        
    context['form'] = form
        
    return render(request, 'events/create.html', context)


def edit(request, pk):
    
    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
 
    event = get_object_or_404(Event, pk=pk)
    
    if event.host != user:
        return HttpResponse("You are not authorized to edit this event.")
    
    if request.POST:
        form = EditEventForm(request.POST or None, request.FILES or None, instance=event)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Updated Event")
            event = obj
            
        return redirect('account')
            
    form = EditEventForm(
        initial = {
            "title":            event.title,
            "datetime":         event.datetime,
            "location":         event.location,
            "description":      event.description,
            "image":            event.image,
            "min_attendees":    event.min_attendees,
            "max_attendees":    event.max_attendees,
        }
    )
    context['form'] = form
    
    return render(request, 'events/edit.html', context)

def delete(request, pk):
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
 
    event = get_object_or_404(Event, pk=pk)
    if event.host != user:
        return HttpResponse("You are not authorized to delete this event.")
    
    if request.POST:
        event.delete()
    
    return redirect('account')
    
    
def get_event_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        events = Event.objects.filter(datetime__gte=timezone.now()).filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(location__icontains=q) |
                Q(datetime__icontains=q)
            ).distinct().order_by('datetime')
        
        for event in events:
            queryset.append(event)
            
    return list(set(queryset))
