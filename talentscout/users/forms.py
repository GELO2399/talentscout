from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# 🟢 User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skills', 'experience', 'education', 'resume']

# 🟢 Employer Signup Form
class EmployerSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    company_name = forms.CharField(label='Company Name', max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'company_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Create UserProfile directly here with employer flag
            UserProfile.objects.create(
                user=user, 
                is_employer=True, 
                company_name=self.cleaned_data["company_name"]
            )
        return user
