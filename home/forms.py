from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =['username','password','password_confirm','email','first_name','last_name']

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['DOB',]

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['dateTime', 'office', 'patient_ID', 'doctor_ID', 'description']


class ContactUserForm(forms.ModelForm):
    phone = forms.RegexField(regex=r'^\+?1?\d{10}$')
    zip = forms.RegexField(regex= r'^\+?1?\d{5}')
    class Meta:
        model = ContactInfo
        fields = ['address','city','state','zip','phone']

class MedicalUserForm(forms.ModelForm):
    weight = forms.RegexField(regex=r'^\+?1?\d{1,3}')
    height = forms.RegexField(regex=r'^\+?1?\d{2,3}')
    class Meta:
        model = MedicalInfo
        fields = ['sex','weight','height','blood_Type']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']
