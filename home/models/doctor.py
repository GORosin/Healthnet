from django.db import models
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from .patient import Patient
from django.contrib.contenttypes.models import ContentType
from .activity import Activity

class Doctor(models.Model):
    # attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None,)
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=10, default='')
    specialty = models.CharField(max_length=100,default='')
    office_hours_start = models.TimeField(default=timezone.now)
    office_hours_end = models.TimeField(default=timezone.now)
    office = models.IntegerField('Room number:')
    class Meta:
        permissions = (("view_medical", "can view medical"),
                       ("edit_medical", "can edit medical"))


    #Methods
    # def set_permissions(self):
    #
    #     self.user.user_permissions.add(permission)


    def viewCalendar(self):
        pass
    def createAppointment(self, date, place, involved, description = ""):
        newactivity = Activity.createActivity(self,timezone.now(),str(Appointment)+"Appointment Created")
        newactivity.save()
        pass
    def editAppointment(self, Appointment, field, newData):
        newactivity = Activity.createActivity(self,datetime.now(),str(Appointment)+"Appointment Edited")
        newactivity.save()
        pass
    def cancelAppointment(self,Appointment):
        newactivity = Activity.createActivity(self,datetime.now(),str(Appointment)+"Appointment Cancelled")
        newactivity.save()
        pass
    def viewMedical(self, patient_ID):
        pass
    def updateMedical(self, patient_ID, field, newData):
        newactivity = Activity.createActivity(self,datetime.now(),"Updated Medical")
        newactivity.save()
        pass
    def __str__(self):
        return self.user.username