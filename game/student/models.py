from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_type = models.CharField(max_length=32)

    def __str__(self):
        return self.role_type

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_id = models.EmailField(max_length = 254)
    mobile_number = models.CharField(max_length=12)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.email_id}'