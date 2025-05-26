# visitor/forms.py
from django import forms
from .models import PersonToVisit, Visitor
from datetime import date


class VisitorLoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Hidden field to store the selected person_to_visit ID
    person_to_visit_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    # Text input for searching staff
    person_to_visit_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type to search for staff...',
            'autocomplete': 'off'
        })
    )
    # The actual ModelChoiceField (hidden from the user)
    person_to_visit = forms.ModelChoiceField(
        queryset=PersonToVisit.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )
    # Updated submit method to handle form submission and save data
    def save(self, commit=True):
        if self.is_valid():
            name = self.cleaned_data['name']
            person_to_visit = self.cleaned_data['person_to_visit']
            
            # Create or get the visitor
            visitor, created = Visitor.objects.get_or_create(
                name=name,
                person_to_visit=person_to_visit
            )
            
            # Set is_signin to True and save
            visitor.is_signin = True
            visitor.login_date = datetime.now()
            if commit:
                visitor.save()
            
            return visitor
        return None
