from django.db import models
from .doctor import Doctor
from .patient import Patient
from .nurse import Nurse

class Hospital(models.Model):
    # attributes
    hospital_ID = models.CharField(max_length=20, default='')
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    nurses = Nurse.objects.all()

    #Methods
    def admitPatient(patient_ID):
        pass

    def dischargerPatient(paitent_ID):
        pass

    def transferPatient(patient_ID, hospital_ID):
        pass