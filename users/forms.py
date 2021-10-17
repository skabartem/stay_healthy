from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Full Name',
        }


class ProfileUpdate(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'male', 'age', 'weight_kg', 'height_cm', 'activity_coefficient', 'meals_p_day', 'goal']
        labels = {
            'male': 'Gender',
            'weight_kg': 'Weight (kg)',
            'height_cm': 'Height (cm)',
            'activity_coefficient': 'Activeness level',
            'meals_p_day': 'Meals per day',
        }
