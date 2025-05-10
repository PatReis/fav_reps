from . import views
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/', views.recipes_overview, name="recipes"),
    path('recipes-video/', views.recipes_video, name="recipes-video"),
    path('recipes-likes/', views.recipes_likes, name="recipes-likes"),

    path('recipes-book/', views.recipes_book, name="recipes-book"),

    path('recipe/<str:pk>/', views.recipe, name="recipe"),

    path('create-recipe/', views.createRecipe, name="create-recipe"),
    path('update-recipe/<str:pk>/', views.updateRecipe, name="update-recipe"),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name="delete-recipe"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
