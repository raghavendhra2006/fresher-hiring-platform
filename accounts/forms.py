from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('fresher', 'Candidate'),
        ('hr', 'HR Recruiter'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="I am joining as a:")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'fresher':
            user.is_fresher = True
        elif role == 'hr':
            user.is_hr = True
            
        if commit:
            user.save()
        return user
