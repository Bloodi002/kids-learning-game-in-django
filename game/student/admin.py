from django.contrib import admin
from .models import Role, Contact, Course, ProblemLevel, ProblemType, Problem, ProblemScoreMapping, CourseContactMapping
# Register your models here.

admin.site.register(Role)
admin.site.register(Contact)
admin.site.register(Course)
admin.site.register(ProblemLevel)
admin.site.register(ProblemType)
admin.site.register(ProblemScoreMapping)
admin.site.register(CourseContactMapping)
admin.site.register(Problem)