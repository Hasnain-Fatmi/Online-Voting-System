from django.contrib import admin
from HomePage.models import *
from django.utils import timezone
# Register your models here.


class VotersInfo(admin.ModelAdmin):
    list_display=('First_Name','Last_Name', 'Email', 'CNIC', 'Address', 'Phone_Number', 'Gender',  'Password')
    list_filter = ('CNIC', 'Gender')
    search_fields = ('First_Name','CNIC')

class CandidatesApplicationInfo(admin.ModelAdmin):
    list_display = ('First_Name', 'Last_Name', 'Father_Name', 'CNIC', 'Gender', 'Age','Email', 'Phone_Number','Address', 'City', 'Nationalities', 'Party', 'symbol')
    list_filter = ('CNIC', 'Gender', 'Age', 'City', 'Party','symbol')
    search_fields = ('First_Name','CNIC', 'Gender', 'Age', 'City', 'Party','symbol')

class PositionInfo(admin.ModelAdmin):
    list_display = ('title','total_vote')
    search_fields = ('title',)
    
class CandidatesInfo(admin.ModelAdmin):
    list_display = ('name','position', 'total_vote')
    list_filter = ('position',)
    search_fields = ('name','position')
    readonly_fields = ('total_vote',)

class VotingTime(admin.ModelAdmin):
    list_display = ('start_datetime', 'end_datetime', 'current_time')  #Add 'current_time' here

    def current_time(self, obj):
        return timezone.now().strftime("%Y-%m-%d %H:%M:%S")  #Format the current time as needed
    
class ResultTime(admin.ModelAdmin):
    list_display = ('result_time',)  
        
admin.site.register(Voter, VotersInfo)
admin.site.register(Candidate_Application,CandidatesApplicationInfo)
admin.site.register(Position,PositionInfo)
admin.site.register(Candidate,CandidatesInfo)
admin.site.register(VotingPeriod, VotingTime)
admin.site.register(PublishResults, ResultTime)
