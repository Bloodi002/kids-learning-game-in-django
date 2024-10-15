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
        return f'{self.course_id}'


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_id = models.EmailField(max_length=254)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.email_id}'
    

class ProblemType(models.Model):
    problem_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class ProblemLevel(models.Model):
    problem_level_id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=100)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE, null=True)
    symbol = models.CharField(max_length=50)

    def __str__(self):
        return f'Level: {self.level}, Problem Type: {self.problem_type.type}: {self.symbol}'

class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    problem_level_id = models.ForeignKey(ProblemLevel, on_delete=models.CASCADE)
    statement = models.TextField()
    max_score = models.IntegerField()
    min_score = models.IntegerField()
    answer = models.CharField(max_length=10, null=True)
    time_bound = models.DurationField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    symbol_position = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.statement


class ProblemScoreMapping(models.Model):
    problem_score_mapping_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    score = models.IntegerField()
    student_answered = models.IntegerField(null=True)

    def __str__(self):
        return f'Contact: {self.contact_id}, Problem: {self.problem_id}, Score: {self.score}'


class CourseContactMapping(models.Model):
    course_contact_mapping_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contact_id}'
    
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.correct_answers} correct answers"