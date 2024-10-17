
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CourseContactMapping, Course, Problem, Contact, Role, ProblemScoreMapping, Achievement
from .forms import RoleForm, UserRegistrationForm, CourseRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.http import HttpResponse
import subprocess


def index(request):
    return render(request, 'index.html')

def role_required(role_type):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            contact = Contact.objects.get(user=request.user)
            if contact.role_id.role_type == role_type:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator

@login_required
@role_required('Teacher')
def role_list(request):
    roles = Role.objects.all().order_by('-role_id')
    return render(request, 'role_list.html', {'roles': roles})

@login_required
@role_required('Teacher')
def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST, request.FILES)
        if form.is_valid():
            role = form.save(commit=False)
            role.user = request.user
            role.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})

@login_required
@role_required('Teacher')
def role_edit(request, role_id):
    # role = get_object_or_404(Role, pk=role_id, user = request.user)
    role = get_object_or_404(Role, pk=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, request.FILES, instance=role)
        if form.is_valid():
            role = form.save(commit=False)
            role.save()
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})

@login_required
@role_required('Teacher')
def role_delete(request, role_id):
    # role = get_object_or_404(Role, pk=role_id, user = request.user)
    role = get_object_or_404(Role, pk=role_id)
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    return render(request, 'role_conform_delete.html', {'role', role})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password
            user.save()

            # Create Contact with additional details
            contact = Contact(
                user=user,
                email_id=form.cleaned_data['email'],
                mobile_number=form.cleaned_data['mobile_number'],
                role_id=form.cleaned_data['role_id'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                is_active=False  # Adjust according to your logic
            )
            contact.save()

            # Log the user in
            login(request, user)
            return redirect('role_list')  # Redirect to role list after successful registration
        else:
            print(form.errors)  # Debugging: Print errors to console
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to login page after logout
    return redirect('login')

@login_required
@role_required('Student')
def enrolled_courses(request):
    # Get the current user's associated contact
    contact = get_object_or_404(Contact, user=request.user)
    
    # Use 'course_id' instead of 'course' in select_related
    enrolled_courses = CourseContactMapping.objects.filter(contact_id=contact).select_related('course_id')
    return render(request, 'student_quiz/enrolled_courses.html', {'courses': enrolled_courses})



@login_required 
@role_required('Student')
def course_problems(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Get the current user's contact (assuming you are linking Contact to the user)
    contact = get_object_or_404(Contact, user=request.user)

    # Get the problems associated with the selected course
    problems = Problem.objects.filter(course_id=course)

    # Check if the problem has been attempted and store score in each problem object
    for problem in problems:
        # Check if the user has already attempted the problem
        attempt = ProblemScoreMapping.objects.filter(contact_id=contact, problem_id=problem).first()
        if attempt:
            problem.attempted = True
            problem.score = attempt.score
        else:
            problem.attempted = False

    return render(request, 'student_quiz/course_problems.html', {'course': course, 'problems': problems})

@login_required
@role_required('Student')
def problem_view(request, problem_id):
    # Get the problem instance
    problem = get_object_or_404(Problem, pk=problem_id)
    
    # Handle form submission (POST request)
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        
        # Check if the user's answer matches the correct answer
        if user_answer == problem.answer:
            score = problem.max_score
        else:
            score = 0  # Or you can set partial scoring logic
        
        # Save the score in the ProblemScoreMapping model
        contact = Contact.objects.get(user=request.user)
        ProblemScoreMapping.objects.create(
            contact_id=contact,
            problem_id=problem,
            score=score
        )

        # Redirect to the problems list page after submission
        return HttpResponseRedirect(reverse('course_problems', args=[problem.course_id]))

    # Handle GET request (initial page load)
    return render(request, 'student_quiz/problem_page.html', {
        'problem': problem  # Pass time bound in seconds
    })
    
@login_required
@role_required('Student')
def problem_timeout_view(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    
    # Set score to 0 since the user did not submit on time
    contact = Contact.objects.get(user=request.user)
    ProblemScoreMapping.objects.create(
        contact_id=contact,
        problem_id=problem,
        score=0
    )
    
    # Redirect to the problems list page after timeout
    return HttpResponseRedirect(reverse('course_problems', args=[problem.course_id]))

def teacher_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a teacher
            contact = Contact.objects.get(user=user)
            if contact.role_id.role_type == 'Teacher':
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                return render(request, 'registration/teacher_login.html', {'error': 'Not authorized as teacher'})
        else:
            return render(request, 'registration/teacher_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'registration/teacher_login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a student
            contact = Contact.objects.get(user=user)
            if contact.role_id.role_type == 'Student':
                login(request, user)
                return redirect('enrolled_courses')  # Redirect to student dashboard
            else:
                return render(request, 'login.html', {'error': 'Not authorized as student'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'registration/login.html')


@login_required
@role_required('Teacher')  

def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html', {'current_year': datetime.now().year})


from django.http import JsonResponse

from django.http import JsonResponse

@login_required
@role_required('Teacher')  # Ensure only teachers can access this view
def register_students_in_course(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            students = form.cleaned_data['students']

            for student in students:
                contact = get_object_or_404(Contact, id=student.id)
                CourseContactMapping.objects.create(course_id=course, contact_id=contact)

            return redirect('teacher_dashboard')  # Redirect to dashboard after successful registration
    else:
        form = CourseRegistrationForm()

    # Handle AJAX request for student filtering
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Modern way to detect AJAX request
        course_id = request.GET.get('course_id')
        if course_id:
            try:
                course_id = int(course_id)
                registered_students = CourseContactMapping.objects.filter(course_id=course_id).values_list('contact_id', flat=True)
                students = Contact.objects.filter(role_id__role_type='Student').exclude(id__in=registered_students)
                # Fetch user__username and email_id
                student_list = list(students.values('id', 'user__username', 'email_id'))
                return JsonResponse({'students': student_list})
            except (ValueError, TypeError):
                pass
        return JsonResponse({'students': []})

    return render(request, 'teacher/register_students_in_course.html', {'form': form})


@login_required
@role_required('Teacher')  # Only allow access for Teachers
def student_course_list(request):
    # Get all students and their registered courses
    students = Contact.objects.filter(role_id__role_type='Student')
    
    # For each student, find their registered courses
    student_courses = []
    for student in students:
        courses = CourseContactMapping.objects.filter(contact_id=student).select_related('course_id')
        student_courses.append({
            'student': student,
            'courses': courses
        })

    return render(request, 'teacher/student_course_list.html', {'student_courses': student_courses})


@login_required
def achievement_view(request):
    achievements = Achievement.objects.filter(user=request.user)
    if achievements.exists():
        # Calculate the average score
        total_correct_answers = achievements.aggregate(Avg('correct_answers'))['correct_answers__avg']
        average_score = round((total_correct_answers / 100) * 10, 2)  # Assuming 100 is the max score
        
        # Assign a badge based on the average score
        if 8 <= average_score <= 10:
            badge = 'GOLD'
        elif 5 <= average_score < 8:
            badge = 'SILVER'
        elif 2 <= average_score < 5:
            badge = 'BRONZE'
        else:
            badge = 'You need to try hard'
    else:
        average_score = 0
        badge = 'You need to try hard'

    return render(request, 'achievement.html', {
        'achievements': achievements,
        'average_score': average_score,
        'badge': badge
    })

def run_opencv_script(request):
    # Run the Python script using subprocess
    try:
        # Replace the path below with the actual path to your Python script
        script_path = 'C:/path_to_your_script/opencv_script.py'
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return HttpResponse(f"Script executed successfully.<br>{stdout.decode('utf-8')}")
        else:
            return HttpResponse(f"Script failed to execute.<br>Error: {stderr.decode('utf-8')}")
    
    except Exception as e:
        return HttpResponse(f"Error running script: {str(e)}")
