from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(MedicalInfo)
# admin.site.register(ContactInfo)
admin.site.register(Nurse)
admin.site.register(Doctor)
# admin.site.register(Administrator)
admin.site.register(Activity)
