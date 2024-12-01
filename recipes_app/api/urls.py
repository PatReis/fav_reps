from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes, name="api_overview"),
    path('recipes/', views.getRecipes, name="api_recipes"),
    path('topics/', views.getTopics, name="api_topics"),
    path('recipe/<str:pk>/', views.getRecipe),
]