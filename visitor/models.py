# visitor/models.py
from django.db import models
from datetime import datetime

class PersonToVisit(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    person_to_visit = models.ForeignKey(PersonToVisit, on_delete=models.CASCADE)
    login_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    signout_date = models.DateTimeField(blank=True, null=True)
    is_signin = models.BooleanField(default=True, blank=True, null=True)
    is_signout = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name
