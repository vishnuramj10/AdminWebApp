from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *  # Assuming you have a UserProfile model
from .forms import *
from travelrequestapp.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from .utils import *
from django.db.models import Q


from .forms import *
@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    is_supervisor = user_profile.supervisor
    
    if request.method == 'POST':
        form = TravelPreAuthorizationModelForm(request.POST)
        form.submitted_by = user_profile.id
        PersonFormSet = modelformset_factory(Person, form=PersonForm, exclude=['travel_auth_form'])
        formset = PersonFormSet(request.POST) 
        if form.is_valid():
            travel_pre_auth = form.save(commit=False)
            travel_pre_auth.submitted_by = user_profile  # Set the submitted_by field to the current user profile
            travel_pre_auth.final_approval_status = 'Pending'  # Set the initial final approval status
            travel_pre_auth.save()
            supervisor_email = Supervisor.objects.get(id=form.cleaned_data.get('supervisor')).email
            send_email('Automated email :: Sent for Approval', 'Your request has been sent to your supervisor for Approval.', 
                      ['vb440@scarletmail.rutgers.edu'])
            #send_mail('Automated email :: Approval Sent', 'Your request has been sent to your supervisor for Approval.', 
             #         settings.EMAIL_HOST_USER, [f'{user_profile.email}'])
            #send_email('Automated email :: New Approval Request', 'You have received a new Travel Request', 
             #         [f'{supervisor_email}'])
            if form.cleaned_data.get('people_travelling') > 0:
                if formset.is_valid():
                    prefix = 1
                    for form in formset:
                        person = form.save(commit=False)
                        person.name = request.POST.get(f'form-{str(prefix)}-name')
                        person.phone_number = request.POST.get(f'form-{prefix}-phone_number')
                        person.email = request.POST.get(f'form-{prefix}-email')
                        person.travel_auth_form_id = travel_pre_auth.id
                        person.save()
                        prefix += 1
                else:
                    print(formset.errors)
            return redirect('travelrequestapp:home')
        else:
            print(form.errors)
    else:
        form = TravelPreAuthorizationModelForm()
        PersonFormSet = modelformset_factory(Person, form=PersonForm, exclude=['travel_auth_form'])
        formset = PersonFormSet(queryset=Person.objects.none())  # Pass an empty queryset

    supervisor_forms = []
    approved_forms = []
    rejected_forms = []

    def fetch_related_data(forms):
        for form in forms:
            submitted_user_profile = Supervisor.objects.get(email=form.submitted_by.email)
            form.submitted_by_name = submitted_user_profile.name
            print(form.submitted_by_name)
            form.related_persons = Person.objects.filter(travel_auth_form_id=form.id)

    if is_supervisor:
        if request.user.email == 'kimaada@rutgers.edu':
            supervisor_forms = TravelAuthForm.objects.filter(first_approval=True, second_approval=False, final_approval_status='Pending') 
        else:
            supervisor_profile = Supervisor.objects.get(email=request.user.email)
            supervisor_forms = TravelAuthForm.objects.filter(supervisor=supervisor_profile.id, first_approval=False)


        # for person_form in supervisor_forms:
        #     submitted_user_profile = User.objects.filter(id = person_form.submitted_by)
        #     submitted_user_profile = Supervisor.objects.get(email=submitted_user_profile.email)
        #     person_form.submitted_by_name = submitted_user_profile.name
        #     person_form.related_persons = Person.objects.filter(travel_auth_form_id=person_form.id)
        approved_forms = TravelAuthForm.objects.filter(Q(final_approval_status='Approved') | (Q(first_approval=True) & Q(final_approval_status='Pending')))        # for person_form in approved_forms:
        #     submitted_user_profile = User.objects.filter(id = person_form.submitted_by)
        #     submitted_user_profile = Supervisor.objects.get(email=submitted_user_profile.email)
        #     person_form.submitted_by_name = submitted_user_profile.name
        #     person_form.related_persons = Person.objects.filter(travel_auth_form_id=person_form.id)

        rejected_forms = TravelAuthForm.objects.filter(final_approval_status='Rejected')
        # for person_form in rejected_forms:
        #     submitted_user_profile = User.objects.filter(id = person_form.submitted_by)
        #     submitted_user_profile = Supervisor.objects.get(email=submitted_user_profile.email)
        #     person_form.submitted_by_name = submitted_user_profile.name
        #     person_form.related_persons = Person.objects.filter(travel_auth_form_id=person_form.id)

        fetch_related_data(supervisor_forms)
        fetch_related_data(approved_forms)
        fetch_related_data(rejected_forms)

    context = {
        "form": form,
        "formset": formset,
        'is_supervisor': is_supervisor,
        'supervisor_forms': supervisor_forms,
        'approved_forms': approved_forms,
        'rejected_forms': rejected_forms,
    }
    return render(request, "home.html", context)

    
