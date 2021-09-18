from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.generic import View
from datetime import datetime
from .models import *
from .forms import *

"""
This creates the index/homepage of Healthnet.
This is where initial navigation happens
"""
def index(request):
    return render(request, "home/index.html")

#======List Views=======================================================================================================
"""
A Class representing a generic list of all patients in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class PatientView(generic.ListView):
   template_name = 'home/patient/patient.html'
   context_object_name = "patient_list"
   """
   Gets the context_object. This is all patients
   """
   def get_queryset(self):
        return Patient.objects.all()
"""
A Class representing a generic list of all admin in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class AdministratorView(generic.ListView):
    template_name = 'home/administrator.html'
    context_object_name = "administrator_list"
    """
    This method gets and returns all administrators
    """
    def get_queryset(self):
        return User.objects.filter(is_superuser = True)
"""
A Class representing a generic list of all Doctors in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class DoctorView(generic.ListView):
    template_name = 'home/doctor.html'
    context_object_name = "doctor_list"
    """
    Gets and returns a list of all doctors
    """
    def get_queryset(self):
        return Doctor.objects.all()
"""
A Class representing a generic list of all Nurses in the system
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class NurseView(generic.ListView):
    template_name = 'home/nurse.html'
    context_object_name = "nurse_list"
    """
    Gets and Returns all nurses
    """
    def get_queryset(self):
        return Nurse.objects.all()
"""
A Class representing a generic list of all Activities in the Activity Log
This List is of usernames, This may change in future
Accessible by anyone if logged in
"""
class ActivityView(generic.ListView):
    template_name = 'home/activities.html'
    context_object_name = "activity_list"
    """
    Returns the activity log
    """
    def get_queryset(self):
        today = datetime.now()
        return Activity.objects.filter(timestamp__year=today.year).order_by('-timestamp')
#======End List Views===================================================================================================

#======Detail Views=====================================================================================================
"""
This view is used when a user clicks on a patient's username
It gets all relevant User information and renders it using the context below
:arg
    patient_id: The id number of the patient, used to gather the information
:returns: a render of the user information page
"""
def pDetail(request,patient_id):
    patient = get_object_or_404(Patient, pk = patient_id)
    #gets the patient
    phone = patient.contact.phone
    phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone) #formats phone
    weight = patient.medical.weight + " lb"
    doctors = Doctor.objects.all()
    doctorlist = []
    for doctor in doctors:
        doctorlist.append(doctor.user.username)
    nurses = Nurse.objects.all()
    for nurse in nurses:
        doctorlist.append(nurse.user.username)
    #these 4 lines are used to format the hieght
    if len(patient.medical.height) == 2:
        height = """ %s'%s" """ % tuple(patient.medical.height)
    else:
        height = """ %s'%s%s" """ % tuple(patient.medical.height)
    context = {
        'name': patient.name,
        'username': patient.username,
        'DOB': patient.DOB,
        'address': patient.contact.address,
        'city': patient.contact.city,
        'state': patient.contact.state,
        'zip': patient.contact.zip,
        'phone': phone,
        'email': patient.user.email,
        'patient': patient,
        'weight': weight,
        'height': height,
        'doctorlist': doctorlist
    }
    return render(request, "home/patient/patientDetail.html", context)

"""
This View is used to when a user clicks a Doctor's ID number
This displays all relevant class information
:arg
    doctor_id: the id number of the doctor
:returns: a render of the doctors info
"""
def dDetail(request,doctor_id):
    doctor = get_object_or_404(Doctor,pk = doctor_id)
    phone = doctor.phone
    phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone)  # formats phone
    return render(request,"home/doctorDetail.html", {'doctor': doctor, 'phone': phone})

def nDetail(request,nurse_id):
    nurse = get_object_or_404(Nurse,pk = nurse_id)
    phone = nurse.phone
    phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(phone)  # formats phone
    return render(request,"home/nDetail.html", {'nurse': nurse, 'phone': phone})
#======End Detail Views=================================================================================================

