from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import sqlite3

"""
This class represents activity objects. It stores information based on actions in other class methods.
:atrb: timestamp: Time when activity was done.
:atrb: User_ID: Identification of the user that performed the activity.
:atrb: Effected_ID: Identification of the user affected by the activity (can be same as User_ID)
:atrb: Activity_Details: Description of the action performed.
"""
class Activity(models.Model):
    timestamp = models.DateTimeField(default=timezone.now())
    User_ID = models.CharField(max_length=100, default='')
    Effected_ID = models.CharField(max_length=100, default='')
    Activity_Details = models.TextField(default="")
    def getActivity(self):
        return self.Activity_Details
    def getTime(self):
        return self.timestamp
    #Used to sort the database in time order such that the user can view the activity log by most recent date.
    def sortTable(self):
        sqlite_file = 'db.sqlite3'
        table_name = 'home_activity'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('SELECT * FROM {home_activity} ORDER BY -{timestamp}')
    #creates a new activity object for other methods to use
    def createActivity(time, details,User_ID,user):
        activity = Activity (
            Effected_ID = User_ID,
            User_ID = user,
            timestamp = time,
            Activity_Details = details,        )
        activity.save()
    #creates a toString
    def __str__(self):
        return "Time: "+str(self.timestamp)+" | Details: "+str(self.Activity_Details)