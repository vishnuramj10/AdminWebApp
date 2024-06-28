# forms.py
from django import forms
from django.forms import modelformset_factory, formset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *  # Import your User and Supervisor models

common_attrs = {
    'class': 'form-control',  # CSS class for styling
}

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput({ 'placeholder': '@rutgers.edu', **common_attrs}) 
        )
    is_supervisor = forms.ChoiceField(
            choices=[(True, 'Yes'), (False, 'No')],
            label="Are you a supervisor?",
            widget=forms.RadioSelect(attrs={'class': 'form-check-inline'})
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_supervisor'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        is_supervisor = eval(self.data.get('is_supervisor'))

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')


        # Check if the email exists in the Supervisor model
        user_record = Supervisor.objects.filter(email=email).first()
        if not user_record:
            raise forms.ValidationError('The provided email is not the database. Please enter the email associated with Rutgers.')

        # If the supervisor exists, check if they are a supervisor
        if is_supervisor==True and user_record.supervisor==False:
            raise forms.ValidationError('The supervisor associated with this email is not marked as a supervisor.')

        # If the supervisor exists, check if they are a supervisor
        if is_supervisor==False and user_record.supervisor==True:
            raise forms.ValidationError('The supervisor associated with this email is marked as a supervisor.')
        
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supervisor = self.cleaned_data['is_supervisor']
        if commit:
            user.save()
        return user

class PersonForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.Textarea(attrs={'rows': 1,**common_attrs}),
    )
    phone_number = forms.CharField(
            label="Phone Number",
            max_length=100,
            widget=forms.TextInput(attrs=common_attrs),
            required=True
        )   
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs=common_attrs) 
        )
    class Meta:
        model = Person
        fields = ['name', 'phone_number', 'email']  # Include only the fields you want in the form

class TravelPreAuthorizationModelForm(forms.ModelForm):
    today_date = forms.DateField(
        label="Today's Date",
        widget=forms.DateInput(attrs={'type': 'date', **common_attrs}),
        required=True
    )
    signature = forms.CharField(
        label="Signature",
        max_length=100,
        widget=forms.TextInput(attrs=common_attrs),
        required=True
    )
    date_of_travel_from_date = forms.DateField(
        label="From Date",
        widget=forms.DateInput(attrs={'type': 'date', **common_attrs}),
        required=True
    )
    date_of_travel_to_date = forms.DateField(
        label="To Date",
        widget=forms.DateInput(attrs={'type': 'date', **common_attrs}),
        required=True
    )

    conference_name = forms.CharField(
        label="Conference Name",
        max_length=200,
        widget=forms.Textarea(attrs={'rows': 2}),  # Apply custom CSS class and set rows to 1
        required=True
    ) 
    conference_location = forms.CharField(
        label="Conference Location",
        max_length=100,
        widget=forms.TextInput(attrs=common_attrs),
        required=True
    )
    reason_for_travel = forms.CharField(
        label="Reason for Travel",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, **common_attrs}),
        required=True
    )
    people_travelling = forms.DecimalField(
        label="People Travelling",
        min_value=0,
        widget=forms.NumberInput(attrs={'id': 'people-travelling', **common_attrs}),
        required=True
    )
    hotel_cost = forms.DecimalField(
        label="Hotel ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'cost-field', 'id': 'hotel-cost', **common_attrs}),
        required=True
    )
    conference_registration_cost = forms.DecimalField(
        label="Conference Registration ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'cost-field', 'id': 'conference-reg-cost', **common_attrs}),
        required=True
    )
    airfare_train_cost = forms.DecimalField(
        label="Airfare/Train ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'cost-field', 'id': 'airfare-train-cost', **common_attrs}),
        required=True
    )
    car_rental_cost = forms.DecimalField(
        label="Car Rental ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'cost-field', 'id': 'car-rental-cost', **common_attrs}),
        required=True
    )
    other_misc_costs = forms.DecimalField(
        label="Other Miscellaneous Costs ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'cost-field', 'id': 'other-costs', **common_attrs})
    )
    total_estimated_costs = forms.DecimalField(
        label="Total Estimated Costs ($)",
        widget=forms.NumberInput(attrs={'id': 'total-costs', **common_attrs}),
    )
    comments = forms.CharField(
        label="Comments",
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50, **common_attrs}),
    )
    #supervisor_choices = [(supervisor.id, supervisor.name) for supervisor in Supervisor.objects.filter(supervisor=True)]
    supervisor = forms.ChoiceField(
        label="Supervisor",
        widget=forms.Select(attrs={'class': 'form-control big-select'}) # You will populate choices dynamically
    )
    associate_director = forms.ChoiceField(
        label="Associate Director",
        choices=[(1,'Kimaada')],  # You will populate choices dynamically
        required=True,
        widget=forms.Select(attrs={'class': 'form-control big-select'})
    )
    class Meta:
        model = TravelAuthForm
        exclude = ['submitted_by', 'final_approval_status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].choices = [
            (supervisor.id, supervisor.name) for supervisor in Supervisor.objects.filter(supervisor=True)
        ]
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("date_of_travel_from_date")
        to_date = cleaned_data.get("date_of_travel_to_date")

        if from_date and to_date and from_date >= to_date:
            raise forms.ValidationError('You cannot have To Date before From Date')

        return cleaned_data
        