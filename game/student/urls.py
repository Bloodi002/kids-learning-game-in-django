from django.urls import path
from . import views

urlpatterns = [

    path('', views.enrolled_courses, name='enrolled_courses'),
    path('course/<int:course_id>/problems/', views.course_problems, name='course_problems'),
    path('course/<int:course_id>/problems/', views.course_problems, name='course_problems'),
    path('problem/<int:problem_id>/', views.problem_view, name='problem_view'),
    path('problem/<int:problem_id>/timeout/', views.problem_timeout_view, name='problem_timeout'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view , name='login'),
    path('teacher/login/', views.teacher_login_view, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),

    path('role-list/', views.role_list, name='role_list'),
    path('create/', views.role_create, name='role_create'),
    path('<int:role_id>/edit/', views.role_edit, name='role_edit'),
    path('<int:role_id>/delete/', views.role_delete, name='role_conform_delete'),

    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/register_students/',views.register_students_in_course, name='register_students_in_course'),
    path('teacher/student-courses/', views.student_course_list, name='student_course_list'),
    
    path('achievement/', views.achievement_view, name='achievement'),
    path('run-script/', views.run_opencv_script, name='run_script'),
]