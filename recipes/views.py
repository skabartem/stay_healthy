from django.shortcuts import render, redirect
from .models import *
from .forms import AddNewRecipe
import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def front_page(request):
    search_query = ''

    recipes = list(Recipe.objects.filter())
    selected_recipes = random.sample(recipes, 4)
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        profiles = Recipe.objects.filter(name__icontains=search_query)
        context = {'profiles': profiles, 'search_query': search_query}

        return render(request, 'recipes/recipes.html', context=context)

    context = {'recipes': selected_recipes, 'search_query': search_query}
    return render(request, 'index.html', context)


def search_recipes(request):
    search_title, search_kcal_from, search_kcal_to = '', '', ''

    request.GET.get('search_title')

    # check filtering fields
    if request.GET.get('search_title'):
        search_title = request.GET.get('search_title')
    if request.GET.get('search_kcal_from'):
        search_kcal_from = request.GET.get('search_kcal_from')
    if request.GET.get('search_kcal_to'):
        search_kcal_to = request.GET.get('search_kcal_to')

    recipes = Recipe.objects.filter()
    if search_title:
        recipes = recipes.filter(
            Q(title__icontains=search_title) |
            Q(time__icontains=search_title)
        )
    if search_kcal_from:
        recipes = recipes.filter(kcal__gte=search_kcal_from)
    if search_kcal_to:
        recipes = recipes.filter(kcal__lte=search_kcal_to)

    # pagination
    page = request.GET.get('page')
    el_per_page = 5
    left_right_pages_range = 2
    paginator = Paginator(recipes, el_per_page)

    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        recipes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        recipes = paginator.page(page)

    left_index = int(page) - left_right_pages_range
    if left_index < 1:
        left_index = 1
    right_index = int(page) + left_right_pages_range + 1
    if right_index > paginator.num_pages:
        right_index = paginator. num_pages + 1

    page_range = range(left_index, right_index)

    context = {'recipes': recipes,
               'nr_results': paginator.count,
               'search_title': search_title,
               'custom_range': page_range,
               'search_kcal_from': search_kcal_from,
               'search_kcal_to': search_kcal_to}
    return render(request, 'recipes/recipes.html', context=context)


@login_required(login_url='user/login')
def add_recipe(request):
    form = AddNewRecipe()

    if request.method == 'POST':
        form = AddNewRecipe(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.added_by = request.user
            recipe.save()

            return redirect('front-page')

    context = {'form': form}
    return render(request, 'recipes/add-recipe.html', context)
