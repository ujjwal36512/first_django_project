from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages
from recipes.models import Recipe

# Create your views here.

class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration Successful')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request,'Please correct the following errors')
        return super().form_invalid(form)
    
    
# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'Registration successful.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Please correct following errors')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'core/register.html', {'form':form})

class customerLoginView(LoginView):
    template_name = 'core/ogin.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Email or Password')
        return super().form_invalid(form)
        
    
# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid email or password')
#     return render(request, 'core/login.html')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()[:6]
        return context
    
# @login_required
# def home_view(request):
#     recipes = Recipe.objects.all()[:6]
#     return render(request, 'core/home.html',{'recipes':recipes})


# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have been successfully logged out.')
#     return redirect('landing')

class CustomerLogoutView(LogoutView):
    next_page = reverse_lazy('landing')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)
           
        