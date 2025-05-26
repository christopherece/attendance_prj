# visitor/forms.py
from django import forms
from .models import Child, Attendance, Teacher
from datetime import datetime

class AttendanceForm(forms.ModelForm):
    child = forms.ModelChoiceField(
        queryset=Child.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parent_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    class Meta:
        model = Attendance
        fields = ['child', 'parent_name', 'notes']

class ChildForm(forms.ModelForm):
    class_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parent_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Child
        fields = ['name', 'class_name', 'parent_email', 'teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].widget.attrs.update({'class': 'form-control'})

class TeacherForm(forms.ModelForm):
    class_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Teacher
        fields = ['name', 'class_name', 'email']
