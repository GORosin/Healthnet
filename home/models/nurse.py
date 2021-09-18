from django.db import models
from django.contrib.auth.models import User
from .activity import Activity

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name     = models.CharField (max_length = 50,  default = '')
    email    = models.CharField (max_length = 100, default = '')
    phone    = models.CharField (max_length = 10 , default = '')
    #hospital = models.ForeignKey(Hospital,on_delete = models.CASCADE, default = None)
    #calendar = models.ForeignKey(AppointmentCalendar, on_delete = models.CASCADE, default = None)

    def viewCalendar(self):
        pass

    def editAppointment(self, Appointment, field, newData):
        newactivity = Activity.createActivity(self,datetime.now(),str(Appointment)+"Appointment Edited")
        newactivity.save()
        pass

    def createAppointment(self, date, place, involved, description = ""):
        newactivity = Activity.createActivity(self,datetime.now(),str(Appointment)+"Appointment Created")
        newactivity.save()
        pass

    def viewMedical(self, patient_ID):
        pass

    def updateMedical(self, patient_ID, field, newData):
        newactivity = Activity.createActivity(self,datetime.now(),"Updated Medical")
        newactivity.save()
        pass

    def admission(self, patient_ID):
        self.hospital.admitPatient(patient_ID)

    def discharge(self, patient_ID):
        self.hospital.dischargePatient(patient_ID)

    def __str__(self):
        return self.user.username