
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CourseContactMapping, Course, Problem, Contact, Role, ProblemScoreMapping
from .forms import RoleForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


def index(request):
    return render(request, 'index.html')


@login_required
def role_list(request):
    roles = Role.objects.all().order_by('-role_id')
    return render(request, 'role_list.html', {'roles': roles})

@login_required
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
def enrolled_courses(request):
    # Get the current user's associated contact
    contact = get_object_or_404(Contact, user=request.user)
    
    # Use 'course_id' instead of 'course' in select_related
    enrolled_courses = CourseContactMapping.objects.filter(contact_id=contact).select_related('course_id')
    return render(request, 'student_quiz/enrolled_courses.html', {'courses': enrolled_courses})



@login_required 
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