def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            user.email = email  # Set the email for the user
            user.save()
            # Check if the 'is_supervisor' checkbox is checked
            is_supervisor = form.cleaned_data['is_supervisor']
            # Create a UserProfile instance associated with the user
            UserProfile.objects.create(user=user, supervisor=is_supervisor, email = email)
            return redirect("travelrequestapp:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form":form})

def approvals(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        action = request.POST.get('action')
        form_instance = TravelAuthForm.objects.get(id=form_id)
        #user_email = UserProfile.objects.get(id=form_instance.submitted_by).user.email
        #print(user_email)
        if action == 'approve':
            if request.user.email == 'kimaada@rutgers.edu' and form_instance.first_approval == True:
                form_instance.second_approval = True
                form_instance.final_approval_status = 'Approved'
                form_instance.save()
                send_email('Automated email :: Approved', f'Your Travel Request made on {form_instance.today_date} has been Approved.', 
                      ['vb440@scarletmail.rutgers.edu'])
                #send_mail('Automated email :: Request Approved', f'Your Travel Request made on {form_instance.today_date} has been Approved.', 
                 #         settings.EMAIL_HOST_USER, [f'{user_email}'])
            if form_instance.first_approval == False:
                form_instance.first_approval = True
                form_instance.save()
                send_email('Automated email :: Approved by Supervisor', f'Your Travel Request made on {form_instance.today_date} has been Approved by your supervisor and sent to your Associate Director.', 
                      ['vb440@scarletmail.rutgers.edu'])
                #send_mail('Automated email :: Request Approved by Supervisor', f'Your Travel Request made on {form_instance.today_date} has been Approved by your supervisor and sent to your Associate Director.', 
                  #        settings.EMAIL_HOST_USER, [f'{user_email}'])
                #send_mail('Automated email :: New Request for Approval', f'You have received a Travel Request made on {form_instance.today_date}', 
                   #       settings.EMAIL_HOST_USER, ['kimaada@rutgers.edu'])
        elif action == 'reject':
            if request.user.email == 'kimaada@rutgers.edu' and form_instance.first_approval == True:
                form_instance.second_approval = False
                form_instance.final_approval_status = 'Rejected'
                form_instance.save()
                send_email('Automated email :: Rejected', f'Your Travel Request made on {form_instance.today_date} has been Rejected by your Associate Director.', 
                      ['vb440@scarletmail.rutgers.edu']) 
                #send_mail('Automated email :: Request Approved', f'Your Travel Request made on {form_instance.today_date} has been Rejected.', 
                 #         settings.EMAIL_HOST_USER, [f'{user_email}']) 
            if form_instance.first_approval == False:
                form_instance.final_approval_status = 'Rejected'
                form_instance.save()
                send_email('Automated email :: Rejected by Supervisor', f'Your Travel Request made on {form_instance.today_date} has been Rejected by your Supervisor.', 
                      ['vb440@scarletmail.rutgers.edu'])
                 #send_mail('Automated email :: Request Rejected by Supervisor', f'Your Travel Request made on {form_instance.today_date} has been Rejected by your Supervisor.', 
                  #        settings.EMAIL_HOST_USER, [f'{user_email}'])

                
    return HttpResponse()

def logout_view(request):
    logout(request)
