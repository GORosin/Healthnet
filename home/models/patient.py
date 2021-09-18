from django.db import models
from django.contrib.auth.models import User, Group, Permission
from .activity import Activity
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
"""
This file is the model for the patient in the Healthnet website
It houses the patient class, medicalInfo class, contact info class and their methods
Author: Stephen Cook
Language: Python 3.4.3 and Django 1.9.1
"""

"""
This is a class representing all important contact information for a patient
:atrb: Patient_ID:  The ID of the patient
:atrb: address:     The patient's current address
:atrb: phone:       The patient's phone number
:atrb: c_states:    The possible choices for states
:atrb: state:       The patient's current state. Not Healthnet currently only supports American Users
:atrb: zip:         The patient's zip code
:atrb: city:        The city or town of the user
"""
class ContactInfo(models.Model):
    Patient_ID = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=10,default='')
    c_states = (
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MP', 'Northern Mariana Islands'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ','New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VI', 'Virgin Islands'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    )
    state = models.CharField(max_length=20, choices=c_states, default="")
    zip = models.CharField(max_length= 5,default="")
    city = models.CharField(max_length= 30, default="")

    """
    A too string used to quickly reference information
    """
    def __str__(self):
        return self.Patient_ID + " contact"
    """
    Updates the current patient's contact information. Current version replaces all aspects of contact information
    :arg
        contact_from:   cleaned_data from the ContactUserForm representing the users new contact information
    """
    def Update(self,contact_form):
            self.address=contact_form['address']
            self.phone=contact_form['phone']
            self.state=contact_form['state']
            self.zip=contact_form['zip']
            self.city=contact_form['city']
            self.save()

"""
This is a class repersenting all important medical information for a patient
:atrb: medical_ID:  The associated ID of a patient
:atrb: c_sex:       The choices for sex
:atrb: blood_Type_c The choice for blood type
:atrb: sex:         The patients sex
:atrb: weight:      The patient's weight
:atrb: height:      The patinet's hieght
:atrb: blood_Type:  The patient's blood type
"""
class MedicalInfo(models.Model):
    medical_ID = models.CharField(max_length=20, default='')
    c_sex = (
        ("M", "Male"),
        ("F", "Female")
    )
    blood_Type_c = (
        ("A+","A+"),("A-","A-"),("B+","B+"),
        ("B-","B-"), ("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-")
    )
    sex = models.CharField(max_length= 1, choices=c_sex, default='')
    weight = models.CharField(max_length=3, default='')
    height = models.CharField(max_length=3, default='')
    blood_Type = models.CharField(max_length=3, choices=blood_Type_c, default='')

    def Update(self,medical_form):
        self.blood_Type = medical_form['blood_Type']
        self.weight = medical_form['weight']
        self.height = medical_form['height']
        self.sex =  medical_form['sex']
        self.save()
    """
    Returns a string for admin
    """
    def __str__(self):
        return self.medical_ID + " medical"

"""
A class used to represent the Patient.
:atrb: name:        The name of the Patient.
:atrb: username:    The patients username, used to easily describe info
:atrb: DOB:         Users date of Birth
:atrb: hospital:    The name of the hospital the user is in
:atrb: contact:     The users contact information
:atrb: medical:     The users medical information
"""
class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    username = models.CharField(max_length=100, default="")
    name = models.CharField(blank=False, default="",max_length=200)
    DOB = models.DateField(blank=False,default=datetime.now)
    # hospital = models.CharField(max_length=100,blank=False)
    #sets the contact information
    contact = models.ForeignKey(
        ContactInfo,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )
    #sets a medical class
    medical = models.ForeignKey(
        MedicalInfo,
        on_delete=models.CASCADE,
        default=None,
        blank=False
    )

    """
    Creates a to string
    """
    def __str__(self):
        return self.user.username

    """
    Creates a patient using form data. This allows the system to creates
    a patient with user info and associated to a user
    :arg
        user_form:      cleaned_data representing user info
        patient_form    cleaned_data representing patient info
        contact_form    cleaned_data representing contact info
        medical_form    cleaned_data representing medical info
    """
    def createPatient(user_form, patient_form, contact_form, medical_form,user):
        #Creates the user profile.
        credentials = User.objects.create_user(
            first_name=user_form['first_name'],
            last_name=user_form['last_name'],
            username=user_form['username'],
            email=user_form['email'],
            password=user_form['password'],
        )
        contact = ContactInfo(
            Patient_ID= user_form['username'],
            address = contact_form['address'],
            phone = contact_form['phone'],
            state = contact_form['state'],
            zip = contact_form['zip'],
            city = contact_form['city']

        )
        #saves the contact
        contact.save()
        medical = MedicalInfo(
            medical_ID = user_form['username'],
            sex = medical_form['sex'],
            weight = medical_form['weight'],
            height = medical_form['height'],
            blood_Type = medical_form['blood_Type']

        )
        medical.save()
        patient = Patient(
            user=credentials,
            name=user_form['first_name'] +" " + user_form['last_name'],
            DOB=patient_form['DOB'],
            contact=contact,
            medical = medical,
            username = user_form['username'],
        )
        patient.save()
        if user == '':
            Activity.createActivity(datetime.now(),"User self registered: ", credentials.username,user)
        else:
            Activity.createActivity(datetime.now(), "created a new patient: ", credentials.username, user)
        return patient
    """
    Updates the contact information
    :arg
        contact_form:   the cleaned data representing the new contact information
    """
    def UpdateContact(self,contact_form,user):
        self.contact.Update(contact_form)
        Activity.createActivity(datetime.now(),"Updated contact information: ",self.username,'')
        return self
    def UpdateMedical(self,medical_form,user):
        self.medical.Update(medical_form)
        Activity.createActivity(datetime.now(),"updated medical for",self.username,user)
        return self
    # def setPermissions(self):
    #     permission = Permissions.objects.create(
    #         codename = 'no_edit_medical'
    #     )
    #     self.user.user_permissions.add(permission)