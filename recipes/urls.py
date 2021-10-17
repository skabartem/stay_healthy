from django.urls import path
from . import views

urlpatterns = [

    path('', views.front_page, name='front-page'),

    path('add-recipe', views.add_recipe, name='new-recipe'),

    path('recipes/', views.search_recipes, name='recipes'),
]