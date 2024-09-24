from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Job,Company,Category,Location,Contact


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Username'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Email'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'onfocus': "this.placeholder = ''",
            'onblur': "this.placeholder = 'Password'",
            'required': 'required',
            'class': ' mb-5 single-input'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'onfocus': "this.placeholder = ''",
            'onblur': "this.placeholder = 'Confirm Password'",
            'required': 'required',
            'class': ' mb-5 single-input'
        })


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Job Title',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Job Title'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Description'",
                'required': 'required',
                'class': ' mb-5 single-textarea'
            }),
            'company': forms.Select(attrs={
                'class': ' mb-5 form-select',
                'id': 'default-select'
            }),
            'location': forms.Select(attrs={
                'class': ' mb-5 form-select',
                'id': 'default-select'
            }),
            'job_type': forms.Select(attrs={
                'class': ' mb-5 form-select',
                'id': 'default-select'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Salary',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Salary'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'application_deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': ' mb-5 single-input'
            }),
            'vacancies': forms.NumberInput(attrs={
                'placeholder': 'Vacancies',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Vacancies'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'required_knowledge_skills_abilities': forms.Textarea(attrs={
                'placeholder': 'Required Knowledge, Skills, and Abilities',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Required Knowledge, Skills, and Abilities'",
                'required': 'required',
                'class': ' mb-5 single-textarea'
            }),
            'education_experience': forms.Textarea(attrs={
                'placeholder': 'Education and Experience',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Education and Experience'",
                'required': 'required',
                'class': ' mb-5 single-textarea'
            }),
            'min_experience_years': forms.NumberInput(attrs={
                'placeholder': 'Minimum Experience Years',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Minimum Experience Years'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'job_category': forms.Select(attrs={
                'class': ' mb-5 form-select',
                'id': 'default-select'
            }),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Company Name',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Company Name'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Email'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Phone'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'Website',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Website'",
                'class': ' mb-5 single-input'
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'About',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'About'",
                'class': ' mb-5 single-textarea'
            }),
            'verified': forms.CheckboxInput(attrs={
                'class': ' mb-5'
            }),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields ="__all__"
        widgets = {
            'country': forms.TextInput(attrs={
                'placeholder': 'Country',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Country'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'City'",
                'required': 'required',
                'class': ' mb-5 single-input'
            })
         }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category Name',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Category Name'",
                'required': 'required',
                'class': ' mb-5 single-input'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': ' mb-5 form-control-file'
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Full Name'",
                'required': 'required',
                'class': 'mb-5 single-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Email'",
                'required': 'required',
                'class': 'mb-5 single-input'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Subject'",
                'required': 'required',
                'class': 'mb-5 single-input'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Your Message'",
                'required': 'required',
                'class': 'mb-5 single-input'
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job', 'full_name', 'age', 'city',"email", 'resume', 'cover_letter']
        widgets = {
            'job': forms.HiddenInput(),
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Full Name'",
                'class': 'mb-5 single-input'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Age',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Age'",
                'class': 'mb-5 single-input'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'City'",
                'class': 'mb-5 single-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Email'",
                'required': 'required',
                'class': 'mb-5 single-input'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'mb-5 single-input'
            }),
            'cover_letter': forms.Textarea(attrs={
                'placeholder': 'Cover Letter',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Cover Letter'",
                'class': 'mb-5 single-input'
            })
        }
