# visitor/models.py
from django.db import models
from datetime import datetime

class Child(models.Model):
    name = models.CharField(max_length=100)
    parent_email = models.EmailField(blank=True, null=True)
    class_name = models.CharField(max_length=50, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    class_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    parent_name = models.CharField(max_length=100)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=datetime.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    is_checked_in = models.BooleanField(default=True)
    is_checked_out = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parent_name} - {self.child.name}"

    @property
    def duration(self):
        if self.check_out_time:
            return self.check_out_time - self.check_in_time
        return None
