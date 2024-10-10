from django.urls import path
from . import views

urlpatterns = [

    path('', views.enrolled_courses, name='enrolled_courses'),
    path('course/<int:course_id>/problems/', views.course_problems, name='course_problems'),
    path('course/<int:course_id>/problems/', views.course_problems, name='course_problems'),
    path('problem/<int:problem_id>/', views.problem_view, name='problem_view'),
    path('problem/<int:problem_id>/timeout/', views.problem_timeout_view, name='problem_timeout'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('role-list', views.role_list, name='role_list'),
    path('create/', views.role_create, name='role_create'),
    path('<int:role_id>/edit/', views.role_edit, name='role_edit'),
    path('<int:role_id>/delete/', views.role_delete, name='role_conform_delete'),

]