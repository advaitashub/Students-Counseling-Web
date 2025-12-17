from django import forms
from django.contrib.auth.models import User
from .models import StudentDetail, CustomUser

class MassAllotmentForm(forms.Form):
    min_percentage = forms.FloatField(label="Minimum Percentage")
    max_percentage = forms.FloatField(label="Maximum Percentage")
    branch_to_allot = forms.ChoiceField(
        choices=[('CSE', 'Computer Science'), ('ECE', 'Electronics'), ('ME', 'Mechanical')],
        label="Branch to Allot"
    )



class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': ' ',
        })
    )
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # encrypt password
        if commit:
            user.save()
        return user

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = '__all__'  # or list fields if you want
        exclude = ['user','rank','is_allotted','allotted_branch','fee_paid','offer_letter_generated']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address':forms.Textarea(attrs={
                'cols':20,
                'rows':3,
                'style':'resize:none;',
            })
        }
