# models.py
from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=255,default="s")
   
    def __str__(self):
        return self.course_name

class Students(models.Model):
    student_id = models.CharField(max_length=100)
    student_name = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)

def __str__(self):
        return self.students_name

class ExamSchedule(models.Model):
    course_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    start_date = models.DateField()
    exam_date = models.DateField()

    def __str__(self):
        return f'{self.student_name} - {self.course_name}'

