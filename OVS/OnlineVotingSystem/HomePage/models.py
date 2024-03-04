from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Voter(models.Model):
    First_Name=models.TextField(max_length=20)
    Last_Name=models.TextField(max_length=20)
    Email = models.TextField(max_length=30)
    CNIC=models.TextField(max_length=13)
    Address=models.TextField()
    Phone_Number=models.TextField(max_length=11)
    Gender=models.TextField(max_length=6)
    Password=models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter', null=True)



class Candidate_Application(models.Model):
    Candidate_Picture = models.ImageField(verbose_name="Candidate Pic", upload_to='candidate_images/', blank=True, null=True) 
    Symbol_Picture = models.ImageField(verbose_name="Symbol Pic", upload_to='symbol_images/', blank=True, null=True) 
    First_Name=models.CharField(max_length=20)
    Last_Name=models.CharField(max_length=20)
    Father_Name=models.CharField(max_length=20)
    Email = models.CharField(max_length=50)
    CNIC=models.CharField(max_length=13)
    Address=models.TextField()
    City=models.CharField(max_length=13)
    Phone_Number=models.CharField(max_length=11)
    Gender=models.CharField(max_length=6)
    Age=models.CharField(max_length=6)
    Nationalities=models.TextField()
    Party=models.CharField(max_length=15)
    symbol=models.CharField(max_length=15)
    disclaimer = models.TextField(default="NULL")

class Position(models.Model):
    # The title field is used to store the position title
    title = models.CharField(max_length=20, unique=True)
    total_vote = models.IntegerField(default=0, editable=False)
    def __str__(self):
        return self.title

    
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    Email=models.CharField(max_length=30)
    CNIC=models.CharField(max_length=13)
    Party=models.CharField(max_length=15)
    symbol=models.CharField(max_length=15)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Candidate Pic", upload_to='images/')
    total_vote = models.IntegerField(default=0, editable=False)
    
    def __str__(self):
        return "{} - {}".format(self.name, self.position.title)  
        
    def increment_position_vote(self):
        self.position.total_vote += 1
        self.position.save() 



# The ControlVote model is used to create the control_vote table
class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, default=1)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,self.candidate,self.position, self.status, self.timestamp)
    
    
class VotingPeriod(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def _str_(self):
        return f"{self.start_datetime} to {self.end_datetime}"
    

class PublishResults(models.Model):
    result_time = models.DateTimeField()
    def _str_(self):
        return f"{self.result_time}"