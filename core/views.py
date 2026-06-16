from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.

def landing_page(request):
    return render(request, 'core/landing.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct following errors')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'core/login.html')

@login_required
def home_view(request):
    return render(request, 'core/home.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('landing')