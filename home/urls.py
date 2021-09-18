from django.conf.urls import url
from . import views

app_name='home'
urlpatterns = [
    # ex: /home/
    url(r'^$', views.index, name='index'),
    # ex: /home/patient/
    url(r'^patient/$', views.PatientView.as_view(), name='patient'),
    # ex: /home/administrator
    url(r'^administrator/$', views.AdministratorView.as_view(), name='administrator'),
    # ex: /home/doctor/
    url(r'doctor/$', views.DoctorView.as_view(), name='doctor'),
    # ex: /home/nurse
    url(r'^nurse/$',views.NurseView.as_view(), name='nurse'),
    # ex: home/patient/1
    url(r'^patient/(?P<patient_id>[0-9]+)/$', views.pDetail, name='pDetail'),
    # ex: home/doctor/1
    url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.dDetail, name='dDetail'),
    url(r'^nurse/(?P<nurse_id>[0-9]+)/$', views.nDetail, name='nDetail'),
    # ex: home/register/
    url(r'register/', views.RegistrationForm.as_view(), name='register'),
    # ex: home/activities/
    url(r'activities/', views.ActivityView.as_view(), name='activities'),
    # ex: /polls/5/contact
    url(r'^(?P<patient_id>[0-9]+)/contact/$',views.ContactEditForm.as_view(), name='contact'),
    url(r'^(?P<patient_id>[0-9]+)/medical/$',views.MedicalEditForm.as_view(), name='medical'),
    url(r'login/$', views.LoginView.as_view(),name='login'),
    url(r'logout/$', views.LogOutView.as_view(),name='logout'),
    url(r'appointment/$', views.newAppointment.as_view(), name='appointment')
]