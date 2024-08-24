from . import views
# from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('login/', views.loginPage, name="user-login"),
    path('login-required/', views.loginRequired, name="user-login-required"),
    path('logout/', views.logoutUser, name="user-logout"),
    path('register/', views.registerPage, name="user-register"),
    path('update/', views.updateUser, name="user-update"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]