#======Registration and Update Views====================================================================================
class RegistrationForm(View):
    template_name='home/patient/register.html'
    # Displays signup form
    def get(self,request):
        user_form= UserForm
        patient_form = PatientUserForm
        contact_form = ContactUserForm
        medical_form = MedicalUserForm
        return render(request, self.template_name,{'user_form': user_form, 'patient_form': patient_form, 'contact_form':contact_form, 'medical_form': medical_form})
    #regesters a user
    def post(self,request):
        user_form = UserForm(request.POST)
        patient_form = PatientUserForm(request.POST)
        contact_form = ContactUserForm(request.POST)
        medical_form = MedicalUserForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid() and contact_form.is_valid() and medical_form.is_valid():
            user_form_cleaned =  user_form.cleaned_data
            patient_form_cleaned = patient_form.cleaned_data
            contact_form_cleaned = contact_form.cleaned_data
            medical_form_cleaned  = medical_form.cleaned_data
            patient = Patient.createPatient(user_form_cleaned, patient_form_cleaned, contact_form_cleaned, medical_form_cleaned,request.user.username)
            patient.save()
            return redirect('home:login')
        else:
            return render(request, self.template_name, {'user_form': user_form, 'patient_form': patient_form, 'contact_form': contact_form, 'medical_form': medical_form})

class ContactEditForm(View):
    template_name = 'home/patient/contactU.html'

    def get(self, request,patient_id):
        #if request.user.is_authenticated:
            patient = get_object_or_404(Patient, pk=patient_id)
            contact_form = ContactUserForm(initial={
                "address": patient.contact.address, "city": patient.contact.city, "state": patient.contact.state,
                "zip": patient.contact.zip, 'phone': patient.contact.phone})

            return render(request, self.template_name,{'contact_form': contact_form, 'patient': patient})
       # else:
        #    return HttpResponse("Login to edit")

    def post(self,request,patient_id):
       # if request.user.is_authenticated:
            patient = get_object_or_404(Patient, pk=patient_id)
            contact_form = ContactUserForm(request.POST)
            if contact_form.is_valid():
                contact_form_clean = contact_form.cleaned_data
                patient = patient.UpdateContact(contact_form_clean,request.user.username)
                patient.save()
                return redirect('home:pDetail', patient_id)
            else:
                return render(request, self.template_name,
                              {'contact_form': contact_form, 'patient': patient})

class MedicalEditForm(View):
    template_name = 'home/patient/updateM.html'

    def get(self, request, patient_id):
        # if request.user.is_authenticated:
        doctors = Doctor.objects.all()
        doctorlist = []
        for doctor in doctors:
            doctorlist.append(doctor.user.username)
        nurses = Nurse.objects.all()
        for nurse in nurses:
            doctorlist.append(nurse.user.username)
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_form = MedicalUserForm(initial={
            "sex": patient.medical.sex, "height": patient.medical.height, "weight": patient.medical.weight,
            "blood_Type": patient.medical.blood_Type})
        return render(request, self.template_name, {'medical_form': medical_form, 'patient': patient, 'doctorlist': doctorlist})
        # else:
        #    return HttpResponse("Login to edit")

    def post(self, request, patient_id):
        # if request.user.is_authenticated:
        patient = get_object_or_404(Patient, pk=patient_id)
        medical_form = MedicalUserForm(request.POST)
        if medical_form.is_valid():
            medical_form_clean = medical_form.cleaned_data
            patient = patient.UpdateMedical(medical_form_clean,request.user.username)
            patient.save()
            return redirect('home:pDetail', patient_id)
        else:
            return render(request, self.template_name,
                          {'contact_form': medical_form, 'patient': patient})


#======End Registration and Update Views================================================================================

#======Login and Logout Views===========================================================================================
class LoginView(View):
    template_name = 'home/login/login.html'
    def get(self,request):
        login_info = LoginForm()
        return render(request,self.template_name,{'form': LoginForm})
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        HttpResponse()
        user = authenticate(username = username,password = password)
        if user is not None:
            Activity.createActivity(datetime.now(), "Logged in:",username, "")
            login(request,user)
            return redirect('home:index')
        else:
            return render(request,'home/login/failure.html',{'login_form':LoginForm})

class LogOutView(View):
    def get(self,request):
        Activity.createActivity(datetime.now(), "Logged out:", request.user.username, "")
        logout(request)
        return redirect('home:index')
#======End Login and Logout Views=======================================================================================

class newAppointment(View):
    template_name = 'home/appointment.html'
    def get(self, request):
        appointment_form = AppointmentForm
        return render(request, self.template_name, {'appointment_form': appointment_form})

    def post(self, request):
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form_cleaned = appointment_form.cleaned_data
            appointment = Appointment.createAppoinment(appointment_form_cleaned)
            appointment.save()
            return redirect('home:appointment')
        else:
            return render(request, self.template_name, {'appointment_form': appointment_form, 'error': True})