from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login-user'),
    path('logout/', views.logoutUser, name='logout-user'),

    path('register/', views.registerUser, name='register-user'),
    path('profile/', views.userProfile, name="profile"),
    path('profile-update/', views.profileUpdate, name="profile-update"),

    path('weight-changes/', views.trackWeight, name="weight-changes"),
]

