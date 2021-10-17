from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Recipe
from .models import Weight
from .forms import *
import random


@login_required(login_url='/user/login')
def userProfile(request):
    profile = Profile.objects.filter(user=request.user).first()

    # amr is 0 only if data incomplete and require update
    if profile.amr != 0:
        goal_multipliers = {
            -1: {'min': 0.9, 'max': 0.95},
            0: {'min': 0.97, 'max': 1.03},
            1: {'min': 1.05, 'max': 1.1}
        }

        if profile.bmi < 18.5:
            bmi_info = 'Underweight (<18.5 score)'
        elif 18.5 <= profile.bmi < 25:
            bmi_info = 'Normal weight (18.5–24.9 score)'
        elif 25 <= profile.bmi < 30:
            bmi_info = 'Overweight (25–29.9 score)'
        elif profile.bmi >= 30:
            bmi_info = 'Obesity  (30 or greater score)'

        kcal_per_dish = profile.amr * goal_multipliers[profile.goal]['max'] / profile.meals_p_day
        all_recipes = list(Recipe.objects.filter(kcal__gte=kcal_per_dish * 0.98, kcal__lte=kcal_per_dish * 1.02))
        recipes_list = random.sample(all_recipes, profile.meals_p_day-1)
        kcal_spent = sum([recipe.kcal for recipe in recipes_list])

        last_dish_kcal_min = profile.amr * goal_multipliers[profile.goal]['min'] - kcal_spent
        last_dish_kcal_max = profile.amr * goal_multipliers[profile.goal]['max'] - kcal_spent

        last_recipe = random.choice(Recipe.objects.filter(kcal__gte=last_dish_kcal_min, kcal__lte=last_dish_kcal_max))
        if last_recipe in recipes_list:
            last_recipe = random.choice(Recipe.objects.filter(kcal__gte=last_dish_kcal_min, kcal__lte=last_dish_kcal_max))
        recipes_list.append(last_recipe)

        total_kcal = sum([dish.kcal for dish in recipes_list])

        context = {'profile': profile, 'recipes': recipes_list, 'total_kcal': total_kcal, 'bmi_info': bmi_info}
        return render(request, 'users/profile.html', context)

    else:
        messages.success(request, 'Update your profile in order to see your ')
        return redirect('/user/profile-update/')


@login_required(login_url='/user/login')
def profileUpdate(request):
    profile = request.user.profile
    form = ProfileUpdate(instance=profile)

    if request.method == 'POST':
        if profile:
            form = ProfileUpdate(request.POST, request.FILES, instance=profile)
        else:
            form = ProfileUpdate(request.POST)

        if form.is_valid():
            form.save(commit=False)
            Weight.objects.create(profile=request.user.profile, weight=form.cleaned_data['weight_kg'])

            form.save()

        return redirect('profile')

    context = {'form': form}
    return render(request, 'users/profile_update.html', context)


@login_required(login_url='/user/login')
def trackWeight(request):
    profile = request.user.profile

    weights = Weight.objects.filter(profile=profile)

    context = {'weights': weights}
    return render(request, 'users/weight-tracker.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('login-user')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('front-page')
        else:
            return redirect('login-user')
    return render(request, 'users/login_page.html')


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('front-page')


def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('profile-update')

        else:
            messages.success(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'users/register_page.html', context)
