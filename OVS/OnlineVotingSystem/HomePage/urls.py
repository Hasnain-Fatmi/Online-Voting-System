from django.contrib import admin
from django.urls import path, include
from HomePage import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

# Importing the required modules
# The admin module is used to create the admin site for the application
# using the default django admin site module

# The path module is used to create the url patterns for the application
# to map the urls to the views

# The views module is used to import the views from the views.py file
# The settings module is used to import the settings from the settings.py file
# to get the media, static files and other settings
# The static module is used to import the static files from the settings.py file

urlpatterns = [
    path('',views.home, name="home"),
    path('registeration', views.voterRegisteration, name="register"),
    path('login', views.voterLogin, name="login"),
    path('contact', views.contact, name="contact"),
    path('complaint', views.complaint, name="complaint"),
    path('help/', views.help, name="help"),
    path('forgetPassword', views.forgetPassword, name="forgetPassword"),
    path('registrationComplete', views.voterRegistrationComplete, name="registrationComplete"),
    path('services', views.services, name="services"),
    path('team', views.team, name="team"),
    path('voterPage', views.voterPage, name="voterPage"),
    path('logoutview', views.logoutview, name='logoutview'),
    path('terms', views.candidateTermsAndConditions, name="terms"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),  
    path('activationFailed', views.activationFailed, name="activationFailed"),
    path('candidate_registration', views.candidateRegistration, name="candidate_registration"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('result/', views.resultView, name='result'),
    path('candidateRegistrationComplete/', views.candidateRegComplete, name='candidateRegistrationComplete'),
    path('voteDone/', views.voteDone, name='voteDone'),
    path('incorrectDetails', views.incorrectDetails, name='incorrectDetails'),
    path('Chart', views.custom_charts, name='Chart'),
    path('ballot/', views.ballot, name='ballot'), 
    path('resultNotAnnounced/', views.resultNotAnnounced, name='resultNotAnnounced'),
    path('passwordChange/', views.passwordChange, name='passwordChange'),
    path('profileChange/', views.profileChange, name='profileChange'),
    
    
    
]
