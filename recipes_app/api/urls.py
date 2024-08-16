from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('recipes/', views.getRecipes),
    path('topics/', views.getTopics),
    path('recipe/<str:pk>/', views.getRecipe),
]