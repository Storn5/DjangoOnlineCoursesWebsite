from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, related_name='teacher', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='students')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'courses'
        ordering = ['name']

class App(models.Model):
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    def __str__(self):
        return str(self.course) + ' ' + str(self.student)
    class Meta:
        db_table = 'applications'
        ordering = ['course', 'student', 'status']