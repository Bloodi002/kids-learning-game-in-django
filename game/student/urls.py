from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_list, name='role_list'),
    path('create/', views.role_create, name='role_create'),
    path('<int:role_id>/edit/', views.role_edit, name='role_edit'),
    path('<int:role_id>/delete/', views.role_delete, name='role_conform_delete'),
    path('register/', views.register, name='register'),
]