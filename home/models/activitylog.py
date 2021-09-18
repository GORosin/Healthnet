from django.db import models
from django.utils import timezone
from .activity import Activity

class ActivityLog(models.Model):
	activities = Activity.objects.all()

	def displayLog(self):
		pass

	#return log
	def addActivity(self):
		#log.append(self)
		pass

	def resetLog(self):
		time = models.DateTimeField()
		return time

	def __str__(self):
		return self.activities
