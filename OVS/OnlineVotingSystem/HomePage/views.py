from OnlineVotingSystem import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from . models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token 
from HomePage.models import Voter, Candidate_Application
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.contrib.auth import update_session_auth_hash




def home(request):
    return render(request,"HomePage/homePage.html")

def services(request):
    return render(request,"Others/services.html")

def help(request):
    return render(request,"Others/help.html")

def contact(request):
    return render(request,"Others/contact.html")

def complaint(request):
    return render(request,"Others/complaint.html")

def team(request):
    return render(request,"Others/team.html")

def voterRegisteration(request):
    
    if request.method=="POST":
        
        FirstName=request.POST.get('firstName')
        LastName=request.POST.get('lastName')
        Email=request.POST.get('emailAddress')
        CNIC=request.POST.get('cnicNum')
        Address=request.POST.get('address')
        DOB=request.POST.get('date')
        PhoneNum=request.POST.get('phone')
        Gender=request.POST.get('gender')
        Pass1=request.POST.get('password')
        Pass2=request.POST.get('confirmPassword')
               
        myUser = User.objects.create_user(FirstName,Email,Pass1)
        
        myVoter = Voter(
            First_Name=FirstName,
            Last_Name=LastName,
            Email=Email,
            CNIC=CNIC,
            Address=Address,
            Phone_Number=PhoneNum,
            Gender=Gender,
            Password=Pass1
        )  
            
        myUser.first_name= FirstName
        myUser.last_name=LastName
        myUser.username=Email
        myUser.is_active = False       
        myUser.save()
        myVoter.save()     
        sendConfirmationEmail(request, myUser)

        return redirect('registrationComplete')
    return render(request,"Voter Registration/registration.html")


@login_required
def candidateRegistration(request):
    if request.method == 'POST':
        CandidatePicture = request.FILES.get('candidate_picture')
        SymbolPicture = request.FILES.get('symbol_picture')
        FirstName=request.POST.get('firstName')
        LastName=request.POST.get('lastName')
        FatherName=request.POST.get('fatherName')
        Email=request.POST.get('email')
        CNIC=request.POST.get('cnic')
        Address=request.POST.get('address')
        City=request.POST.get('city')
        PhoneNumber=request.POST.get('phone')
        Gender=request.POST.get('gender')
        Age=request.POST.get('age')
        Nationality=request.POST.get('nationality')
        Party=request.POST.get('party')
        Symbol=request.POST.get('symbol')
        disclaimer=request.POST.get('legal_disclaimer')
        
        myCandidate = Candidate_Application(
            Candidate_Picture=CandidatePicture,
            Symbol_Picture=SymbolPicture,
            First_Name=FirstName,
            Last_Name=LastName,
            Father_Name=FatherName,
            Email=Email,
            CNIC=CNIC,
            Address=Address,
            City=City,
            Phone_Number=PhoneNumber,
            Gender=Gender,
            Age=Age,
            Nationalities=Nationality,
            Party=Party,
            symbol= Symbol,
            disclaimer=disclaimer
           
        )  
        myCandidate.save()
        
        return redirect('candidateRegistrationComplete')
    # Render the candidate registration form
    return render(request, "Candidate/candidateRegistration.html")


@login_required
def candidateTermsAndConditions(request):
    return render(request,"Candidate/termsAndConditions.html") 


@login_required
def candidateRegComplete(request):
    return render(request,"Candidate/candidateRegistrationComplete.html")

def sendConfirmationEmail(request, myUser):
    current_site = get_current_site(request)
    emailSubject = "Online Voting System - Confirm your Email"
    message2 = render_to_string('Voter Registration/confirmationEmail.html',{
            
            'name': myUser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser)
        })
    email = EmailMessage(
        emailSubject,
        message2,
        settings.EMAIL_HOST_USER,
        [myUser.email],
    )
    email.fail_silently = True
    email.send()
    
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        return redirect('login')
    else:
        return render(request,'registrationFailed.html')

def activationFailed(request):
    return render(request,"Voter Registration/registrationFailed.html")

def voterRegistrationComplete(request):
    return render(request,"Voter Registration/registrationComplete.html")

def voterLogin(request):
    
    if request.method=="POST":
        name=request.POST.get('firstName')
        pass1=request.POST.get('pass1')
        
        user=authenticate(username=name, password=pass1)
        
        if user is not None:  
             login(request, user)      
             return redirect('voterPage')
         
        else:
            messages.error(request,"invalid credentials")
            return redirect('incorrectDetails') 
        
    return render(request,"Login/login.html")


def incorrectDetails(request):
    return render(request,"Login/incorrectDetails.html")

def forgetPassword(request):
    return render(request,"Password Reset/password_reset.html")

@login_required
def logoutview(request):
    logout(request)
    return redirect('home')

