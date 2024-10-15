from django import forms
from .models import Role, Contact, Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CourseContactMapping

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_type']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=12)
    role_id = forms.ModelChoiceField(queryset=Role.objects.all())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'mobile_number', 'role_id', 'date_of_birth')

class CourseRegistrationForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), 
        required=True,
        widget=forms.Select(attrs={'id': 'id_course'})  # Set the id here
    )
    students = forms.ModelMultipleChoiceField(queryset=Contact.objects.none(), required=True, widget=forms.SelectMultiple(attrs={'id': 'id_students'}))

    def __init__(self, *args, **kwargs):
        super(CourseRegistrationForm, self).__init__(*args, **kwargs)

        # If the course is selected, populate the students queryset
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                # Get all students who are not already registered in the selected course
                registered_students = CourseContactMapping.objects.filter(course_id=course_id).values_list('contact_id', flat=True)
                self.fields['students'].queryset = Contact.objects.filter(role_id__role_type='Student').exclude(id__in=registered_students)
            except (ValueError, TypeError):
                self.fields['students'].queryset = Contact.objects.filter(role_id__role_type='Student')
        else:
            # Default: Show all students if no course is selected
            self.fields['students'].queryset = Contact.objects.filter(role_id__role_type='Student')

