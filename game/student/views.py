from django.shortcuts import render
from .models import Role, Contact
from .forms import RoleForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


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








