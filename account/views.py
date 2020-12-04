from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from events.models import Event
from .models import Account

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect(reverse('events:index'))
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('events:index')) #Homepage
    
def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect(reverse('events:index')) #Homepage
        
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                return redirect(reverse('events:index')) #Homepage
                
    else:
        form = AccountAuthenticationForm()
       
    context['login_form'] = form
    return render(request, 'account/login.html', context)
    
    
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    context = {}
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
            
    else:
        form = AccountUpdateForm(
            initial= {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    
    # events_attending = request.user.events
    # context['events_attending'] = events_attending
    
    events_hosting = Event.objects.filter(host=request.user)
    context['events_hosting'] = events_hosting
    
    return render(request, 'account/account.html', context)
    
def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})

