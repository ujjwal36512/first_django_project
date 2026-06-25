from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})),
    password2 = forms.CharField(label='Confirm Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = [  'email', 
                    'full_name', 
                    'address',
                    'gender', 
                    'contact_number',
                    'password1', ''
                    'password2']
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError('Email already exists')
            return email
        
    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if contact:
            cleaned =contact.replace(' ', '').replace('-', '')
            if not cleaned.isdigit():
                raise ValidationError('Contact number must contain only digits.')
            
            if len(cleaned) <10:
                raise ValidationError('Contact number must be at least 10 digits long.')
        return contact
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
       
        if commit:
            user.save()
        return user
    
    