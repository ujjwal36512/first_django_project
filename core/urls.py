from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.customerLoginView.as_view(), name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
]