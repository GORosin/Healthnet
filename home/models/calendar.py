from django.db import models
from datetime import datetime
class Appointment(models.Model):
    dateTime = models.DateTimeField(blank= False, default=datetime.now)           #appointment date and time
    office = models.IntegerField('Room number:')    #office number of the doctor
    patient_ID = models.CharField(max_length=20, default='')    #patient user ID
    doctor_ID = models.CharField(max_length=20, default='')     #doctor user ID
    description = models.CharField(max_length=100, default='')  #description for the appointment

    def editTime(dateTime):
        pass

    def editDescription(description):
        pass

    def editLocation(office):
        pass

    def editPatient(patient_ID):
        pass

    def editDoctor(doctor_ID):
        pass

    def createAppoinment(appointment_form):
        appointment = Appointment(
            dateTime=appointment_form['dateTime'],
            office=appointment_form['office'],
            patient_ID=appointment_form['patient_ID'],
            doctor_ID=appointment_form['doctor_ID'],
            description=appointment_form['description']
        )
        appointment.save()
        return appointment

    def __str__(self):
        tostr = ""
        tostr += self.dateTime + " at office No." + self.office + "\n"
        tostr += " Patient ID: " + self.patient_ID + "\n Doctor ID: " + self.doctor_ID + "\n"
        tostr += "  Description: " + self.description
        return tostr

class Calendar(models.Model):
    Appointments = Appointment.objects.all
    User_ID = models.CharField(max_length=20, default='')


    def cancelAppointment(dateTime):
        pass

    def editAppointment(editState):
        pass

    def __str__(self):
        return self.User_ID