@login_required     
def voterPage(request):
    try:
        # Retrieve the VotingPeriod instance (you might need to filter based on your requirements)
        voting_period = VotingPeriod.objects.first()

        if voting_period:
            # Get the current datetime
            current_datetime = timezone.now()

            if voting_period.start_datetime and voting_period.end_datetime:
                # Check if the current datetime is within the specified voting period
                if voting_period.start_datetime <= current_datetime <= voting_period.end_datetime:
                    is_voting_period = True
                    # Fetch the positions
                    obj = Position.objects.all()
                    start_time = None
                    end_time = None
                else:
                    is_voting_period = False
                    obj = None  # No positions available outside the voting period
                    start_time = voting_period.start_datetime
                    end_time = voting_period.end_datetime
            else:
                is_voting_period = False
                obj = None
                start_time = None
                end_time = None
        else:
            raise VotingPeriod.DoesNotExist
    except VotingPeriod.DoesNotExist:
        # Handle the scenario where no voting period exists
        # Set appropriate values or handle the absence of a voting period
        is_voting_period = False
        obj = None
        start_time = None
        end_time = None

    # Pass the necessary data to the template context
    context = {
        'obj': obj,
        'voting_period': voting_period,
        'current_datetime': timezone.now(),
        'is_voting_period': is_voting_period,
        'start_time': start_time,
        'end_time': end_time,
    }
    return render(request, "Voter Dashboard/voterPage.html", context)

        
@login_required
def voteDone(request):
     return render(request,"Voter Dashboard/voteDone.html")

@login_required
def positionView(request):
  
    obj = Position.objects.all()
    return render(request, "Voter Dashboard/position.html", {'obj':obj})

@login_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]
        if temp.status == False:
            # The temp2 variable is used to store the Candidate object
            # The total_vote of the candidate is incremented by 1
            # The status of the ControlVote object is changed to True
            # The user is redirected to the position page
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.increment_position_vote()  # Increment position vote count
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/voteDone/')
        else:
            messages.success(request, 'You have already voted for this position.')
            return render(request, 'Candidate/candidate.html', {'obj':obj})
    else:
        return render(request, 'Candidate/candidate.html', {'obj':obj})
    
@login_required
def candidateDetailView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "Candidate/candidate_detail.html", {'obj':obj})

@login_required
def resultView(request):
    publish_results = PublishResults.objects.first()

    if publish_results and timezone.now() < publish_results.result_time:
        return render(request, "Voter Dashboard/resultNotAnnounced.html")
    else:
        positions = Position.objects.all()
        categorized_candidates = defaultdict(list)

        for position in positions:
            candidates = Candidate.objects.filter(position=position).order_by('-total_vote')
            categorized_candidates[position.title] = candidates

        return render(request, "Voter Dashboard/result.html", {'categorized_candidates': dict(categorized_candidates)})
   
def custom_charts(request):
    candidate_labels = []
    candidate_data = []

    candidate_queryset = Candidate.objects.order_by('-total_vote') # Adjust as needed
    for candidate in candidate_queryset:
        candidate_labels.append(candidate.name)
        candidate_data.append(candidate.total_vote)

    position_labels = []
    position_data = []

    position_queryset = Position.objects.order_by('-total_vote')  # Adjust as needed
    for position in position_queryset:
        position_labels.append(position.title)
        position_data.append(position.total_vote)
    
    return render(request, 'Others/charts.html', {
        'candidate_labels': candidate_labels,
        'candidate_data': candidate_data,
        'position_labels': position_labels,
        'position_data': position_data
    })
   
@login_required
def ballot(request):
    user = request.user
    voted_candidates = ControlVote.objects.filter(user=user, status=True).select_related('candidate', 'position')
    return render(request, 'Voter Dashboard/ballot.html', {'voted_candidates': voted_candidates})    

def resultNotAnnounced(request):
    return render(request,"Voter Page/resultNotAnnounced.html")

@login_required
def passwordChange(request):
    if request.method == 'POST':
        # Get the posted data directly from request.POST
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if both new passwords match
        if new_password1 != new_password2:
            return HttpResponse("New passwords do not match.", status=400)

        # Check if the old password is correct
        if not request.user.check_password(old_password):
            return HttpResponse("Invalid old password.", status=400)

        # Update the password
        request.user.set_password(new_password1)
        request.user.save()

        # Update the session hash
        update_session_auth_hash(request, request.user)

        # Redirect to a success page
        return redirect('voterPage')
    else:
        # Render the password change page
        return render(request, "passwordReset.html")

def profileChange(request):
    voter = Voter.objects.get(Email=request.user.email)

    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user = request.user
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update voter information
        voter.First_Name = request.POST.get('first_name')
        voter.Last_Name = request.POST.get('last_name')
        voter.Email = request.POST.get('email')
        voter.CNIC = request.POST.get('cnicNum')
        voter.Address = request.POST.get('address')
        voter.Phone_Number = request.POST.get('phone')
        voter.save()

        return redirect('voterPage')
    else:
        return render(request, "Voter Dashboard/changeProfile.html", {'voter': voter})
